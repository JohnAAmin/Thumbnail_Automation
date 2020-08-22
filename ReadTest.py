# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:08:02 2020

@author: John Amin
"""
import yaml
import os

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
    print("SELECTED FILE: {}".format(thumbnail_list))
    return thumbnail_list

def main(*arg):
    if arg == None:
        file_name = fileselect()
    else:
        file_name = arg[0]

    roster_dict = "Roster.yaml"
    name, x = file_name.split('.')

    with open(file_name) as file:
          Entry = yaml.load(file, Loader=yaml.FullLoader)
    
    with open(roster_dict) as file:
          Roster = yaml.load(file, Loader=yaml.FullLoader)
    
    pics = Entry["Thumbnails"]
    chars = Roster["Roster"]

    for key, val in pics.items():
        try:
            # print(type(str(val['P1']))) # debug code to check data type
            val['C1'] = chars[val['C1']]
            val['C2'] = chars[val['C2']]
            
            print("\tThumbnail Good: {}".format(key))
        except KeyError:
            print("\tBad Character Name. Skipping Thumbnail: {}".format(key))
        except:
            print("\tEditing Error")

if __name__ == "__main__":
    main()
