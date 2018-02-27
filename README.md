# Drakan-REO-OBJ-Converter
These scripts can convert Drakan Order of the Flame 3D model files (REO - Riot Engine Objects) to .OBJ files and vice versa.

## Overview
In Documentation/REO-FileStructure.pdf I have collected all the information I could gather about the REO format. It still has some unknown features which are also mentioned in the pdf.  
The conversion does not handle any bounding box information.  
A .mtl material file for the needed textures will be created / used in the conversion to support correct texturing.

## Usage
When exporting a .REO file from the Drakan Editor, you will receive the REO file with the needed textures in bmp format.
You need to move the REO file to the folder where the scripts are run the converter script REOConverter.py in which you replace the filename variable with the file you want to convert.
If you want to convert the .OBJ to a .REO, you need to place the .OBJ and .MTL file (Material file) in the same folder and run OBJConverter.py (replace the filename variable with the one you want to convert)

## Screens
#### Example REO to OBJ conversion
![Church REO to OBJ converted](documentation/screens/REO%20to%20OBJ/Church-TexturedCorrectly.jpg)  
![DragonHead REO to OBJ converted](documentation/screens/REO%20to%20OBJ/DragonHead-TexturedCorrectly.jpg)  

#### Example OBJ to REO conversion
![Blender monkey in modeler](documentation/screens/OBJ%20to%20REO/OBJtoREOMonkey.jpg)  
![Spryo OBJ in editor](documentation/screens/OBJ%20to%20REO/Spyro.jpg)  
![Spyro OBJ ingame](documentation/screens/OBJ%20to%20REO/IngameSpyro.jpg)  
