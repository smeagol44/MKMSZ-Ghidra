// Read-only check of imported curated MKMSZ global names, types, comments and navigation.
// Does not create/rename/clear any symbols, data, functions, bookmarks or comments.
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

public class AuditMkmszImportedState extends GhidraScript {
    private static final String CLEAN_SHA =
        "9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6";
    private static final CategoryPath CATEGORY = new CategoryPath("/MKMSZ");
    private File root;
    private int checked = 0, mismatches = 0;
    private final Map<String, Integer> checks = new LinkedHashMap<>();
    private final Map<String, Integer> failures = new LinkedHashMap<>();

    @Override
    public void run() throws Exception {
        if (currentProgram == null ||
            !CLEAN_SHA.equalsIgnoreCase(currentProgram.getExecutableSHA256())) {
            println("MKMSZ import audit REFUSED: open the clean USA Rev.0 global program");
            return;
        }
        root = askDirectory("Select MKMSZ-Ghidra repository root", "Select");
        if (root == null) return;
        auditFunctions();
        auditGlobals();
        auditCodeLabels();
        auditTypes();
        auditTypedData();
        auditComments();
        auditBookmarks();
        println("MKMSZ read-only import audit: " + (checked - mismatches) + "/" +
            checked + " exact record checks, " + mismatches + " mismatch(es)");
        for (String category : checks.keySet()) {
            println("  " + category + ": " +
                (checks.get(category) - failures.getOrDefault(category, 0)) +
                "/" + checks.get(category) + " exact");
        }
        if (mismatches != 0) {
            println("Review mismatch lines above; locally owned differences may be intentional.");
            println("No database edits performed. Missing data names can be fixed by the updated extended importer.");
        }
        else println("All audited records match manifests (not proof of all-Wiki semantic completeness).");
    }

    private List<String[]> rows(String name, int count) throws IOException {
        File file = new File(new File(root, "analysis"), name);
        if (!file.isFile()) throw new FileNotFoundException(file.getAbsolutePath());
        List<String[]> result = new ArrayList<>();
        boolean header = true;
        for (String line : Files.readAllLines(file.toPath(), StandardCharsets.UTF_8)) {
            if (header) { header = false; continue; }
            if (line.isEmpty() || line.startsWith("#")) continue;
            String[] cells = line.split("\\t", -1);
            if (cells.length != count) throw new IOException("Malformed " + name + ": " + line);
            if (name.equals("functions.tsv") || name.equals("globals.tsv") ||
                cells[0].equals("global")) result.add(cells);
        }
        return result;
    }

    private Address at(String address) {
        return toAddr(Long.decode(address));
    }

    private void check(String category, String where, boolean ok, String actual) {
        checked++;
        checks.put(category, checks.getOrDefault(category, 0) + 1);
        if (ok) return;
        mismatches++;
        failures.put(category, failures.getOrDefault(category, 0) + 1);
        println("MISMATCH " + category + " " + where + ": " + actual);
    }

    private String primary(Address addr) {
        Symbol s = currentProgram.getSymbolTable().getPrimarySymbol(addr);
        return s == null ? "(none)" : s.getName() + " (" + s.getSource() + ")";
    }

    private void auditFunctions() throws Exception {
        for (String[] r : rows("functions.tsv", 4)) {
            Address addr = at(r[0]);
            Function f = getFunctionAt(addr);
            check("global-function", r[0], f != null && f.getName().equals(r[1]),
                "expected " + r[1] + ", found " + (f == null ? "(no function)" : f.getName()));
        }
    }

    private void auditGlobals() throws Exception {
        for (String[] r : rows("globals.tsv", 4)) {
            Address addr = at(r[0]);
            Symbol s = currentProgram.getSymbolTable().getPrimarySymbol(addr);
            check("global-label", r[0], s != null && s.getName().equals(r[1]),
                "expected " + r[1] + ", found " + primary(addr));
        }
    }

    private void auditCodeLabels() throws Exception {
        for (String[] r : rows("code_labels.tsv", 5)) {
            Address addr = at(r[1]);
            boolean found = false;
            for (Symbol s : currentProgram.getSymbolTable().getSymbols(addr)) {
                if (s.getName().equals(r[2])) { found = true; break; }
            }
            check("code-label", r[1], found, "missing secondary label " + r[2]);
        }
    }

