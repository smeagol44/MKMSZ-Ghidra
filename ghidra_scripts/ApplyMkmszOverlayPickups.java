// Stage-qualified, guarded pickup records for separately imported raw overlays.
// Does NOT create functions or change existing disassembly.
// @category MKMSZ
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.data.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.SourceType;

public class ApplyMkmszOverlayPickups extends GhidraScript {
    @Override public void run() throws Exception {
        String[] args = getScriptArgs();
        File root = args.length > 0 ? new File(args[0]) :
            askDirectory("Choose MKMSZ-Ghidra repository root", "Select");
        if (root == null) return;
        String hash = currentProgram.getExecutableSHA256();
        if (hash == null || !currentProgram.getLanguage().isBigEndian()) {
            println("REFUSED: missing source SHA or not big-endian"); return;
        }
        List<String[]> manifest = load(new File(root,"analysis/overlays.tsv"),8);
        String[] chosen = null;
        for (String[] line: manifest) {
            if (hash.equalsIgnoreCase(line[6]) &&
                currentProgram.getName().startsWith("mkmsz_overlay_"+line[1].toLowerCase(Locale.ROOT)+"_"))
                chosen=line;
        }
        if (chosen == null) {
            println("REFUSED: no matching overlay name and SHA in overlays.tsv"); return;
        }
        final long romLo = Long.decode(chosen[3]), romHi=Long.decode(chosen[4]);
        final long base = Long.decode(chosen[5]);
        if (currentProgram.getMemory().getBlock(toAddr(base)) == null ||
            !currentProgram.getMemory().contains(toAddr(base + romHi-romLo-1))) {
            println("REFUSED: overlay bytes are not mapped at " + chosen[5]); return;
        }
        DataTypeManager mgr=currentProgram.getDataTypeManager();
        CategoryPath cat=new CategoryPath("/MKMSZ");
        DataType dt=mgr.getDataType(new DataTypePath(cat,"MKMSZ_PickupRecord"));
        if (dt == null) {
            StructureDataType structure=new StructureDataType(cat,"MKMSZ_PickupRecord",0x30);
            String[] names={"x_fixed8","y_fixed8","z_fixed8","location_metadata",
                "type_behavior","callback_flags","award_callback","collision_extent_a",
                "collision_extent_b","resource_selector","presentation_descriptor","collected_flag"};
            for(int i=0;i<names.length;i++)
                structure.replaceAtOffset(i*4,UnsignedIntegerDataType.dataType,4,names[i],
                    "Stock ordinary pickup record, see canonical Wiki");
            dt=mgr.addDataType(structure,DataTypeConflictHandler.KEEP_HANDLER);
        }
        if (dt.getLength()!=0x30) {
            println("REFUSED: MKMSZ_PickupRecord is not 0x30 bytes"); return;
        }
        int total=0,created=0,present=0,conflicts=0;
        for (String[] r: load(new File(root,"analysis/rom_pickups.tsv"),15)) {
            if (!r[0].equals(chosen[1])) continue;
            total++;
            long off=Long.decode(r[4]);
            if(off<romLo || off+0x30>romHi) {
                println("Outside overlay: "+r[4]);conflicts++;continue;
            }
            Address at=toAddr(base+off-romLo);
            int[] positions={0x10,0x14,0x18,0x24,0x28,0x2c};
            int[] cols={6,7,8,9,10,11};
            boolean guarded=true;
            for (int i=0;i<positions.length;i++) {
                long got=0;
                for (int b=0;b<4;b++)
                    got=(got<<8)|(currentProgram.getMemory().getByte(at.add(positions[i]+b))&255L);
                if (got != (Long.decode(r[cols[i]]) & 0xffffffffL)) guarded=false;
            }
            if (!guarded) {println("Guard mismatch: "+at);conflicts++;continue;}
            boolean occupied=false, same=false;
            for(int i=0;i<0x30;i++){
                Address here=at.add(i);
                if (currentProgram.getListing().getInstructionContaining(here)!=null) {
                    occupied=true;break;
                }
                Data old=currentProgram.getListing().getDataContaining(here);
                if(old!=null && !Undefined.isUndefined(old.getDataType())){
                    if(i==0 && old.getLength()==0x30 && old.getDataType().isEquivalent(dt))
                        same=true;
                    occupied=true;break;
                }
            }
            if(same){present++;continue;}
            if(occupied){println("Occupied existing markup: "+at);conflicts++;continue;}
            try {
                createData(at,dt);
                String label="pickup_"+chosen[1].toLowerCase(Locale.ROOT)+"_"+
                    String.format(Locale.ROOT,"%02d",Integer.parseInt(r[2]));
                if(getSymbolAt(at)==null)createLabel(at,label,true,SourceType.USER_DEFINED);
                created++;
            } catch(Exception error) {
                println("Could not type pickup at "+at+": "+error);conflicts++;
            }
        }
        println("Overlay "+chosen[1]+" pickup records: expected="+total+
            ", typed="+created+", already typed="+present+", conflicts="+conflicts);
    }
    private List<String[]> load(File file,int columns)throws IOException{
        List<String[]> result=new ArrayList<>();boolean header=true;
        for(String l:Files.readAllLines(file.toPath(),StandardCharsets.UTF_8)){
            if(header){header=false;continue;}
            if(l.isEmpty()||l.startsWith("#"))continue;
            String[] cells=l.split("\\t",-1);
            if(cells.length!=columns)throw new IOException("Malformed "+file+": "+l);
            result.add(cells);
        }
        return result;
    }
}
