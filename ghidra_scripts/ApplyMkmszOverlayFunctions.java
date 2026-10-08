// Guarded MIPS32 function entry recovery for separately imported MKMSZ raw overlays.
// Requires original stock source, exact stage scope, and verified 16-byte entry signatures.
// It does not clear existing code/data, cross stages, or infer unknown function entry points.
// @category MKMSZ
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;

import ghidra.app.cmd.disassemble.MipsDisassembleCommand;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.*;
import ghidra.program.model.data.Undefined;
import ghidra.program.model.lang.Register;
import ghidra.program.model.listing.*;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.symbol.SourceType;

public class ApplyMkmszOverlayFunctions extends GhidraScript {
    private static final long MAX_FLOW_WINDOW = 0x1000L;
    private File root;
    private String scope;
    private String stage;
    private long romStart, romEnd, base, end;
    private int created, renamed, unchanged, review, disassembled;

    @Override
    public void run() throws Exception {
        if (currentProgram == null) throw new IOException("Open an overlay program first");
        String[] args = getScriptArgs();
        root = args.length > 0 ? new File(args[0]) :
            askDirectory("Select MKMSZ-Ghidra repository root", "Select");
        if (root == null) return;
        if (!identifyExactOverlay()) {
            println("MKMSZ function import REFUSED: unrecognized or incorrectly mapped overlay");
            return;
        }
        Map<String, String> signatures = new LinkedHashMap<>();
        for (String[] line : load("overlay_function_guards.tsv", 4)) {
            if (line[0].equals(scope)) {
                if (signatures.put(line[1], line[2]) != null)
                    throw new IOException("Duplicate entry guard " + line[1]);
            }
        }
        List<String[]> functions = new ArrayList<>();
        for (String[] row : load("overlay_functions.tsv", 5))
            if (row[0].equals(scope)) functions.add(row);
        if (functions.size() != signatures.size() || functions.isEmpty())
            throw new IOException("Missing or extra function entry guards for " + scope);
        for (String[] row : functions) {
            if (!signatures.containsKey(row[1]))
                throw new IOException("No original-byte guard for " + row[1]);
        }

        println("MKMSZ overlay function import scope: " + scope +
            " (" + stage + "), entries=" + functions.size());
        for (String[] row : functions) {
            monitor.checkCancelled();
            try {
                applyOne(row, signatures.get(row[1]), functions);
            }
            catch (Exception error) {
                review++;
                println("REVIEW " + row[2] + " at " + row[1] + ": " + error);
            }
        }
        println("MKMSZ overlay function import: created=" + created +
            ", renamed=" + renamed + ", unchanged=" + unchanged +
            ", disassembled=" + disassembled + ", review=" + review +
            " (scope=" + scope + ")");
        println("Run ApplyMkmszExtended.java afterward only for other scoped metadata.");
    }

    private boolean identifyExactOverlay() throws Exception {
        if (!currentProgram.getLanguage().isBigEndian() ||
            !currentProgram.getLanguage().getProcessor().toString().equalsIgnoreCase("MIPS") ||
            currentProgram.getAddressFactory().getDefaultAddressSpace().getSize() != 32)
            return false;
        String sha = currentProgram.getExecutableSHA256();
        String name = currentProgram.getName();
        if (sha == null || sha.isEmpty()) return false;
        String found = null;
        for (String[] line : load("scopes.tsv", 3)) {
            if (line[0].equals("global")) continue;
            if (line[1].equals(name) && line[2].equalsIgnoreCase(sha))
                found = line[0];
        }
        if (found == null) return false;
        for (String[] row : load("overlays.tsv", 8)) {
            if (!row[0].equals(found)) continue;
            if (!row[6].equalsIgnoreCase(sha)) return false;
            scope = found;
            stage = row[1];
            romStart = Long.decode(row[3]);
            romEnd = Long.decode(row[4]);
            base = Long.decode(row[5]);
            end = base + romEnd - romStart;
            if (romStart >= romEnd || end > 0x100000000L) return false;
            Address begin = toAddr(base);
            Address last = toAddr(end - 1);
            MemoryBlock block = currentProgram.getMemory().getBlock(begin);
            if (block == null || !block.getStart().equals(begin) ||
                block.getSize() != (romEnd - romStart) ||
                !currentProgram.getMemory().contains(last)) return false;
            return true;
        }
        return false;
    }

