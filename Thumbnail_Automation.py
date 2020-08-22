
"""
Created on Mon May  4 20:31:53 2020

@author: John Amin

TODO:

* Refactor code in a clean way
* Make callable from command prompt
* Control text size based on name length 
    
"""
# Imports

import yaml
import win32com.client
import time as t
import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

#File Locations
file = "Thumbnail_BG.psd"
PS_File = current_dir + "/Photoshop/" + file 

Exports_Folder = current_dir
#------------------------------------------------------------------------------
def fileselect():
    thumbnail_list = ""
    files = (os.listdir())
    for file in files:
        if os.path.isdir(file):
            continue
        else:
            name, ext = file.split('.')
            if ("Peak" in name) and ext == "yaml":
                thumbnail_list = file
    print("selected file: {}".format(thumbnail_list))
    return thumbnail_list
#------------------------------------------------------------------------------
def main(*arg):
    if arg == None:
        file_name = fileselect()
    else:
        file_name = arg[0]
    
    #USER BOOLS
    PNG = False  # export in PNG? Else JPEG
    qout = True  # Quits after Export
    
    roster_dict = "Roster.yaml"
    name, x = file_name.split('.')
    files = os.listdir()
    
    # Checks for Folder, or Generates if it doesn't exist
    if name in files:
        print('Folder "{}" already exists'.format(name))
    else:
        os.mkdir(name)
    Image_Folder = Exports_Folder + '/' + name + '/'
    
    # Opens and Loads the Thumbnail Yaml
    with open(file_name) as file:
         Entry = yaml.load(file, Loader=yaml.FullLoader)
    
    # Opens and Loads the Roster Dictionary
    with open(roster_dict) as file:
         Roster = yaml.load(file, Loader=yaml.FullLoader)

    pics = Entry["Thumbnails"]
    chars = Roster["Roster"]
    
    #------------------------------------------------------------------------------
    
    print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    start = t.time()
    print("Task Start:")
    #------------------------------------------------------------------------------
    #Test Data
    # testdict = {"T":"Peak #40",
    #             "R":"Top 16 GF",
    #             "P1":"J4m",
    #             "P2":"Jamin",
    #             "C1":"(1)-Mario.png",
    #             "C2":"(3)-Link.png"} 
    #------------------------------------------------------------------------------
    # Open Photoshop Template
    
    print("\tOpen Photoshop Template: ... ", end="")
    
    Template = PS_File
    psApp = win32com.client.Dispatch("Photoshop.Application")
    psApp.Open(Template)
    doc = psApp.Application.ActiveDocument
    
    A = round((t.time() - start), 1)
    print("{} s".format(A))
    #------------------------------------------------------------------------------
    # Perform Edits
    
    for key, val in pics.items():
        print("  Thumbnail: {}".format(key))
        try:
            val['C1'] = chars[val['C1']]
            val['C2'] = chars[val['C2']]
            testdict = pics[key]
        
        
            print("\tPerforming Edits: .......... ", end="")    
            
            Titles = doc.LayerSets["Titles"]
            Char1 = doc.LayerSets["Char1"]
            Char2 = doc.LayerSets["Char2"]
            
            Titles.ArtLayers["Player 1"].TextItem.contents = str(testdict["P1"])
            Titles.ArtLayers["Player 2"].TextItem.contents = str(testdict["P2"])
            Titles.ArtLayers["Round"].TextItem.contents = str(testdict["R"])
            Titles.ArtLayers["Tourney"].TextItem.contents = str(testdict["T"])
            
            Char1.ArtLayers[testdict["C1"]].Visible = True
            Char2.ArtLayers[testdict["C2"]].Visible = True
            
            B = round((t.time() - start), 1)
            print("{} s".format(B))
            #------------------------------------------------------------------------------
            # Export New Thumbnail
            print("\tExport New Thumbnail: ...... ", end="")
            
            options = win32com.client.Dispatch("Photoshop.ExportOptionsSaveForWeb")
            if PNG == True:
                options.Format = 13 # PNG
                options.PNG8 = True
                ext = ".png"
            else:
                options.Format = 6  #JPEG
                options.quality = 20 # 20% File sizes well under 1MB
                ext = ".jpeg"
            
            exportpath = Image_Folder
            exportname = "("+ str(key) +")" + str(testdict["P1"])+"_vs_"+str(testdict["P2"])
            exportname = exportname + ext
            
            exportfile = exportpath + exportname
            
            doc.Export(ExportIn=exportfile, ExportAs=2, Options=options)
            
            C = round((t.time() - start), 1)
            print("{} s".format(C))
            #------------------------------------------------------------------------------
            #Reset File
            print("\tReset Photoshop File: ...... ", end="")
            
            Char1.ArtLayers[testdict["C1"]].Visible = False
            Char2.ArtLayers[testdict["C2"]].Visible = False
            
            Titles.ArtLayers["Player 1"].TextItem.contents = "Player 1"
            Titles.ArtLayers["Player 2"].TextItem.contents = "Player 2"
            Titles.ArtLayers["Round"].TextItem.contents = "Round"
            Titles.ArtLayers["Tourney"].TextItem.contents = "Tourney"
            
            D = round((t.time() - start), 1)
            print("{} s".format(D))
            
        except KeyError:
            print('\tBad Character Name. Skipping Thumbnail')
    #    except:
    #        print("\tError editing photoshop file.", end="")
    #------------------------------------------------------------------------------
    
    # Task Complete
    if qout:
        doc.Close(2)
        psApp.Quit()

    print("Task Complete: .................. {} s".format(D))
    print(" - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    
if __name__ == "__main__":
    main()