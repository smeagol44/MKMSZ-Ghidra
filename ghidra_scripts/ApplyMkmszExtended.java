// Apply reviewed types, signatures, locals, data, bookmarks and relations.
// Additional metadata is additive and guarded; unsupported overlay programs fail closed.
// @category MKMSZ

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.data.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;

public class ApplyMkmszExtended extends GhidraScript {
    private static final String CLEAN_SHA =
        "9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6";
    private static final CategoryPath CATEGORY = new CategoryPath("/MKMSZ");
    private File root;
    private String scope;
    private int applied = 0, skipped = 0;
    private Map<String, DataType> pendingTypes = Collections.emptyMap();

    @Override
    public void run() throws Exception {
        if (currentProgram == null) throw new IOException("Open a program first");
        String[] arguments = getScriptArgs();
        root = arguments.length != 0 ? new File(arguments[0]) :
            askDirectory("Select MKMSZ-Ghidra repository root", "Select");
        if (root == null) return;
        scope = identifyScope();
        if (scope == null) {
            println("MKMSZ extended analysis REFUSED: program identity not in analysis/scopes.tsv");
            return;
        }
        println("MKMSZ extended analysis scope: " + scope);
        // Define types first, then code/data consumers.
        applyTypes();
        applySignatures();
        applyLocals();
        applyData();
        applyComments();
        applyBookmarks();
        applyRelations();
        println("MKMSZ extended analysis: applied " + applied +
            ", skipped " + skipped + " (scope=" + scope + ")");
    }

    private String identifyScope() throws Exception {
        String hash = currentProgram.getExecutableSHA256();
        if (hash == null || hash.trim().isEmpty()) {
            println("Missing imported-file SHA-256: cannot verify target safely.");
            return null;
        }
        String name = currentProgram.getName();
        for (String[] row : rows("scopes.tsv", 3)) {
            if (row[0].equals("global")) {
                if (!row[2].equalsIgnoreCase(CLEAN_SHA)) {
                    throw new IOException("Global scope hash manifest was changed");
                }
                if (hash.equalsIgnoreCase(row[2])) return "global";
            }
            else if (!row[2].isEmpty() && row[1].equals(name) &&
                     hash.equalsIgnoreCase(row[2])) return row[0];
        }
        println("Program: " + name + " sha256=" + hash);
        return null;
    }

    private List<String[]> rows(String file, int columns) throws Exception {
        File path = new File(new File(root, "analysis"), file);
        if (!path.isFile()) throw new FileNotFoundException(path.getAbsolutePath());
        List<String[]> result = new ArrayList<>();
        boolean header = true;
        for (String line : Files.readAllLines(path.toPath(), StandardCharsets.UTF_8)) {
            if (header) { header = false; continue; }
            if (line.isEmpty() || line.startsWith("#")) continue;
            String[] cells = line.split("\\t", -1);
            if (cells.length != columns)
                throw new IOException(file + " expected " + columns + " columns: " + line);
            if (file.equals("scopes.tsv") || cells[0].equals(scope)) result.add(cells);
        }
        return result;
    }

    private long number(String s) {
        return Long.decode(s);
    }

    private Address addr(String s) {
        return toAddr(number(s));
    }

    private boolean mapped(Address a) {
        if (!currentProgram.getMemory().contains(a)) {
            println("Unmapped address " + a + " in " + scope + "; skipped");
            skipped++;
            return false;
        }
        return true;
    }

    private DataType resolveType(String spec) {
        String s = spec.trim();
        if (s.endsWith("]")) {
            int bracket = s.lastIndexOf('[');
            if (bracket <= 0) throw new IllegalArgumentException("Bad array " + s);
            DataType element = resolveType(s.substring(0, bracket));
            int count = Integer.parseInt(s.substring(bracket + 1, s.length() - 1));
            if (count < 1 || element.getLength() <= 0)
                throw new IllegalArgumentException("Bad array length " + s);
            return new ArrayDataType(element, count, element.getLength());
        }
        if (s.equals("u8")) return UnsignedCharDataType.dataType;
        if (s.equals("u16")) return UnsignedShortDataType.dataType;
        if (s.equals("u32")) return UnsignedIntegerDataType.dataType;
        if (s.equals("s32")) return IntegerDataType.dataType;
        if (s.equals("void")) return VoidDataType.dataType;
        if (s.equals("ptr32")) return new PointerDataType(Undefined1DataType.dataType, 4);
        DataType staged = pendingTypes.get(s);
        if (staged != null) return staged;
        DataType custom = currentProgram.getDataTypeManager().getDataType(
            new DataTypePath(CATEGORY, s));
        if (custom == null) throw new IllegalArgumentException("Unknown type: " + s);
        return custom;
    }

