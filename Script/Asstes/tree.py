import re as RE
from xml.etree import ElementTree as ET
import os as OS
import tkinter as tk

#namespace
ns = '{x-schema:CIV4GameInfoSchema.xml}'
#tag for add songs
song_tag = 'EraInfoSoundtrack'
#constant of xml of game
pref = 'AS2D_'
#quantity of folder
epocas = ["Ancient","Classical","Medieval","Renaissance","Industrial","Modern","Future"]
space_buttons = 50 #space between buttons

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

def write_xml_gameinfo(list_of_songs,era_folder):
    if len(root_gameinfo[0]) != len(epocas):
        print("tag_era are missing, the tag_era found are:")
        for tag_EraInfo in root_gameinfo[0]:
            print(tag_EraInfo[0].text)                
    else:
        # get the index of era_folder
        index = epocas.index(era_folder)
        if root_gameinfo[0][index][31].tag == (ns + 'EraInfoSoundtracks'):
            #clear songs
            for element in root_gameinfo[0][index][31]:
                root_gameinfo[0][index][31].remove(element)
                print(root_gameinfo[0][index][31].tag)
                print(len(root_gameinfo[0][index][31]))
            #new songs
            for song in list_of_songs:
                name_song = OS.path.splitext(song)[0] 
                refactor_name = RE.sub(r"[^a-zA-Z0-9]", "", str(name_song))     # Remove Special Characters from a String Using re.sub()           
                new_song=ET.Element(song_tag)
                new_song.text= pref + refactor_name.upper()
                root_gameinfo[0][index][31].append(new_song)
        else:
            print("EraInfoSoundtracks not found")
    try:
        ET.register_namespace('',"x-schema:CIV4GameInfoSchema.xml")
        tree_gameinfo.write('output.xml')
        #print_all_songs()
    except:
        print("Something went wrong when writing to the file")

 
def directory():
    #path of files
    path = path = OS.getcwd()
    #print(path)
    return path

def list_of_songs_get(era_folder):
    #arr of dictory and files in the soundtracks folder
    list_of_songs = OS.listdir(directory() + '\Asstes\Sounds\Soundtracks' + chr(92) + era_folder)
    print(list_of_songs)
    return list_of_songs
#------------------------------------------------------------------------#

#--------------------------parsing directly------------------------------#
tree_gameinfo = ET.parse(directory() + '\Asstes\XML\GameInfo\CIV4EraInfos.xml')
root_gameinfo = tree_gameinfo.getroot()
tree_audio2dscripts = ET.parse(directory() + '\Asstes\XML\Audio\Audio2DScripts.xml')
root_audio2dscripts = tree_audio2dscripts.getroot()
tree_audiodefines = ET.parse(directory() + '\Asstes\XML\Audio\AudioDefines.xml')
root_audiodefines = tree_audiodefines.getroot()
#------------------------------------------------------------------------#

#------------------------------------Menu----------------------------------#
rootTK= tk.Tk()

rootTK.title('Civ IV selected songs')
canvas1 = tk.Canvas(rootTK, width = 500, height = 600)
canvas1.pack()

label1 = tk.Label(rootTK, text= 'Select the folder and load: ', fg='blue', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 50, window=label1)

#define buttons and functions
for x in range(len(epocas)):
    def action (epoca = epocas[x]):
        label1 = tk.Label(rootTK, text= epoca, fg='blue', font=('helvetica', 12, 'bold'))
        canvas1.create_window(150, 550, window=label1)
        write_xml_gameinfo(list_of_songs_get(epoca),epoca)
    button = tk.Button(text=epocas[x], command=action, bg='brown',fg='white')
    #buttons.append(button)
    canvas1.create_window(150, 150 + x*space_buttons, window=button)

rootTK.mainloop()

#--------------------------------------------------------------------------#