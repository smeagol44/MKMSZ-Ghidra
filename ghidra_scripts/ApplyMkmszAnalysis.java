// Apply shared MKMSZ analysis names/comments to the currently open program.
// @category MKMSZ

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import ghidra.program.model.symbol.Symbol;

public class ApplyMkmszAnalysis extends GhidraScript {

    private static final String EXPECTED_SHA256 =
        "9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6";

    @Override
    public void run() throws Exception {
        if (currentProgram == null) {
            popup("Open the MKMSZ program first.");
            return;
        }

        String sha = currentProgram.getExecutableSHA256();
        if (sha == null || !sha.equalsIgnoreCase(EXPECTED_SHA256)) {
            popup("Refusing to apply MKMSZ symbols: missing or unexpected SHA-256:\n" + sha);
            return;
        }

        File repoRoot = askDirectory("Select MKMSZ-Ghidra repository root", "Select");
        if (repoRoot == null) {
            return;
        }

        int functions = applyFunctions(new File(repoRoot, "analysis/functions.tsv"));
        int globals = applyGlobals(new File(repoRoot, "analysis/globals.tsv"));

        println("MKMSZ analysis applied: " + functions + " function entries, " +
            globals + " global entries.");
    }

    private int applyFunctions(File file) throws Exception {
        int count = 0;
        for (String[] row : readTsv(file)) {
            Address address = toAddr(parseHexAddress(row[0]));
            String name = row[1];
            String evidence = row[2];
            String comment = row[3];

            Function function = getFunctionAt(address);
            if (function == null) {
                println("No function at " + address + "; skipped " + name);
                continue;
            }

            if (!name.equals(function.getName())) {
                // The original importer used USER_DEFINED names. A differing locally
                // owned name must survive reimport, even if the row changed upstream.
                if (function.getSymbol().getSource() == SourceType.USER_DEFINED) {
                    println("Preserving local function name at " + address +
                        ": " + function.getName() + " != " + name);
                    continue;
                }
                function.setName(name, SourceType.USER_DEFINED);
            }
            applyManagedPlateComment(address, evidence, comment);
            count++;
        }
        return count;
    }

    private int applyGlobals(File file) throws Exception {
        int count = 0;
        for (String[] row : readTsv(file)) {
            Address address = toAddr(parseHexAddress(row[0]));
            String name = row[1];
            String evidence = row[2];
            String comment = row[3];

            Symbol prior = currentProgram.getSymbolTable().getPrimarySymbol(address);
            if (prior != null && !name.equals(prior.getName())) {
                // Do not replace a hand-named address or steal its primary symbol.
                if (prior.getSource() == SourceType.USER_DEFINED) {
                    println("Preserving local global label at " + address +
                        ": " + prior.getName() + " != " + name);
                    continue;
                }
            }
            if (prior == null || !name.equals(prior.getName())) {
                createLabel(address, name, true, SourceType.USER_DEFINED);
            }
            applyManagedPlateComment(address, evidence, comment);
            count++;
        }
        return count;
    }

    private void applyManagedPlateComment(Address address, String evidence, String text) {
        String previous = getPlateComment(address);
        if (previous != null && !previous.startsWith("[MKMSZ]")) {
            println("Preserving locally owned plate comment at " + address);
            return;
        }
        String managed = "[MKMSZ] " + evidence + "\n" + text;
        if (!managed.equals(previous)) setPlateComment(address, managed);
    }

    private List<String[]> readTsv(File file) throws IOException {
        if (!file.isFile()) {
            throw new FileNotFoundException(file.getAbsolutePath());
        }

        List<String[]> rows = new ArrayList<>();
        List<String> lines = Files.readAllLines(file.toPath(), StandardCharsets.UTF_8);

        boolean first = true;
        for (String line : lines) {
            if (first) {
                first = false;
                continue;
            }
            if (line.trim().isEmpty() || line.startsWith("#")) {
                continue;
            }

            String[] parts = line.split("\\t", 4);
            if (parts.length != 4) {
                println("Malformed TSV row skipped: " + line);
                continue;
            }
            rows.add(parts);
        }
        return rows;
    }

    private long parseHexAddress(String text) {
        String s = text.trim().toLowerCase();
        if (s.startsWith("0x")) {
            s = s.substring(2);
        }
        return Long.parseUnsignedLong(s, 16);
    }
}