    private void applyOne(String[] row, String guard, List<String[]> functions) throws Exception {
        Address at = toAddr(Long.decode(row[1]));
        long address = at.getOffset();
        if (address < base || address + 16 > end || (address & 3) != 0) {
            reject(row, "outside scoped overlay or not 4-byte aligned"); return;
        }
        if (!guard.matches("[0-9a-fA-F]{32}")) {
            reject(row, "invalid manifest prefix (must be exactly 16 bytes)"); return;
        }
        StringBuilder observed = new StringBuilder();
        for (int i = 0; i < 16; i++)
            observed.append(String.format(Locale.ROOT, "%02x",
                currentProgram.getMemory().getByte(at.add(i)) & 0xff));
        if (!guard.equalsIgnoreCase(observed.toString())) {
            reject(row, "original 16-byte entry guard mismatch"); return;
        }
        Function owner = getFunctionContaining(at);
        if (owner != null && !owner.getEntryPoint().equals(at)) {
            reject(row, "entry is inside a different function " + owner.getName()); return;
        }
        Instruction instruction = currentProgram.getListing().getInstructionAt(at);
        if (instruction != null && instruction.getLength() != 4) {
            reject(row, "preexisting instruction is not 4-byte MIPS32; do not clear"); return;
        }
        Register mode = currentProgram.getProgramContext().getRegister("ISA_MODE");
        if (instruction != null && mode != null) {
            java.math.BigInteger value =
                currentProgram.getProgramContext().getValue(mode, at, false);
            if (value != null && value.intValue() != 0) {
                reject(row, "preexisting ISA_MODE is not MIPS32"); return;
            }
        }
        if (instruction == null) {
            Data data = currentProgram.getListing().getDataContaining(at);
            if (data != null && !Undefined.isUndefined(data.getDataType())) {
                reject(row, "existing typed data at function entry"); return;
            }
            long exclusiveEnd = Math.min(end, address + MAX_FLOW_WINDOW);
            for (String[] other : functions) {
                long next = Long.decode(other[1]);
                if (next > address && next < exclusiveEnd) exclusiveEnd = next;
            }
            for (String[] pickup : load("rom_pickups.tsv", 15)) {
                if (!pickup[0].equals(stage)) continue;
                long pickupSource = Long.decode(pickup[4]);
                long pickupVa = base + pickupSource - romStart;
                if (pickupVa > address && pickupVa < exclusiveEnd)
                    exclusiveEnd = pickupVa;
            }
            // The restricted interval never contains a different cataloged
            // function entry, cataloged pickup structure, or adjacent overlay.
            long max = exclusiveEnd - 1;
            if (max < address + 3) {
                reject(row, "no disassembly window remains"); return;
            }
            AddressSet restrict = new AddressSet(at, toAddr(max));
            // This invokes the same correct 32-bit mode as Ghidra's explicit
            // "Disassemble MIPS", not the default MIPS16-sensitive action.
            MipsDisassembleCommand decode =
                new MipsDisassembleCommand(at, restrict, false);
            decode.enableCodeAnalysis(false);
            if (!decode.applyTo(currentProgram, monitor)) {
                reject(row, "MIPS32 disassembly failed: " + decode.getStatusMsg()); return;
            }
            instruction = currentProgram.getListing().getInstructionAt(at);
            if (instruction == null || instruction.getLength() != 4) {
                reject(row, "disassembler did not produce MIPS32 entry"); return;
            }
            disassembled++;
        }
        Function function = getFunctionAt(at);
        if (function == null) {
            CreateFunctionCmd cmd = new CreateFunctionCmd(at);
            if (!cmd.applyTo(currentProgram, monitor)) {
                reject(row, "cannot create function: " + cmd.getStatusMsg()); return;
            }
            function = getFunctionAt(at);
            if (function == null) {
                reject(row, "creation command did not produce a function"); return;
            }
            created++;
        }
        if (!function.getName().equals(row[2])) {
            if (function.getSymbol().getSource() == SourceType.USER_DEFINED) {
                reject(row, "preserving user-named function " + function.getName()); return;
            }
            function.setName(row[2], SourceType.USER_DEFINED);
            renamed++;
        }
        else unchanged++;
        String prior = getPlateComment(at);
        if (prior == null || prior.startsWith("[MKMSZ]")) {
            String comment = "[MKMSZ] " + row[3] + "\n" + row[4];
            if (!comment.equals(prior)) setPlateComment(at, comment);
        }
        println("OK " + row[2] + " at " + at +
            " (body instructions are bounded by decoded flow; inspect if truncated)");
    }

    private void reject(String[] row, String why) {
        review++;
        println("REVIEW " + row[2] + " at " + row[1] + ": " + why);
        // Refusals do not modify code, types, function bodies, or labels.
    }

    private List<String[]> load(String filename, int columns) throws IOException {
        File file = new File(new File(root, "analysis"), filename);
        List<String[]> result = new ArrayList<>();
        boolean header = true;
        for (String line : Files.readAllLines(file.toPath(), StandardCharsets.UTF_8)) {
            if (header) { header = false; continue; }
            if (line.isEmpty() || line.startsWith("#")) continue;
            String[] cells = line.split("\t", -1);
            if (cells.length != columns)
                throw new IOException("Invalid " + filename + " row: " + line);
            result.add(cells);
        }
        return result;
    }
}
