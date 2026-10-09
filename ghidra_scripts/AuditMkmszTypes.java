// Compare existing /MKMSZ types with exact curated TSV definitions without modifying Ghidra.
// @category MKMSZ
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.data.*;

public class AuditMkmszTypes extends GhidraScript {
    private static final String CLEAN_SHA =
        "9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6";
    private static final CategoryPath CATEGORY = new CategoryPath("/MKMSZ");

    private static class Expected {
        String name;
        String kind;
        int size;
        LinkedHashMap<Integer, String[]> fields = new LinkedHashMap<>();
        LinkedHashMap<String, Long> members = new LinkedHashMap<>();
        Expected(String kind, String name, int size) {
            this.kind = kind;
            this.name = name;
            this.size = size;
        }
    }

    private int pass, mismatch, missing;
    private int observedFields, observedMembers;

    @Override
    public void run() throws Exception {
        if (currentProgram == null ||
            !CLEAN_SHA.equalsIgnoreCase(currentProgram.getExecutableSHA256()) ||
            !currentProgram.getLanguage().isBigEndian()) {
            println("MKMSZ type audit REFUSED: expected exact supported clean USA Rev0 N64 program");
            return;
        }
        String[] args = getScriptArgs();
        File root = args.length != 0 ? new File(args[0]) :
            askDirectory("Select MKMSZ-Ghidra repository root", "Select");
        if (root == null) return;
        File manifest = new File(new File(root, "analysis"), "types.tsv");
        LinkedHashMap<String, Expected> expected = loadExpected(manifest);
        DataTypeManager manager = currentProgram.getDataTypeManager();
        println("MKMSZ read-only type audit: definitions=" + expected.size() +
            ", scope=global, category=/MKMSZ");
        for (Expected type : expected.values()) {
            monitor.checkCancelled();
            DataType present = manager.getDataType(new DataTypePath(CATEGORY, type.name));
            if (present == null) {
                missing++;
                println("MISSING " + type.name + ": no /MKMSZ definition");
                continue;
            }
            ArrayList<String> differences = new ArrayList<>();
            if (present.getLength() != type.size) {
                differences.add("size expected 0x" + Integer.toHexString(type.size) +
                    " found 0x" + Integer.toHexString(present.getLength()));
            }
            if (type.kind.equals("struct")) {
                if (!(present instanceof Structure)) {
                    differences.add("kind expected structure, found " + present.getClass().getSimpleName());
                }
                else compareStructure(type, (Structure) present, differences);
            }
            else if (type.kind.equals("enum")) {
                if (!(present instanceof ghidra.program.model.data.Enum)) {
                    differences.add("kind expected enum, found " + present.getClass().getSimpleName());
                }
                else compareEnum(type, (ghidra.program.model.data.Enum) present, differences);
            }
            else throw new IOException("Unknown expected kind " + type.kind);
            if (differences.isEmpty()) {
                pass++;
                println("MATCH " + type.name + " (0x" + Integer.toHexString(type.size) +
                    " bytes, " + (type.kind.equals("enum") ? type.members.size() + " members" :
                    type.fields.size() + " fields") + ")");
            }
            else {
                mismatch++;
                println("MISMATCH " + type.name + ": " + differences.size() + " differences");
                for (String diff : differences) println("  - " + diff);
            }
        }
        println("MKMSZ read-only type audit: match=" + pass + ", mismatch=" + mismatch +
            ", missing=" + missing + ", checked=" + expected.size() +
            ", fields=" + observedFields + ", enum_members=" + observedMembers);
        println("NO CHANGES MADE: differences require separate review; do not automatically overwrite types.");
    }

    private void compareStructure(Expected want, Structure have, List<String> differences) {
        Map<Integer, DataTypeComponent> actual = new HashMap<>();
        for (DataTypeComponent component : have.getDefinedComponents()) {
            DataTypeComponent old = actual.put(component.getOffset(), component);
            if (old != null) differences.add("duplicate defined component offset +0x" +
                Integer.toHexString(component.getOffset()));
        }
        for (Map.Entry<Integer, String[]> e : want.fields.entrySet()) {
            int offset = e.getKey();
            String[] value = e.getValue();
            String fieldName = value[0], datatype = value[1];
            DataTypeComponent component = actual.remove(offset);
            observedFields++;
            if (component == null) {
                differences.add("missing field " + fieldName + " at +0x" + Integer.toHexString(offset));
                continue;
            }
            if (!fieldName.equals(component.getFieldName())) {
                differences.add("field +0x" + Integer.toHexString(offset) +
                    " name expected " + fieldName + " found " + component.getFieldName());
            }
            DataType fieldType = expectedType(datatype);
            if (!component.getDataType().isEquivalent(fieldType)) {
                differences.add("field " + fieldName + " type expected " + datatype +
                    " found " + component.getDataType().getDisplayName());
            }
            if (component.getLength() != fieldType.getLength()) {
                differences.add("field " + fieldName + " length expected " + fieldType.getLength() +
                    " found " + component.getLength());
            }
        }
        for (DataTypeComponent extra : actual.values()) {
            differences.add("unexpected defined component at +0x" +
                Integer.toHexString(extra.getOffset()) +
                " (" + extra.getFieldName() + ": " + extra.getDataType().getDisplayName() + ")");
        }
    }

