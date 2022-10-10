import re as RE
from xml.etree import ElementTree as ET
import os as OS
import tkinter as tk


#constant of xml of game
ns = '{x-schema:CIV4GameInfoSchema.xml}' #namespace
pref_gameinfo = 'AS2D_'
pref_audiodefines = 'SONG_'
song_tag = 'EraInfoSoundtrack'
#quantity of folder
epocas = ["Ancient","Classical","Medieval","Renaissance","Industrial","Modern","Future"]
#space between buttons
space_buttons = 50 

#--------------------------------Script------------------------------------#
#list with all songs in xml
def print_all_songs():
    for i in range(len(root_gameinfo[0])):
        name = root_gameinfo[0][i][0].text
        size = len(root_gameinfo[0][i][31])
        print('_____________________________')
        print('Name: ' + name)
        print('Size :' +str(size))
        for x in root_gameinfo[0][i][31]:
            print(x.text)

def directory_get():
    #path of files
    path = path = OS.getcwd()
    #print(path)
    return path

def list_of_songs_get(era_folder):
    #list of dictory and files in the soundtrack\era_folder
    try:
        list_of_songs = OS.listdir(directory_get() + '\Sounds\Soundtrack' + chr(92) + era_folder)
        #print(list_of_songs)
        return list_of_songs
    except:
        print('the folder ' + era_folder + ' not found!')
        return False

def write_xml_gameinfo(era_folder):
    list_of_songs = list_of_songs_get(era_folder=era_folder)
    if list_of_songs == False:
        return False
    try:
        if len(epocas) != len(root_gameinfo[0]):
            print('there are tags in CIV4EraInfos.xml missing')
            return False
        else:
            # get the index of era_folder
            index = epocas.index(era_folder)
            if root_gameinfo[0][index][31].tag == (ns + 'EraInfoSoundtracks'):
                #clear songs
                root_gameinfo[0][index][31].clear()
                #new songs
                for song in list_of_songs:
                    name_song = OS.path.splitext(song)[0] 
                    refactor_name = RE.sub(r"[^a-zA-Z0-9]", "", str(name_song))     # Remove Special Characters from a String Using re.sub()           
                    new_song=ET.Element(song_tag)
                    new_song.text= pref_gameinfo + refactor_name.upper()
                    root_gameinfo[0][index][31].append(new_song)
            else:
                print("The tag EraInfoSoundtracks not found. Tag: "+root_gameinfo[0][index][31].tag)
                return False
    except:
        print('Something went wrong when append the new songs in root infogame.')
        return False
    try:
        ET.register_namespace('',"x-schema:CIV4GameInfoSchema.xml")
        tree_gameinfo.write('output_gi.xml')
        #print_all_songs()
        return True
    except:
        print("Something went wrong when writing to the file CIV4GameInfos.xml")
        return False

def write_xml_audiodefines(era_folder):
    try:
        list_of_songs = list_of_songs_get(era_folder=era_folder)
        print(list_of_songs)
        for song in list_of_songs:
            element = ET.Element('SoundData')
            name_file = OS.path.splitext(song)[0] 
            refactor_name_file = RE.sub(r"[^a-zA-Z0-9]", "", str(name_file)) # Remove Special Characters from a String Using re.sub()
            song_id = pref_audiodefines + refactor_name_file.upper()
            se_songid = ET.SubElement(element, 'SoundID')
            se_filename = ET.SubElement(element, 'Filename')
            se_loadtype = ET.SubElement(element, 'LoadType')
            se_biscompressed = ET.SubElement(element, 'bIsCompressed')
            se_bingeneric = ET.SubElement(element, 'bInGeneric')
            se_songid.text = song_id
            se_filename.text = '\Sounds\Soundtrack' + chr(92) + era_folder + chr(92) + name_file
            se_loadtype.text = 'STREAMED'
            se_biscompressed.text = '1'
            se_bingeneric.text = '1'
            # print(ET.tostring(element,encoding="unicode"))
            root_audiodefines[0].append(element)
    except:
        print('Something went wrong when append the new songs in root audiodefines.')
        return False
    try:
        ET.register_namespace('',"x-schema:AudioDefinesSchema.xml")
        tree_audiodefines.write('output_ad.xml')
        return True
    except:
        print("Something went wrong when writing to the file AudioDefines.xml")
        return False
def write_xml_audio2dscripts():
    return False
#------------------------------------------------------------------------#

#--------------------------parsing directly------------------------------#
tree_gameinfo = ET.parse(directory_get() + '\XML\GameInfo\CIV4EraInfos.xml')
root_gameinfo = tree_gameinfo.getroot()
tree_audio2dscripts = ET.parse(directory_get() + '\XML\Audio\Audio2DScripts.xml')
root_audio2dscripts = tree_audio2dscripts.getroot()
tree_audiodefines = ET.parse(directory_get() + '\XML\Audio\AudioDefines.xml')
root_audiodefines = tree_audiodefines.getroot()
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
        a = write_xml_gameinfo(epoca)
        b = write_xml_audiodefines(epoca)
        if  a and b:
            label1 = tk.Label(rootTK, text='The files in the ' +epoca+ ' folder were added successfully!', fg='blue', font=('helvetica', 12, 'bold'))
            canvas1.create_window(215, 400, window=label1)
        else:
            label1 = tk.Label(rootTK, text= '                Something went wrong in the process!!              ', fg='red', font=('helvetica', 12, 'bold'))
            canvas1.create_window(215, 400, window=label1)
    button = tk.Button(text=epocas[x], command=action, bg='brown',fg='white')
    #buttons.append(button)
    canvas1.create_window(215, 60 + x*space_buttons, window=button)

rootTK.mainloop()

#--------------------------------------------------------------------------#