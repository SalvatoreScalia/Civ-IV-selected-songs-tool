import re as RE
from xml.etree import ElementTree as ET
import os as OS
import tkinter as tk


#constant of xml of game
ns_civ4erainfos = '{x-schema:CIV4GameInfoSchema.xml}' #namespace for civ4erainfos.xml
ns_audio2dscripts = '{x-schema:AudioScriptSchema.xml}'
ns_audiodefines = '{x-schema:AudioDefinesSchema.xml}'
pref_civ4erainfos = 'AS2D_'
pref_audiodefines = 'SONG_'
song_tag = 'EraInfoSoundtrack'
declaration_and_comment_civ4erainfos = f"<?xml version=\"1.0\"?>\n<!-- python script by Salvatore Scalia https://github.com/SalvatoreScalia/Civ-IV-selected-songs-tool -->\n<!-- edited with XMLSPY v2004 rel. 2 U (http://www.xmlspy.com) by Alex Mantzaris (Firaxis Games) -->\n<!-- Sid Meier's Civilization 4 -->\n<!-- Copyright Firaxis Games 2005 -->\n<!-- -->\n<!-- EraInfo - This structure describes the name and soundtracks for each era. -->\n<!-- -->\n<!-- MODDERS: Removing ERA's can cause problems if you are not careful. If you must remove them, you need to do the following: -->\n<!-- 1. Clean up the references to the ERA's in CIV4BuildingInfos -->\n<!-- 2. Clean up the references to the ERA's in CIV4TechInfos -->\n<!-- 3. Clean up the references to the ERA's in CIV4LeaderHeadInfos -->\n<!-- 4. Clean up the references to the ERA's in CIV4CityLSystem -->\n<!-- 5. Clean up the references to the ERA's in CIV4PlotLSystem -->\n<!-- Good luck! -->\n"
declaration_and_comment_audiodefines = f"<?xml version=\"1.0\"?>\n<!-- python script by Salvatore Scalia https://github.com/SalvatoreScalia/Civ-IV-selected-songs-tool -->\n<!-- edited with XMLSPY v2004 rel. 2 U (http://www.xmlspy.com) by Dean Ray Johnson (Firaxis Games) -->\n<!-- Sid Meier's Civilization 4 -->\n<!-- Copyright Firaxis Games 2005 -->\n<!-- -->\n<!-- AudioDefines -->\n"
declaration_and_comment_audio2dscripts = f"<?xml version=\"1.0\"?>\n<!-- python script by Salvatore Scalia https://github.com/SalvatoreScalia/Civ-IV-selected-songs-tool -->\n<!-- edited with XMLSpy v2005 rel. 3 U (http://www.altova.com) by Soren Johnson (Firaxis Games) -->\n<!-- edited with XMLSPY v2004 rel. 2 U (http://www.xmlspy.com) by Michael Curran (Firaxis Games) -->\n<!-- Sid Meier's Civilization 4 -->\n<!-- Copyright Firaxis Games 2005 -->\n<!-- -->\n<!-- 2D Sound Scripts -->\n"
#quantity of folder
epocas = ["Ancient","Classical","Medieval","Renaissance","Industrial","Modern","Future"]
#directory of folder
directoy_civ4erainfos = "\XML\GameInfo\CIV4EraInfos.xml"
directory_audio2dscripts = "\XML\Audio\Audio2DScripts.xml"
directory_audiodefines = "\XML\Audio\AudioDefines.xml"

#space between buttons
space_buttons = 50

#Correct path of CIV4-Selected-Songs
incorrectpath = False

#--------------------------------Script------------------------------------#
def print_all_songs():#list with all songs in xml
    for i in range(len(root_civ4erainfos[0])):
        name = root_civ4erainfos[0][i][0].text
        size = len(root_civ4erainfos[0][i][31])
        print('_____________________________')
        print('Name: ' + name)
        print('Size: ' +str(size))
        for x in root_civ4erainfos[0][i][31]:
            print(x.text)

def refactor_name_file(name_file):
    name = OS.path.splitext(name_file)[0]
    refactor_name = RE.sub(r"[^a-zA-Z0-9]", "", str(name)) # Remove Special Characters from a String Using re.sub()
    return refactor_name.upper()

def refactor_xml_element(script_id,sound_id):
    return f'<Script2DSound> <ScriptID>{script_id}</ScriptID> <SoundID>{sound_id}</SoundID> <SoundType>GAME_MUSIC</SoundType> <iMinVolume>70</iMinVolume> <iMaxVolume>70</iMaxVolume> <iPitchChangeDown>0</iPitchChangeDown> <iPitchChangeUp>0</iPitchChangeUp> <iMinLeftPan>-1</iMinLeftPan> <iMaxLeftPan>-1</iMaxLeftPan> <iMinRightPan>-1</iMinRightPan> <iMaxRightPan>-1</iMaxRightPan> <bLooping>0</bLooping> <iMinTimeDelay>0</iMinTimeDelay> <iMaxTimeDelay>0</iMaxTimeDelay> <bTaperForSoundtracks>0</bTaperForSoundtracks> <iLengthOfSound>0</iLengthOfSound> <fMinDryLevel>1.0</fMinDryLevel> <fMaxDryLevel>1.0</fMaxDryLevel> <fMinWetLevel>0.0</fMinWetLevel> <fMaxWetLevel>0.0</fMaxWetLevel> <iNotPlayPercent>0</iNotPlayPercent> </Script2DSound>'

