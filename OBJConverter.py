'''
Created on 11.08.2016

@author: BuXXe
'''

import OBJClass
import os

if __name__ == '__main__':
    
    # Filename without extension! (.reo .obj and .mtl will be appended in code)
    # TODO: Right now we assume the obj file is in the same directory as the OBJConverter.py
    filename="spyro"

    # read the obj file
    with open(filename+".obj", 'r') as f:
        read_data = f.readlines()
    
    # TODO: perhaps use only regex in future but for now keep it simple
    # TODO: perhaps we should use some kind of grammar or state machine to parse the file
    
    # iterate through the read_data
    linecounter = 0
    
    # create new object
    OBJ = OBJClass.OBJ()
    
    # set filename as model name
    # Change this if you want a different name
    OBJ.name = filename
    
    
    
    # INFO: Comments and empty lines will be ignored as for now
    while(linecounter < len(read_data)):
        if(read_data[linecounter][0] == '#' or read_data[linecounter][0] == '\n'):
            linecounter += 1
            continue
        
        # Build material dictionary
        elif(read_data[linecounter].startswith("mtllib")):
            mtlfile = read_data[linecounter].replace("mtllib ","",1).replace("\n","")
            # read the mtl file
            with open(mtlfile, 'r') as f:
                mtl_data = f.readlines()
                f.close()
            
            mtl_linecounter = 0
            while(mtl_linecounter < len(mtl_data)):
                if(mtl_data[mtl_linecounter].startswith("newmtl")):
                    # get material name
                    materialname = mtl_data[mtl_linecounter].replace("newmtl ","",1).replace("\n","")
                    # search for a map_Kd entry to get the texture
                if(mtl_data[mtl_linecounter].startswith("map_Kd")):
                    # set only filename as texture entry
                    print "happens"
                    OBJ.materials[materialname] = os.path.basename(mtl_data[mtl_linecounter].replace("map_Kd ","",1).replace("\n",""))
                
                mtl_linecounter+=1
            
        
                       
        # Build up lists of vertices vt and faces
        elif(read_data[linecounter].startswith("v ")):
            OBJ.vertices.append(read_data[linecounter].replace("v ","",1).replace("\n",""))
        
        elif(read_data[linecounter].startswith("vt ")):
            OBJ.vertexTexcoord.append(read_data[linecounter].replace("vt ","",1).replace("\n",""))
            
        elif(read_data[linecounter].startswith("usemtl")):
            # set active material which will be used by the following faces
            activeMaterial = read_data[linecounter].replace("usemtl ","",1).replace("\n","")
            # add entry to faces dictionary if not yet existing and initialize empty list
            if not activeMaterial in OBJ.faces:
                OBJ.faces[activeMaterial] = []
        
        elif(read_data[linecounter].startswith("f ")):
            OBJ.faces[activeMaterial].append(read_data[linecounter].replace("f ","",1).replace("\n",""))
            OBJ.facecount +=1
        
        linecounter += 1    
            
    

    
    # Create the .reo file
    with open(filename+".reo", 'w') as f:
        f.write("# Riot Engine Object\n")
        f.write("# Created with the .obj to .reo converter by BuXXe\n\n")
        
        f.write("version " + OBJ.version + "\n")
        f.write("name "+ OBJ.name +"\n")
        
        f.write("created by "+ OBJ.author+ " on " + OBJ.creationDate + "\n\n")
        
        f.write("Lighting " + str(OBJ.lighting) + "\n\n")
        
        #write materials
        f.write("materials " + str(len(OBJ.materials)) + "\n")
        for index,entry in enumerate(sorted(OBJ.materials)):
            f.write(str(index)+ " texture " + OBJ.materials[entry] + "\n")
        
        f.write("\n")
        f.write("transform\n")
        for en in OBJ.transform:
            f.write(" ".join([str(d) for d in en])+"\n")
        
        f.write("\n")
        f.write("vertices "+ str(len(OBJ.vertices)) +"\n")
        
        for index, vert in enumerate(OBJ.vertices):
            f.write(str(index) +" " + vert + "\n")
            
        f.write("\n")
        f.write("faces " +str(OBJ.facecount)+ "\n")
        f.write("\n")
        
        # create blocks and print them
        facecounter = 0
        
        
        for material in sorted(OBJ.faces):
            for face in OBJ.faces[material]:
                f.write("polygon "+str(facecounter)+"\n")
                facecounter+=1
                fparts = face.split(" ")
                               
                f.write("vt "+str(len(fparts))+":" + " ".join([str(int(d.split("/")[0]) - 1) for d in reversed(fparts)]) + "\n")
                f.write("ma " + str(sorted(OBJ.materials).index(material)) + "\n")
                f.write("tu "+ " ".join(  [ OBJ.vertexTexcoord[(int(d.split("/")[1]) - 1)].split(" ")[0] for d in reversed(fparts)]) + "\n")
                f.write("tv "+ " ".join(  [ OBJ.vertexTexcoord[(int(d.split("/")[1]) - 1)].split(" ")[1] for d in reversed(fparts)]) + "\n")
                f.write("\n")
