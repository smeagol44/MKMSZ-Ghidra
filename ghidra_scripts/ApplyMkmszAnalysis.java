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
        if (sha != null && !sha.equalsIgnoreCase(EXPECTED_SHA256)) {
            popup("Refusing to apply MKMSZ symbols: unexpected SHA-256:\n" + sha);
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

            function.setName(name, SourceType.USER_DEFINED);
            setPlateComment(address, "[MKMSZ] " + evidence + "\n" + comment);
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

            createLabel(address, name, true, SourceType.USER_DEFINED);
            setPlateComment(address, "[MKMSZ] " + evidence + "\n" + comment);
            count++;
        }
        return count;
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