def list_songs(era_folder): #list of dictory and files in the soundtrack\era_folder
    try: 
        list_of_songs = OS.listdir(OS.getcwd() + '\Sounds\Soundtrack' + chr(92) + era_folder)
        return list_of_songs
    except Exception as e:
        print('the folder ' + era_folder + ' not found!')
        print(e)
        return False

def write_xml_civ4erainfos(era_folder):
    try:
        list_of_songs = list_songs(era_folder=era_folder)
        if list_of_songs == False:
            return False
        if len(epocas) != len(root_civ4erainfos[0]):
            print('there are tags in CIV4EraInfos.xml missing')
            return False
        else:
            # get the index of era_folder
            index = epocas.index(era_folder)
            if root_civ4erainfos[0][index][31].tag == (ns_civ4erainfos + 'EraInfoSoundtracks'):
                #clear songs
                root_civ4erainfos[0][index][31].clear()
                #new songs
                for song in list_of_songs:
                    new_song = ET.Element(song_tag)
                    new_song.text = pref_civ4erainfos + refactor_name_file(song)
                    root_civ4erainfos[0][index][31].append(new_song)
            else:
                print("The tag EraInfoSoundtracks not found. Tag: "+root_civ4erainfos[0][index][31].tag)
                return False
    except Exception as e:
        print('Something went wrong when append the new songs in root infogame.')
        print(e)
        return False
    try:
        ET.indent(tree_civ4erainfos)
        ET.register_namespace('',"x-schema:CIV4GameInfoSchema.xml")
        xmlstr_civ4erainfos = ET.tostring(root_civ4erainfos).decode()
        # Create a file with header + xmlstr
        with open(OS.getcwd() + directoy_civ4erainfos, "w", encoding='UTF-8') as out:
            out.write(declaration_and_comment_civ4erainfos + xmlstr_civ4erainfos)
        #tree_civ4erainfos.write(directory_get() + directoy_civ4erainfos, encoding='UTF-8', xml_declaration=True)
        return True
    except Exception as e:
        print("Something went wrong when writing to the file CIV4GameInfos.xml")
        print(e)
        return False

def write_xml_audiodefines(era_folder):
    try:
        list_of_songs = list_songs(era_folder=era_folder)
        #print('List of songs: '+ str(list_of_songs))
        if list_of_songs == False:
            return False
        for song in list_of_songs:
            dir_song = 'Sounds/Soundtrack/'+ era_folder + chr(47) + OS.path.splitext(song)[0]
            song_id = pref_audiodefines + refactor_name_file(song)
            write = True
            # print(len(root_audiodefines[0].findall(ns_audiodefines + 'SoundData')))
            # print(len(root_audiodefines[0].findall('SoundData')))
            for sounddata in root_audiodefines[0].findall('SoundData'):
                if sounddata.find('Filename').text == dir_song:
                    write = False
                    sounddata.find('SoundID').text = song_id
                    print(f'This song: "{song}" is already in the folder: {era_folder}')
            for sounddata in root_audiodefines[0].findall(ns_audiodefines + 'SoundData'):
                if sounddata.find(ns_audiodefines + 'Filename').text == dir_song:
                    write = False
                    sounddata.find(ns_audiodefines + 'SoundID').text = song_id
                    print(f'This song: "{song}" is already in the folder: {era_folder}. ns')
            if write:                    
                element = ET.Element('SoundData')
                se_songid = ET.SubElement(element, 'SoundID')
                se_filename = ET.SubElement(element, 'Filename')
                se_loadtype = ET.SubElement(element, 'LoadType')
                se_biscompressed = ET.SubElement(element, 'bIsCompressed')
                se_bingeneric = ET.SubElement(element, 'bInGeneric')
                se_songid.text = song_id
                se_filename.text = dir_song
                se_loadtype.text = 'STREAMED'
                se_biscompressed.text = '1'
                se_bingeneric.text = '1'
                root_audiodefines[0].append(element)
    except Exception as e:
        print('Something went wrong when append the new songs in root audiodefines.')
        print(e)
        return False
    try:
        ET.indent(tree_audiodefines)
        ET.register_namespace('',"x-schema:AudioDefinesSchema.xml")
        xmlstr_audiodefines = ET.tostring(root_audiodefines).decode()
        # Create a file with header + xmlstr
        with open(OS.getcwd() + directory_audiodefines, "w", encoding='UTF-8') as out:
            out.write(declaration_and_comment_audiodefines + xmlstr_audiodefines)
        #tree_audiodefines.write(directory_get() + directory_audiodefines, encoding='UTF-8', xml_declaration=True)
        return True
    except Exception as e:
        print("Something went wrong when writing to the file AudioDefines.xml")
        print(e)
        return False

