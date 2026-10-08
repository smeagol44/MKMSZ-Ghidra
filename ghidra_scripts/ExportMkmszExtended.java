// Export Ghidra's richer analysis as an independent review snapshot.
// Read-only: never overwrites curated analysis/*.tsv.
// @category MKMSZ

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.data.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.SourceType;

public class ExportMkmszExtended extends GhidraScript {
    private PrintWriter out;

    @Override
    public void run() throws Exception {
        if (currentProgram == null) {
            popup("Open the MKMSZ program first.");
            return;
        }
        File directory = askDirectory("Choose review-export folder", "Export");
        if (directory == null) return;
        if (!directory.exists() && !directory.mkdirs())
            throw new IOException("Cannot create export directory");
        File output = new File(directory, "extended-review.tsv");
        try (PrintWriter writer = new PrintWriter(
                new OutputStreamWriter(new FileOutputStream(output), StandardCharsets.UTF_8))) {
            out = writer;
            record("record", "address_or_name", "detail", "notes");
            exportTypes();
            exportFunctions();
            exportBookmarks();
            exportComments();
        }
        println("Review-only Ghidra metadata snapshot: " + output.getAbsolutePath());
    }

    private void record(String kind, String address, String detail, String notes) {
        out.println(clean(kind) + "\t" + clean(address) + "\t" +
            clean(detail) + "\t" + clean(notes));
    }

    private String clean(String s) {
        return s == null ? "" :
            s.replace("\t", " ").replace("\r", " ").replace("\n", " / ");
    }

    private void exportTypes() {
        Iterator<DataType> it = currentProgram.getDataTypeManager().getAllDataTypes();
        while (it.hasNext()) {
            DataType type = it.next();
            if (!type.getCategoryPath().getPath().equals("/MKMSZ")) continue;
            if (type instanceof Structure) {
                Structure st = (Structure) type;
                record("struct", st.getName(), "length=" + st.getLength(), "");
                for (DataTypeComponent field : st.getDefinedComponents())
                    record("field", st.getName(), "offset=" + field.getOffset() +
                        " " + field.getDataType().getName(),
                        field.getFieldName() + " " + field.getComment());
            }
            else if (type instanceof ghidra.program.model.data.Enum) {
                ghidra.program.model.data.Enum en = (ghidra.program.model.data.Enum) type;
                record("enum", en.getName(), "length=" + en.getLength(), "");
                for (String name : en.getNames())
                    record("member", en.getName(), name, "value=" + en.getValue(name));
            }
        }
    }

    private void exportFunctions() {
        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
        while (it.hasNext()) {
            Function function = it.next();
            String at = function.getEntryPoint().toString();
            if (function.getSignatureSource() == SourceType.USER_DEFINED)
                record("signature", at, function.getPrototypeString(false, false),
                    "Review calling convention and inferred params before importing");
            for (Variable variable : function.getLocalVariables()) {
                if (variable.getSource() != SourceType.USER_DEFINED) continue;
                String storage = variable.hasStackStorage() ?
                    "stack=" + variable.getStackOffset() :
                    variable.getVariableStorage().toString();
                record("local", at, variable.getName() + ":" +
                    variable.getDataType().getName(), storage);
            }
        }
    }

    private void exportBookmarks() {
        Iterator<Bookmark> it = currentProgram.getBookmarkManager().getBookmarksIterator();
        while (it.hasNext()) {
            Bookmark bookmark = it.next();
            if (!bookmark.getCategory().startsWith("MKMSZ/")) continue;
            record("bookmark", bookmark.getAddress().toString(),
                bookmark.getCategory(), bookmark.getComment());
        }
    }

    private void exportComments() {
        CodeUnitIterator it = currentProgram.getListing().getCodeUnits(true);
        final int[] kinds = {
            CodeUnit.PLATE_COMMENT, CodeUnit.PRE_COMMENT, CodeUnit.EOL_COMMENT,
            CodeUnit.POST_COMMENT, CodeUnit.REPEATABLE_COMMENT
        };
        final String[] labels = {"plate", "pre", "eol", "post", "repeatable"};
        while (it.hasNext()) {
            CodeUnit cu = it.next();
            for (int i = 0; i < kinds.length; i++) {
                String value = cu.getComment(kinds[i]);
                if (value == null || !value.startsWith("[MKMSZ]")) continue;
                record("comment/" + labels[i], cu.getAddress().toString(), value, "");
            }
        }
    }
}