    private void auditTypes() throws Exception {
        Map<String, DataType> found = new HashMap<>();
        for (String[] r : rows("types.tsv", 10)) {
            String kind = r[1];
            if (kind.equals("struct") || kind.equals("enum")) {
                DataType dt = currentProgram.getDataTypeManager().getDataType(
                    new DataTypePath(CATEGORY, r[2]));
                found.put(r[2], dt);
                int wanted = (int) Long.decode(r[3]).longValue();
                check("type-definition", r[2],
                    dt != null && dt.getLength() == wanted,
                    "expected size " + r[3] + ", actual " +
                    (dt == null ? "(missing)" : Integer.toString(dt.getLength())));
            }
            else if (kind.equals("field")) {
                DataType dt = found.get(r[2]);
                int offset = (int) Long.decode(r[5]).longValue();
                DataTypeComponent comp = dt instanceof Structure ?
                    ((Structure) dt).getComponentAt(offset) : null;
                boolean ok = comp != null && r[4].equals(comp.getFieldName());
                check("type-field", r[2] + "+" + r[5], ok,
                    "expected " + r[4] + ", actual " +
                    (comp == null ? "(missing)" : comp.getFieldName()));
            }
            else if (kind.equals("member")) {
                DataType dt = found.get(r[2]);
                boolean ok = dt instanceof ghidra.program.model.data.Enum &&
                    ((ghidra.program.model.data.Enum) dt).contains(r[4]);
                check("enum-member", r[2] + ":" + r[4], ok,
                    "expected enum member " + r[4]);
            }
        }
    }

    private void auditTypedData() throws Exception {
        for (String[] r : rows("data.tsv", 6)) {
            Address addr = at(r[1]);
            DataType wanted = currentProgram.getDataTypeManager().getDataType(
                new DataTypePath(CATEGORY, r[2]));
            Data d = getDataAt(addr);
            boolean typed = wanted != null && d != null &&
                d.getDataType().isEquivalent(wanted);
            check("typed-data", r[1], typed, "expected " + r[2] + ", actual " +
                (d == null ? "(no data)" : d.getDataType().getName()));
            if (typed && !r[3].isEmpty()) {
                Symbol s = currentProgram.getSymbolTable().getPrimarySymbol(addr);
                check("typed-data-label", r[1], s != null && r[3].equals(s.getName()),
                    "expected " + r[3] + ", found " + primary(addr));
            }
        }
    }

    private void auditComments() throws Exception {
        for (String[] r : rows("comments.tsv", 5)) {
            Address addr = at(r[1]);
            CodeUnit unit = currentProgram.getListing().getCodeUnitAt(addr);
            int kind;
            if (r[2].equals("plate")) kind = CodeUnit.PLATE_COMMENT;
            else if (r[2].equals("pre")) kind = CodeUnit.PRE_COMMENT;
            else if (r[2].equals("eol")) kind = CodeUnit.EOL_COMMENT;
            else if (r[2].equals("post")) kind = CodeUnit.POST_COMMENT;
            else if (r[2].equals("repeatable")) kind = CodeUnit.REPEATABLE_COMMENT;
            else throw new IOException("Unknown comment kind " + r[2]);
            String actual = unit == null ? null : unit.getComment(kind);
            String expected = "[MKMSZ] " + r[3] + "\n" + r[4];
            check("comment", r[1] + ":" + r[2], expected.equals(actual),
                actual == null ? "(missing)" : "present but different (may be local)");
        }
    }

    private void auditBookmarks() throws Exception {
        BookmarkManager bm = currentProgram.getBookmarkManager();
        for (String[] r : rows("bookmarks.tsv", 5)) {
            Address addr = at(r[1]);
            String category = "MKMSZ/" + r[2];
            Bookmark existing = bm.getBookmark(addr, "Info", category);
            String expected = r[3] + ": " + r[4];
            check("bookmark", r[1] + ":" + category,
                existing != null && expected.equals(existing.getComment()),
                existing == null ? "(missing)" : "present with locally different note");
        }
    }
}
