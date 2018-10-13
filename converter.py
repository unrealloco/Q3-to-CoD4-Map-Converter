import glob
import msvcrt
import time
import os
import re
import subprocess
import shutil

def __enter__(self):

    return self

def __exit__(self, type, value, traceback):

    pass

def q3map2(path):

    subprocess.check_call([r""+dir_path_root+"/q3map2.exe", "-convert", "-format", "map", "-map", ""+path, "-game", "quake3"])

    time.sleep(2)

    filename = path.replace('.bsp','')

    if os.path.isfile(dir_path_root+'\\out\\'+filename+'_converted.map'):
        os.remove(dir_path_root+'\\out\\'+filename+'_converted.map',dir_fd=None)

    os.rename(dir_path_root+'\\bsp\\'+filename+'_converted.map',dir_path_root+'\\out\\'+filename+'_converted.map')

def removeLines(initLine, endLine, fileName): 

    f = open(fileName, "r")
    list = f.readlines()
    f.close()
    del list[int(initLine):int(endLine)]
    newF = open(fileName, "w")
    newF.writelines(list)
    newF.close()

def remove_patchdef(fileName):

    global loop

    init = False
    end = False

    init_string = "// patch"
    end_string = "\t\t}"
    f = open(fileName, "r")

    for num, line in enumerate(f,1):
        if init_string in line:
            init = True
            init_num = num
            break

    if init == False:
        loop = False
        return

    for num, line in enumerate(f,init_num):
        if end_string in line:
            if num > init_num:
                end = True
                end_num = num
                break

    if end == False:
        return

    removeLines(init_num-1,end_num+3,path)

def fix_uv(filename):

    file_string = ''
    f = open(filename,"r")

    for line in f:
        file_string += line

    final_string = file_string.replace("0 0 0 0.5 0.5 0 0 0","256 256 0 0 0 0 lightmap_gray 35840 35840 0 0 0 0")
    
    h = open(filename,"w")
    h.write(final_string)
    h.close
    f.close

def fix_materials(filename):

    file_string = ''
    f = open(filename,"r")

    for line in f:
        file_string += line

    final_string = re.sub(r"(?=\b\D\D\D\b).*/\b"," ) ", file_string,)
    
    h = open(filename,"w")
    h.write(final_string)
    h.close
    f.close

def few_lines_fix(filename):

    file_string = ''
    f = open(filename,"r")

    for line in f:
        file_string += line

    final_string = file_string.replace("// Generated by Q3Map2 (ydnar) -convert -format map","iwmap 4\n\"000_Global\" flags  active\n\"The Map\" flags ")
    
    h = open(filename,"w")
    h.write(final_string)
    h.close
    f.close