def write_xml_audio2dscripts(era_folder):
    try:
        list_of_songs = list_songs(era_folder=era_folder)
        if list_of_songs == False:
            return False
        for song in list_of_songs:
            script_id = pref_civ4erainfos + refactor_name_file(song)
            sound_id = pref_audiodefines + refactor_name_file(song) 
            write = True
            for script2dsound in root_audio2dscripts.findall('Script2DSound'):
                if script2dsound.find('SoundID').text == sound_id and script2dsound.find('ScriptID').text == script_id:
                    write = False
                if (script2dsound.find('SoundID').text == sound_id) ^ (script2dsound.find('ScriptID').text == script_id):
                    root_audio2dscripts.remove(script2dsound)
            for script2dsound in root_audio2dscripts.findall(ns_audio2dscripts + 'Script2DSound'):
                if script2dsound.find(ns_audio2dscripts + 'SoundID').text == sound_id and script2dsound.find(ns_audio2dscripts + 'ScriptID').text == script_id:
                    write = False
                if (script2dsound.find(ns_audio2dscripts + 'SoundID').text == sound_id) ^ (script2dsound.find(ns_audio2dscripts + 'ScriptID').text == script_id):
                    root_audio2dscripts.remove(script2dsound)
            if write:
                refactor_str_audio2dscript = refactor_xml_element(script_id, sound_id)
                element = ET.fromstring(refactor_str_audio2dscript)
                root_audio2dscripts.append(element)
    except Exception as e:
        print(e)
        return False
    try:
        ET.indent(tree_audio2dscripts)
        ET.register_namespace('',"x-schema:AudioScriptSchema.xml")
        xmlstr_audio2dscript = ET.tostring(root_audio2dscripts).decode()
        # Create a file with header + xmlstr
        with open(OS.getcwd() + directory_audio2dscripts, "w", encoding='UTF-8') as out:
            out.write(declaration_and_comment_audio2dscripts + xmlstr_audio2dscript)
        #tree_audio2dscripts.write(directory_get() + directory_audio2dscripts, encoding='UTF-8', xml_declaration=True)
        return True
    except Exception as e:
        print("Something went wrong when writing to the file Audio2DScripts.xml")
        print(e)
        return False
#------------------------------------------------------------------------#

#--------------------------parsing directly------------------------------#
print("v1.0")
try:
    current_path = OS.getcwd()
    tree_civ4erainfos = ET.parse(current_path + directoy_civ4erainfos)
    root_civ4erainfos = tree_civ4erainfos.getroot()
    tree_audio2dscripts = ET.parse(current_path + directory_audio2dscripts)
    root_audio2dscripts = tree_audio2dscripts.getroot()
    tree_audiodefines = ET.parse(current_path + directory_audiodefines)
    root_audiodefines = tree_audiodefines.getroot()
except Exception as e:
    incorrectpath = True
    print(e)
#------------------------------------------------------------------------#

#------------------------------------Menu----------------------------------#
rootTK= tk.Tk()

rootTK.title('Civ IV selected songs')
canvas1 = tk.Canvas(rootTK, width = 430, height = 440)
canvas1.pack()

label1 = tk.Label(rootTK, text= 'Select the folder and load: ', fg='blue', font=('helvetica', 12, 'bold'))
canvas1.create_window(215, 30, window=label1)

#define buttons and functions
for x in range(len(epocas)):
    def action (epoca = epocas[x]):
        a = write_xml_civ4erainfos(epoca)
        b = write_xml_audiodefines(epoca)
        c = write_xml_audio2dscripts(epoca)
        if  a and b and c:
            label1 = tk.Label(rootTK, text='The files in the ' +epoca+ ' folder were added successfully!', fg='blue', font=('helvetica', 12, 'bold'))
            canvas1.create_window(215, 400, window=label1)
            print_all_songs()
        else:
            label1 = tk.Label(rootTK, text= '                Something went wrong in the process!!              ', fg='red', font=('helvetica', 12, 'bold'))
            canvas1.create_window(215, 400, window=label1)
    button = tk.Button(text=epocas[x], command=action, bg='brown',fg='white')
    #buttons.append(button)
    canvas1.create_window(215, 60 + x*space_buttons, window=button)
    if incorrectpath:
        label1 = tk.Label(rootTK, text= '           Ensure the program is running in the Assets folder!!            ', fg='red', font=('helvetica', 12, 'bold'))
        canvas1.create_window(215, 400, window=label1)

rootTK.mainloop()
#--------------------------------------------------------------------------#
#parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)) # Python 3.8
#print(ET.tostring(root_civ4erainfos,encoding='utf8',method='xml'))