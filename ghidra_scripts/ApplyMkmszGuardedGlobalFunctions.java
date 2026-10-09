// Recover narrowly verified global VI callback only; does not alter other functions.
// @category MKMSZ
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;
import ghidra.app.script.GhidraScript;
import ghidra.app.cmd.disassemble.MipsDisassembleCommand;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.program.model.address.*;
import ghidra.program.model.data.Undefined;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.SourceType;

public class ApplyMkmszGuardedGlobalFunctions extends GhidraScript {
    private static final String CLEAN_SHA="9c18254abf6722b95aa782fcd310bd95f6bcf147da66beb77ce32ca90673ffc6";
    private int created=0, recognized=0, review=0;
    @Override public void run() throws Exception {
        if(currentProgram==null || !CLEAN_SHA.equalsIgnoreCase(currentProgram.getExecutableSHA256()) ||
           !currentProgram.getLanguage().isBigEndian() ||
           !currentProgram.getLanguage().getProcessor().toString().equalsIgnoreCase("MIPS")) {
            println("REFUSED: expected exact clean MKMSZ N64 USA Rev0 MIPS big-endian program"); return;
        }
        String[] args=getScriptArgs();
        File root=args.length>0?new File(args[0]):askDirectory("Select MKMSZ-Ghidra repository root","Select");
        if(root==null)return;
        File manifest=new File(new File(root,"analysis"),"global_function_guards.tsv");
        List<String> lines=Files.readAllLines(manifest.toPath(),StandardCharsets.UTF_8);
        for(int index=1;index<lines.size();index++) {
            String[] row=lines.get(index).split("\t",-1);
            if(row.length!=7)throw new IOException("Bad global function guard row "+(index+1));
            Address at=toAddr(Long.decode(row[0]));
            if(!checkHex(at,row[2]) || !checkHex(at.subtract(8),row[3]) ||
               !checkHex(toAddr(Long.decode(row[4])),row[5])) {
                println("REVIEW "+row[1]+": clean-ROM entry/predecessor/registration guard mismatch");review++;continue;
            }
            Function containing=getFunctionContaining(at);
            if(containing!=null && !containing.getEntryPoint().equals(at)) {
                println("REVIEW "+row[1]+": entry overlaps existing function "+containing.getName());review++;continue;
            }
            Instruction ins=currentProgram.getListing().getInstructionAt(at);
            if(ins!=null && ins.getLength()!=4){println("REVIEW: non-MIPS32 entry at "+at);review++;continue;}
            if(ins==null) {
                Data d=currentProgram.getListing().getDataContaining(at);
                if(d!=null && !Undefined.isUndefined(d.getDataType())) {
                    println("REVIEW: typed data at "+at);review++;continue;
                }
                AddressSet restrict=new AddressSet(at,toAddr(0x80015B80L));
                MipsDisassembleCommand cmd=new MipsDisassembleCommand(at,restrict,false);
                cmd.enableCodeAnalysis(false);
                if(!cmd.applyTo(currentProgram,monitor) ||
                   currentProgram.getListing().getInstructionAt(at)==null ||
                   currentProgram.getListing().getInstructionAt(at).getLength()!=4) {
                    println("REVIEW: could not decode MIPS32 entry "+at);review++;continue;
                }
            }
            Function fn=getFunctionAt(at);
            if(fn==null) {
                CreateFunctionCmd create=new CreateFunctionCmd(at);
                if(!create.applyTo(currentProgram,monitor) || getFunctionAt(at)==null) {
                    println("REVIEW: could not create function "+at);review++;continue;
                }
                fn=getFunctionAt(at);
                created++;
            } else recognized++;
            if(fn.getSymbol().getSource()==SourceType.USER_DEFINED && !row[1].equals(fn.getName())) {
                println("REVIEW: preserving user name "+fn.getName());review++;continue;
            }
            if(!row[1].equals(fn.getName()))fn.setName(row[1],SourceType.USER_DEFINED);
            String previous=getPlateComment(at);
            if(previous==null || previous.startsWith("[MKMSZ]"))
                setPlateComment(at,"[MKMSZ] "+row[6]);
            println("OK "+row[1]+" at "+at);
        }
        println("Guarded global function import: created="+created+", already="+recognized+", review="+review);
    }
    private boolean checkHex(Address address,String expected) throws Exception {
        if(!expected.matches("[0-9a-fA-F]+") || (expected.length()%2)!=0)return false;
        for(int i=0;i<expected.length()/2;i++) {
            int n=Integer.parseInt(expected.substring(i*2,i*2+2),16);
            if(!currentProgram.getMemory().contains(address.add(i)) ||
               (currentProgram.getMemory().getByte(address.add(i))&255)!=n)return false;
        }
        return true;
    }
}