    private void applyTypes() throws Exception {
        // schema: scope,kind,name,size,field,offset,datatype,value,evidence,note
        List<String[]> records = rows("types.tsv", 10);
        Map<String, DataType> pending = new LinkedHashMap<>();
        for (String[] r : records) {
            if (!r[1].equals("struct") && !r[1].equals("enum")) continue;
            if (pending.containsKey(r[2])) throw new IOException("Duplicate type " + r[2]);
            int size = (int) number(r[3]);
            if (r[1].equals("struct"))
                pending.put(r[2], new StructureDataType(CATEGORY, r[2], size));
            else pending.put(r[2], new EnumDataType(CATEGORY, r[2], size));
        }
        DataTypeManager manager = currentProgram.getDataTypeManager();
        pendingTypes = pending;
        for (String[] r : records) {
            if (!r[1].equals("field") && !r[1].equals("member")) continue;
            DataType parent = pending.get(r[2]);
            if (parent == null) throw new IOException("Missing parent type: " + r[2]);
            if (r[1].equals("field")) {
                if (!(parent instanceof Structure)) throw new IOException("Not a struct: " + r[2]);
                Structure st = (Structure) parent;
                int offset = (int) number(r[5]);
                DataType valueType = resolveType(r[6]);
                // Define into an existing undefined span, without shifting subsequent fields.
                if (offset < 0 || offset + valueType.getLength() > st.getLength())
                    throw new IOException("Field outside " + r[2] + ": " + r[4]);
                if (st.getDefinedComponentAtOrAfterOffset(offset) != null) {
                    DataTypeComponent next = st.getDefinedComponentAtOrAfterOffset(offset);
                    if (next.getOffset() < offset + valueType.getLength())
                        throw new IOException("Overlapping fields in " + r[2]);
                }
                st.replaceAtOffset(offset, valueType, -1, r[4], r[9]);
            }
            else {
                if (!(parent instanceof ghidra.program.model.data.Enum))
                    throw new IOException("Not an enum: " + r[2]);
                ((ghidra.program.model.data.Enum) parent).add(r[4], number(r[7]), r[9]);
            }
        }
        pendingTypes = Collections.emptyMap();
        for (Map.Entry<String, DataType> entry : pending.entrySet()) {
            DataType existing = manager.getDataType(new DataTypePath(CATEGORY, entry.getKey()));
            if (existing != null) {
                if (!existing.isEquivalent(entry.getValue()))
                    println("Existing locally edited type " + entry.getKey() + "; skipped");
                skipped++;
            }
            else {
                manager.addDataType(entry.getValue(), DataTypeConflictHandler.KEEP_HANDLER);
                applied++;
            }
        }
    }

    private void applySignatures() throws Exception {
        // scope,address,return_type,parameters,evidence,note
        for (String[] r : rows("signatures.tsv", 6)) {
            Address at = addr(r[1]);
            if (!mapped(at)) continue;
            Function f = getFunctionAt(at);
            if (f == null || f.getSignatureSource() == SourceType.USER_DEFINED) {
                println("Signature at " + at + " missing/already user-defined; skipped");
                skipped++; continue;
            }
            DataType ret = resolveType(r[2]);
            List<Variable> params = new ArrayList<>();
            if (!r[3].isEmpty()) {
                for (String piece : r[3].split(",")) {
                    String[] p = piece.split(":", -1);
                    if (p.length != 2) throw new IOException("Bad parameter " + piece);
                    params.add(new ParameterImpl(p[0], resolveType(p[1]), currentProgram));
                }
            }
            // No forced storage conflicts, no guessed calling-convention changes.
            f.replaceParameters(Function.FunctionUpdateType.DYNAMIC_STORAGE_ALL_PARAMS,
                false, SourceType.USER_DEFINED, params.toArray(new Variable[0]));
            f.setReturnType(ret, SourceType.USER_DEFINED);
            applied++;
        }
    }

    private void applyLocals() throws Exception {
        // scope,function_address,name,datatype,stack_offset,evidence,note
        for (String[] r : rows("locals.tsv", 7)) {
            Address at = addr(r[1]);
            if (!mapped(at)) continue;
            Function f = getFunctionAt(at);
            if (f == null) { skipped++; continue; }
            int offset = (int) number(r[4]);
            boolean conflict = false;
            for (Variable v : f.getAllVariables()) {
                if (r[2].equals(v.getName()) ||
                    (v.hasStackStorage() && v.getStackOffset() == offset)) {
                    conflict = true; break;
                }
            }
            if (conflict) { skipped++; continue; }
            f.addLocalVariable(new LocalVariableImpl(r[2], resolveType(r[3]),
                offset, currentProgram), SourceType.USER_DEFINED);
            applied++;
        }
    }