    private void compareEnum(Expected want, ghidra.program.model.data.Enum have,
                             List<String> differences) {
        HashSet<String> actualNames = new HashSet<>(Arrays.asList(have.getNames()));
        for (Map.Entry<String, Long> e : want.members.entrySet()) {
            observedMembers++;
            if (!actualNames.remove(e.getKey())) {
                differences.add("missing enum member " + e.getKey());
                continue;
            }
            if (have.getValue(e.getKey()) != e.getValue()) {
                differences.add("enum member " + e.getKey() + " expected 0x" +
                    Long.toHexString(e.getValue()) + " found 0x" +
                    Long.toHexString(have.getValue(e.getKey())));
            }
        }
        for (String unexpected : actualNames)
            differences.add("unexpected enum member " + unexpected +
                " =0x" + Long.toHexString(have.getValue(unexpected)));
    }

    private DataType expectedType(String spec) {
        String s = spec.trim();
        if (s.endsWith("]")) {
            int bracket = s.lastIndexOf('[');
            if (bracket <= 0) throw new IllegalArgumentException("Invalid array type " + s);
            DataType element = expectedType(s.substring(0, bracket));
            int count = Integer.parseInt(s.substring(bracket + 1, s.length() - 1));
            if (count <= 0) throw new IllegalArgumentException("Invalid array count " + s);
            return new ArrayDataType(element, count, element.getLength());
        }
        switch (s) {
            case "u8": return UnsignedCharDataType.dataType;
            case "u16": return UnsignedShortDataType.dataType;
            case "u32": return UnsignedIntegerDataType.dataType;
            case "s32": return IntegerDataType.dataType;
            case "ptr32": return new PointerDataType(Undefined1DataType.dataType, 4);
            default: throw new IllegalArgumentException("Unrecognized manifest field type " + s);
        }
    }

    private LinkedHashMap<String, Expected> loadExpected(File file) throws Exception {
        if (!file.isFile()) throw new FileNotFoundException(file.getAbsolutePath());
        List<String> lines = Files.readAllLines(file.toPath(), StandardCharsets.UTF_8);
        LinkedHashMap<String, Expected> expected = new LinkedHashMap<>();
        if (lines.size() == 0 || !lines.get(0).startsWith("scope\tkind\tname\tsize\t"))
            throw new IOException("Unexpected types.tsv header");
        for (int i = 1; i < lines.size(); i++) {
            if (lines.get(i).isEmpty() || lines.get(i).startsWith("#")) continue;
            String[] row = lines.get(i).split("\t", -1);
            if (row.length != 10) throw new IOException("Invalid types.tsv row " + (i + 1));
            if (!row[0].equals("global")) continue;
            String kind = row[1], name = row[2];
            if (kind.equals("struct") || kind.equals("enum")) {
                if (expected.putIfAbsent(name,
                    new Expected(kind, name, (int) Long.decode(row[3]).longValue())) != null)
                    throw new IOException("Duplicate type " + name);
            }
        }
        for (int i = 1; i < lines.size(); i++) {
            if (lines.get(i).isEmpty() || lines.get(i).startsWith("#")) continue;
            String[] row = lines.get(i).split("\t", -1);
            if (row.length != 10) throw new IOException("Invalid row " + (i + 1));
            if (!row[0].equals("global")) continue;
            String kind = row[1];
            if (!kind.equals("field") && !kind.equals("member")) continue;
            Expected type = expected.get(row[2]);
            if (type == null) throw new IOException("Unknown parent " + row[2]);
            if (kind.equals("field")) {
                if (!type.kind.equals("struct")) throw new IOException("Field on non-struct " + type.name);
                int offset = (int) Long.decode(row[5]).longValue();
                if (type.fields.putIfAbsent(offset, new String[] {row[4], row[6]}) != null)
                    throw new IOException("Duplicate field offset " + type.name + "+" + offset);
            }
            else {
                if (!type.kind.equals("enum")) throw new IOException("Member on non-enum " + type.name);
                if (type.members.putIfAbsent(row[4], Long.decode(row[7])) != null)
                    throw new IOException("Duplicate enum member " + type.name + "." + row[4]);
            }
        }
        return expected;
    }
}
