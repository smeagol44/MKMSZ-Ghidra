// Export user-defined MKMSZ function/global names for review.
// This deliberately writes to a local export directory and never overwrites
// the repository's canonical analysis files automatically.
// @category MKMSZ

import java.io.*;
import java.nio.charset.StandardCharsets;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.*;

public class ExportMkmszNames extends GhidraScript {

    @Override
    public void run() throws Exception {
        if (currentProgram == null) {
            popup("Open the MKMSZ program first.");
            return;
        }

        File outDir = askDirectory("Select export directory", "Export");
        if (outDir == null) {
            return;
        }
        if (!outDir.exists() && !outDir.mkdirs()) {
            throw new IOException("Could not create " + outDir);
        }

        File functionFile = new File(outDir, "user-functions.tsv");
        File symbolFile = new File(outDir, "user-symbols.tsv");

        exportFunctions(functionFile);
        exportSymbols(symbolFile);

        println("Exported user-defined names to:");
        println("  " + functionFile.getAbsolutePath());
        println("  " + symbolFile.getAbsolutePath());
    }

    private void exportFunctions(File file) throws Exception {
        try (PrintWriter out = new PrintWriter(file, StandardCharsets.UTF_8.name())) {
            out.println("address\tname");
            for (Function function :
                    currentProgram.getFunctionManager().getFunctions(true)) {
                if (function.getSymbol().getSource() != SourceType.USER_DEFINED) {
                    continue;
                }
                out.println("0x" + function.getEntryPoint().toString() + "\t" +
                    sanitize(function.getName()));
            }
        }
    }

    private void exportSymbols(File file) throws Exception {
        try (PrintWriter out = new PrintWriter(file, StandardCharsets.UTF_8.name())) {
            out.println("address\tname\ttype");
            SymbolIterator it = currentProgram.getSymbolTable().getAllSymbols(true);
            while (it.hasNext()) {
                Symbol symbol = it.next();
                if (symbol.getSource() != SourceType.USER_DEFINED) {
                    continue;
                }
                if (symbol.getSymbolType() == SymbolType.FUNCTION) {
                    continue;
                }
                out.println("0x" + symbol.getAddress().toString() + "\t" +
                    sanitize(symbol.getName()) + "\t" + symbol.getSymbolType());
            }
        }
    }

    private String sanitize(String value) {
        return value.replace("\t", " ").replace("\r", " ").replace("\n", " ");
    }
}