    private void applyData() throws Exception {
        // scope,address,datatype,label,evidence,note
        for (String[] r : rows("data.tsv", 6)) {
            Address at = addr(r[1]);
            if (!mapped(at)) continue;
            if (currentProgram.getListing().getInstructionContaining(at) != null) {
                println("Instruction at data address " + at + "; skipped");
                skipped++; continue;
            }
            DataType wanted = resolveType(r[2]);
            Data existing = getDataAt(at);
            if (existing != null && !Undefined.isUndefined(existing.getDataType())) {
                if (!existing.getDataType().isEquivalent(wanted))
                    println("Existing different data at " + at + "; skipped");
                skipped++; continue;
            }
            // Ghidra rejects overlaps: do not clear instructions or existing data.
            try {
                createData(at, wanted);
                if (!r[3].isEmpty() && getSymbolAt(at) == null)
                    createLabel(at, r[3], true, SourceType.USER_DEFINED);
                applied++;
            }
            catch (Exception ex) { println("Data at " + at + " skipped: " + ex); skipped++; }
        }
    }

    private void applyComments() throws Exception {
        // scope,address,kind,evidence,text
        for (String[] r : rows("comments.tsv", 5)) {
            Address at = addr(r[1]);
            if (!mapped(at)) continue;
            CodeUnit unit = currentProgram.getListing().getCodeUnitAt(at);
            if (unit == null) { skipped++; continue; }
            int kind;
            if (r[2].equals("plate")) kind = CodeUnit.PLATE_COMMENT;
            else if (r[2].equals("pre")) kind = CodeUnit.PRE_COMMENT;
            else if (r[2].equals("eol")) kind = CodeUnit.EOL_COMMENT;
            else if (r[2].equals("post")) kind = CodeUnit.POST_COMMENT;
            else if (r[2].equals("repeatable")) kind = CodeUnit.REPEATABLE_COMMENT;
            else throw new IOException("Invalid comment kind " + r[2]);
            String previous = unit.getComment(kind);
            if (previous != null && !previous.startsWith("[MKMSZ]")) {
                skipped++; continue;
            }
            String comment = "[MKMSZ] " + r[3] + "\n" + r[4];
            if (!comment.equals(previous)) { unit.setComment(kind, comment); applied++; }
        }
    }

    private void applyBookmarks() throws Exception {
        // scope,address,category,evidence,note
        BookmarkManager manager = currentProgram.getBookmarkManager();
        for (String[] r : rows("bookmarks.tsv", 5)) {
            Address at = addr(r[1]);
            if (!mapped(at)) continue;
            String category = "MKMSZ/" + r[2];
            String content = r[3] + ": " + r[4];
            Bookmark old = manager.getBookmark(at, "Info", category);
            if (old != null && !old.getComment().equals(content)) {
                skipped++; continue; // Do not replace someone's local note.
            }
            if (old == null) { manager.setBookmark(at, "Info", category, content); applied++; }
        }
    }

    private void applyRelations() throws Exception {
        // scope,from,to,kind,operand,evidence,note
        BookmarkManager bm = currentProgram.getBookmarkManager();
        ReferenceManager rm = currentProgram.getReferenceManager();
        for (String[] r : rows("relations.tsv", 7)) {
            Address from = addr(r[1]), to = addr(r[2]);
            if (!mapped(from) || !mapped(to)) continue;
            String category = "MKMSZ/relation/" + r[3] + "/" + r[2];
            if (bm.getBookmark(from, "Info", category) == null) {
                bm.setBookmark(from, "Info", category,
                    r[5] + ": " + r[6] + " -> " + r[2]);
                applied++;
            }
            if (r[3].equals("NOTE")) continue;
            // Explicit operand only. Never displace or reinterpret stock auto-refs.
            int op = Integer.parseInt(r[4]);
            if (rm.getReference(from, to, op) != null) continue;
            if (rm.getReferencesFrom(from, op).length != 0) {
                println("Reference operand occupied at " + from + " op " + op);
                skipped++; continue;
            }
            RefType type = r[3].equals("DATA_REF") ? RefType.DATA : RefType.UNCONDITIONAL_CALL;
            rm.addMemoryReference(from, to, type, SourceType.USER_DEFINED, op);
            applied++;
        }
    }
}
