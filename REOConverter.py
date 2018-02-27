'''
Created on 08.08.2016

@author: BuXXe
'''

import REOClass

if __name__ == '__main__':
    
    # Filename without extension! (.reo .obj and .mtl will be appended in code)
    # TODO: Right now we assume the reo file is in the same directory as the REOConverter.py
    filename="DragonHead(H)"

    # read the reo file
    # blocks: version, name, created by ... on, lighting, transform, materials, faces, vertices, bspheres/bboxes 
    with open(filename+".reo", 'r') as f:
        read_data = f.readlines()
    
    # TODO: perhaps use only regex in future but for now keep it simple
    # TODO: perhaps we should use some kind of grammar or state machine to parse the file
    
    # iterate through the read_data
    linecounter = 0
    
    # create new object
    REO = REOClass.REO()
    
    # INFO: Comments and empty lines will be ignored as for now
    while(linecounter < len(read_data)):
        if(read_data[linecounter][0] == '#' or read_data[linecounter][0] == '\n'):
            linecounter += 1
            continue
        
        # set metadata
        elif(read_data[linecounter].startswith("version")):
            REO.version = read_data[linecounter].replace("version ","",1).replace("\n","")
        elif(read_data[linecounter].startswith("name")):
            REO.name = read_data[linecounter].replace("name ","",1).replace("\n","")
        elif(read_data[linecounter].startswith("created by")):
            authoranddate = read_data[linecounter].replace("created by ","",1).replace("\n","")
            # INFO: might seem complex but is necessary cause a user could have " on " as part of his name 
            # which would perhaps even kill the REO Importer of the Riot Engine
            # TODO: Right now we assume a fixed length for the date. Perhaps a more flexible way of solving this split would be nice
            REO.creationDate = authoranddate[-10:]
            REO.author = authoranddate[:-14]

        elif(read_data[linecounter].startswith("Lighting")):
            REO.lighting = read_data[linecounter].replace("Lighting ","",1).replace("\n","")
        
        elif(read_data[linecounter].startswith("materials")):
            materialcount = read_data[linecounter].replace("materials ","",1).replace("\n","")
            # walk over the next #materialcount lines to collect the materials
            materials = []
            for n in xrange (int(materialcount)):
                # TODO: right now we assume the format: ID TYPE FILENAME (Filenames without any spaces!)
                # If there is a model with no texture the entry is ex.: 0 Texture(0)
                # For these definitions the converter would crash due index out of range
                entry = read_data[linecounter+n+1].replace("\n","").split(" ")
                materials.append([entry[1],entry[2]])
                
            REO.materials = materials

            # jump over #materialcount lines 
            linecounter += int(materialcount)
        
        elif(read_data[linecounter].startswith("transform")):
            # INFO: Assumes that after transform keyword we will have 3 lines representing the matrix
            REO.transform = [read_data[linecounter+1].replace("\n","").split(" "), read_data[linecounter+2].replace("\n","").split(" "), read_data[linecounter+3].replace("\n","").split(" ")]
            linecounter+=3
            
        elif(read_data[linecounter].startswith("vertices")):    
            vertexcount = read_data[linecounter].replace("vertices ","",1).replace("\n","")
            # walk over the next #vertexcount lines to collect the vertices
            vertices = []
            for n in xrange (int(vertexcount)):
                # TODO: right now we assume the format: ID X Y Z 
                # if there are other formats, for example including the W entry, this needs to be changed
                entry = read_data[linecounter+n+1].replace("\n","").split(" ")
                vertices.append([entry[1],entry[2],entry[3]])
                
            REO.vertices = vertices
            
            # jump over #vertexcount lines 
            linecounter += int(vertexcount)
        
        
        elif(read_data[linecounter].startswith("faces")):  
            facecount = read_data[linecounter].replace("faces ","",1).replace("\n","")
            # Assumption: There is an empty line after the faces entry. Then we have blocks of 5 or 6 lines per polygon
            # TODO: The Inner Temple has an entry "fl 2S" in a polygon block which leads to a 6 line block.
            
            linecounter+=1
            faces = []
            
            # Dictionary of UV-Tex-Coords -> vtid
            reverseTexDict = {}
            # VT entries of format [U,V]
            vtentries = []
            
            # walk over the next #facecount blocks to collect the faces
            for n in xrange (int(facecount)):
                # INFO: polygon rows may be ignored as they are only giving structural information
                vt = read_data[linecounter+n*6+2].replace("\n","")
                # each face has: used vertices, corresponding UV coords per vertex, used material
                                
                # face entry consists of: [[vertices],[vtextureids],materialid]
                face = vt.split(":")[1].split(" ")
                mat = read_data[linecounter+n*6+3].replace("\n","").split(" ")[1]
                                
                Utex = read_data[linecounter+n*6+4].replace("\n","").replace("tu ","",1).split(" ")
                Vtex = read_data[linecounter+n*6+5].replace("\n","").replace("tv ","",1).split(" ")
                
                # list holding the corresponding vt ids for the current faces' vertices
                vtent = []
                for i in xrange(len(face)):
                        
                    # If there is no entry in the reverseTexDict for the current UV coords, create 
                    # an entry and append UV coords to vtentries list
                    if str([Utex[i],Vtex[i]]) not in reverseTexDict:
                        reverseTexDict[str([Utex[i],Vtex[i]])] = len(vtentries)
                        vtentries.append([Utex[i],Vtex[i]]) 
                    
                    # Append the textureid to the list
                    vtent.append(reverseTexDict[str([Utex[i],Vtex[i]])])
                    

                # TODO: fl 2S entries are not further investigated yet and will be ignored as for now                    
                if(read_data[linecounter+n*6+6].startswith("fl")):
                    linecounter+=1
                
                # add vt entries    
                faces.append([face,vtent,mat])

            REO.faces = faces
            REO.vtentries = vtentries
            
            # jump over #facecount * 6 lines 
            linecounter += int(facecount)*6
            
        # TODO: We cannot use the bounding data in the obj format. Right now we will just ignore them. 
        # In future approach, we could parse the bounding spheres / boxes as model data.
        elif(read_data[linecounter].startswith("bspheres")):  
            bspherecount = read_data[linecounter].replace("bspheres ","",1).replace("\n","")
            # Assumption again: Seems to have an empty line before the bsphere block like in face def above
            linecounter+=1
                         
            bspheres = []
            # walk over the next #bspherecount blocks to collect the bspheres
            
            for n in xrange (int(bspherecount)):
                # Assumption: 3 lines per bsphere
                bspheres.append([read_data[linecounter+n*4+1].replace("\n",""),read_data[linecounter+n*4+2].replace("\n",""),read_data[linecounter+n*4+3].replace("\n","")])
             
            REO.bspheres = bspheres
            # jump over #bspherecount * 4 lines 
            linecounter += int(bspherecount)*4
        
        elif(read_data[linecounter].startswith("bboxes")):
            bboxcount = read_data[linecounter].replace("bboxes ","",1).replace("\n","")
            # Assumption again: Seems to have an empty line before the bboxes block like in face and bsphere def above
            linecounter+=1
                         
            bboxes = []
            # walk over the next #bboxcount blocks to collect the bboxes
            
            for n in xrange (int(bboxcount)):
                # Assumption: 6 lines per bbox
                
                bbox =[]
                for i in xrange(1,7):
                    bbox.append(read_data[linecounter+n*7+i].replace("\n",""))
                    
                bboxes.append(bbox)
             
            REO.bboxes = bboxes
            # jump over #bboxcount * 7 lines 
            linecounter += int(bboxcount)*7

        linecounter += 1    
            
    # print REO.__dict__
    withTextures = True
    
    if(withTextures):
        # Build the mtl file
        with open(filename+".mtl", 'w') as f:
            f.write("# Material file for REO file: "+REO.name+"\n")
            f.write("\n")        
            # Assumption: Only entries of id Texutre Filename in reo file
            for index,entry in enumerate(REO.materials):
                f.write("newmtl Material"+str(index) +"\n")
                f.write("map_Kd " + entry[1] +"\n")
                f.write("\n")
            
            f.close()

    # Now lets build an obj file:
    with open(filename+".obj", 'w') as f:
        if(withTextures):
            f.write("mtllib " + filename+".mtl" + "\n")
            f.write("\n")
        
        # vertices
        for entry in REO.vertices:
            f.write("v "+" ".join(entry)+"\n")
        
        f.write("\n")
    
        # vertex texture coords
        if(withTextures):
            for en in REO.vtentries: 
                f.write("vt "+" ".join(en)+"\n")
                  
        f.write("\n")
        
          
        if(withTextures):
            # INFO: blocks with entries per material -> smaller obj file but changes order of the faces!
            # face definitions with vt ids
            # preprocess and build the blocks
            # dictionary holds lists of face definitions per materialid
            faceblocks={}
            # initialize list
            for index,entry in enumerate(REO.materials):
                faceblocks[str(index)] = []
            
            for entry in REO.faces:
                withtexid = []
                # associate the vertices with their corresponding vt entry id
                for index,vert in enumerate(entry[0]):
                    withtexid.append(str(int(vert)+1)+'/'+ str(int(entry[1][index])+1) )
               
                faceblocks[entry[2]].append("f "+" ".join(withtexid)+"\n")
            
            # write blocks of faces per material 
            for entry in sorted(faceblocks):
                f.write("usemtl Material"+entry+"\n")
                for face in faceblocks[entry]:
                    f.write(face)
        
        else:
            for entry in REO.faces:
                withtexid = [str(int(d)+1) for d in entry[0]]
                f.write("f "+" ".join(withtexid)+"\n")
                        