def make_gdt(path,filename):

    file_string = ''
    end_string = ''
    gdt_list = ''
    batch_string = ''
    end_string_fix = ''

    i = 0
    f = open(path,"r")

    for line in f:
        if re.search(r"(?=\b\D\D\D\b).*\s?256",line):
            file_string += line

    array = re.findall(r"(?=\b\D\D\D\b).*\s?256",file_string)

    for line in array:
        if line in end_string:
            continue
        else:
            end_string += line + '\n'

    array_final_list = end_string.split()

    for line in array_final_list:
        if line == "" or line == ")" or line == "256" or line == "caulk" or line == "clip" or line == "trigger" or line == "nodraw" or line == "slick":
            continue
        else: end_string_fix += line + '\n'

    array_final_list = end_string_fix.split()
    array_size = len(array_final_list)

    while i < array_size:
        gdt_list += "\""+array_final_list[i].lower()+"\" ( \"material.gdf\" )\n{\n\"template\" \"material.template\"\n\"materialType\" \"world phong\"\n\"locale_case\" \"0\"\n\"locale_test\" \"1\"\n\"locale_tools\" \"0\"\n\"locale_decal\" \"0\"\n\"locale_Middle_East\" \"0\"\n\"locale_London\" \"0\"\n\"locale_Kiev\" \"0\"\n\"locale_Chechnya\" \"0\"\n\"locale_Generic\" \"0\"\n\"locale_Duhoc\" \"0\"\n\"locale_Villers\" \"0\"\n\"locale_Egypt\" \"0\"\n\"locale_Libya\" \"0\"\n\"locale_Tunisia\" \"0\"\n\"locale_Industrial\" \"0\"\n\"locale_Poland\" \"0\"\n\"locale_Modern_America\" \"0\"\n\"usage\" \"ground\"\n\"surfaceType\" \"concrete\"\n\"missileClip\" \"0\"\n\"bulletClip\" \"0\"\n\"playerClip\" \"0\"\n\"aiClip\" \"0\"\n\"vehicleClip\" \"0\"\n\"itemClip\" \"0\"\n\"canShootClip\" \"0\"\n\"aiSightClip\" \"0\"\n\"noFallDamage\" \"0\"\n\"noSteps\" \"0\"\n\"noImpact\" \"0\"\n\"noMarks\" \"0\"\n\"noPenetrate\" \"0\"\n\"noDrop\" \"0\"\n\"slick\" \"0\"\n\"ladder\" \"0\"\n\"mantleOn\" \"0\"\n\"mantleOver\" \"0\"\n\"noLightmap\" \"0\"\n\"noDynamicLight\" \"0\"\n\"noCastShadow\" \"0\"\n\"noReceiveDynamicShadow\" \"0\"\n\"noDraw\" \"0\"\n\"noFog\" \"0\"\n\"drawToggle\" \"0\"\n\"sky\" \"0\"\n\"radialNormals\" \"0\"\n\"nonColliding\" \"0\"\n\"nonSolid\" \"0\"\n\"transparent\" \"0\"\n\"detail\" \"0\"\n\"structural\" \"0\"\n\"portal\" \"0\"\n\"lightPortal\" \"0\"\n\"origin\" \"0\"\n\"physicsGeom\" \"0\"\n\"hdrPortal\" \"0\"\n\"hasEditorMaterial\" \"0\"\n\"zFeather\" \"0\"\n\"zFeatherDepth\" \"40\"\n\"eyeOffsetDepth\" \"0\"\n\"outdoorOnly\" \"0\"\n\"falloff\" \"0\"\n\"falloffBeginAngle\" \"35\"\n\"falloffEndAngle\" \"65\"\n\"useSpotLight\" \"0\"\n\"distFalloff\" \"0\"\n\"distFalloffBeginDistance\" \"200\"\n\"distFalloffEndDistance\" \"10\"\n\"falloffBeginColor\" \"1.000000 1.000000 1.000000 1.000000\"\n\"falloffEndColor\" \"0.500000 0.500000 0.500000 0.500000\"\n\"texScroll\" \"0\"\n\"detailScaleX\" \"8\"\n\"detailScaleY\" \"8\"\n\"envMapMin\" \"0.2\"\n\"envMapMax\" \"1\"\n\"envMapExponent\" \"2.5\"\n\"useLegacyNormalEncoding\" \"0\"\n\"sort\" \"<default>*\"\n\"customTemplate\" \"\"\n\"customString\" \"\"\n\"colorTint\" \"1.000000 1.000000 1.000000 1.000000\"\n\"colorMap\" \""+"texture_assets\\\quake3\\\\"+array_final_list[i]+".jpg"+"\"\n\"detailMap\" \"\"\n\"normalMap\" \"\"\n\"specColorMap\" \"\"\n\"cosinePowerMap\" \"\"\n\"specColorStrength\" \"100\"\n\"cosinePowerStrength\" \"100\"\n\"tileColor\" \"tile both*\"\n\"tileNormal\" \"tile both*\"\n\"tileSpecular\" \"tile both*\"\n\"filterColor\" \"mip standard (2x bilinear)*\"\n\"filterDetail\" \"mip standard (2x bilinear)*\"\n\"filterNormal\" \"mip standard (2x bilinear)*\"\n\"filterSpecular\" \"mip standard (2x bilinear)*\"\n\"nopicmipColor\" \"0\"\n\"nopicmipDetail\" \"0\"\n\"nopicmipNormal\" \"0\"\n\"nopicmipSpecular\" \"0\"\n\"noStreamColor\" \"0\"\n\"tessSize\" \"0\"\n\"textureAtlasRowCount\" \"1\"\n\"textureAtlasColumnCount\" \"1\"\n\"distortionScaleX\" \"0.5\"\n\"distortionScaleY\" \"0.5\"\n\"distortionColorBehavior\" \"scales distortion strength*\"\n\"waterMapTextureWidth\" \"64\"\n\"waterMapHorizontalWorldLength\" \"37\"\n\"waterMapVerticalWorldLength\" \"37\"\n\"waterMapWindSpeed\" \"76\"\n\"waterMapWindDirectionX\" \"1\"\n\"waterMapWindDirectionY\" \"0\"\n\"waterMapAmplitude\" \"0.06\"\n\"waterColorR\" \"0.2\"\n\"waterColorG\" \"0.3\"\n\"waterColorB\" \"0.4\"\n\"formatColor\" \"<auto compression>*\"\n\"formatDetail\" \"<auto compression>*\"\n\"formatSpecular\" \"<auto compression>*\"\n\"formatNormal\" \"<auto compression>*\"\n\"blendFunc\" \"Replace*\"\n\"customBlendOpRgb\" \"Add*\"\n\"customBlendOpAlpha\" \"Add*\"\n\"srcCustomBlendFunc\" \"One*\"\n\"destCustomBlendFunc\" \"One*\"\n\"srcCustomBlendFuncAlpha\" \"One*\"\n\"destCustomBlendFuncAlpha\" \"One*\"\n\"alphaTest\" \"Always*\"\n\"depthTest\" \"LessEqual*\"\n\"depthWrite\" \"<auto>*\"\n\"cullFace\" \"Back*\"\n\"polygonOffset\" \"None*\"\n\"showAdvancedOptions\" \"<none>*\"\n\"colorWriteRed\" \"Enable\"\n\"colorWriteGreen\" \"Enable\"\n\"colorWriteBlue\" \"Enable\"\n\"colorWriteAlpha\" \"Enable\"\n\"stencilOpFail1\" \"Keep\"\n\"stencilOpZFail1\" \"Keep\"\n\"stencilOpPass1\" \"Keep\"\n\"stencilOpFail2\" \"Keep\"\n\"stencilOpZFail2\" \"Keep\"\n\"stencilOpPass2\" \"Keep\"\n\"stencilFunc1\" \"Always\"\n\"stencilFunc2\" \"Always\"\n\"stencil\" \"Disable\"\n}\n"
        i += 1

    gdt_file_name = filename.replace('.map','.gdt')

    h = open(gdt_file_name,"w")
    h.write("{\n"+gdt_list+"\n}")
    h.close
    
    bat_file_name = filename.replace('.map','.bat')

    i = 0

    while i < array_size:
        batch_string += "converter -nocachedownload -single material "+array_final_list[i]+"\n"
        i += 1

    print('Generate Batch...')

    b = open(bat_file_name,"w")
    b.write("@ECHO OFF\n"+batch_string+"\npause")
    b.close

    f.close


def cod4_conv(filename):

    dir_path_root = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path_root)

    global path
    global loop

    loop = True
    path = dir_path_root + "\\" + filename

    few_lines_fix(path)

    print('Removing patchdefs...')

    while loop:
        remove_patchdef(path)

    print('Fixing UVs...')
    fix_uv(path)

    print('Fixing materials...')
    fix_materials(path)

    print('Generate GDT...')
    make_gdt(path,filename)

def main():

    global dir_path_root
    dir_path_root = os.path.dirname(os.path.realpath(__file__))

    print('')
    print('#####################################')
    print('          Q3 Bsp -- > Q3 Map')
    print('#####################################')
    print('')
    time.sleep(1)

    os.chdir(dir_path_root+"/bsp")

    for file in glob.glob("*.bsp"):
        q3map2(file)

    os.chdir(dir_path_root)

    print('')
    print('#####################################')
    print('          Q3 Map -- > CoD4 Map')
    print('#####################################')
    print('')
    time.sleep(1)

    os.chdir(dir_path_root+"/out")

    for file in glob.glob("*.map"):
        cod4_conv(file)

    print('\nDone!\n')
    print("Press any key to continue...")
    msvcrt.getch()

main()