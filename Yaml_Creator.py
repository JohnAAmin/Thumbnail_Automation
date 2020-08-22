# -*- coding: utf-8 -*-
"""
Thumbnail Title Reader

@author: johna
"""
import yaml
from ReadTest import main as checker
from Thumbnail_Automation import main as thumbnails
#-----------------------------------------------------------------------------#
# Place Match Titles Here:
thumbnail_list = '''
PSC LCQ

Pools WR1 Mir4ge (Luigi) vs Frog (Sonic) (Peak LCQ)
Pools WR2 Zador (Mega Man) vs Manny (Lucas) (Peak LCQ)
Pools WQ Scarlat (Sonic) vs Monteant (G&W) (Peak LCQ)
Pools WSF Coffee (Bowser) vs DeWarioFreak (Snake) (Peak LCQ)
Pools WSF Big Nibble (ROB) vs Nub (Captain Falcon) (Peak LCQ)
Top 24 WQ Kabi (Hero) vs Capitancito (Cloud) (Peak LCQ)
Top 24 WQ GordoLad (King Dedede) vs Monteant (G&W) (Peak LCQ)
Top 24 WSF Kabi (Hero) vs MJI (Joker) (Peak LCQ)
Top 24 WSF Monteant (G&W) vs NUB (Roy) (Peak LCQ)
Top 24 WF Kabi (Hero) vs Monteant (G&W) (Peak LCQ)
Top 24 LQ Coffee (Bowser) vs Nub (Captain Falcon) (Peak LCQ)
Top 24 LSF Zador (Mega Man) vs Coffee (Bowser) (Peak LCQ)
Top 24 LF Zador (Mega Man) vs Kabi (Hero) (Peak LCQ)
Top 24 GF Monteant (G&W) vs Kabi (Hero) (Peak LCQ)

'''
#-----------------------------------------------------------------------------#
sep = "- - - - - - - - - - - - - - - - - - - - "
print('\n' + sep)
print("Generating Thumbnail Yaml")
tlist = thumbnail_list.split('\n')

count = 1
dx = {}; d = {};
for name in tlist:
    try:
        if (name == '') or (len(name.split()) < 4):
            pass
        elif ("Pools" in name) or ("Top" in name):
            Rx = 0              # Number of words in Round "Pools"/"Top"
            if ("Pools" in name):
                Rx = 2
            elif("Top" in name):
                Rx = 3           
            data = name.split()
            
            # Gets Round Name
            R = ' '.join(data[0:Rx])
            
            pOpen =  [x for x in data if '(' in x]
            pClose = [x for x in data if ')' in x]
            
            io1 = [i for i, x in enumerate(data) if pOpen[0] in x][0]
            ic1 = [i for i, x in enumerate(data) if pClose[0] in x][0]
            
            io2 = [i for i, x in enumerate(data) if pOpen[1] in x][0]
            ic2 = [i for i, x in enumerate(data) if pClose[1] in x][0]
            
            # Gets Player 1 Name
            P1 = ' '.join(data[Rx:io1])
            # Gets Character 1 Name
            if io1 == ic1:
                C1 = data[io1][1:-1]
            else:
                C1 = ' '.join(data[io1:ic1+1])[1:-1]
                C1 = C1.split(' / ')[0]
            
            # Gets Player 2 Name        
            P2 = ' '.join(data[ic1+2:io2])
            # Gets Character 2 Name
            if io2 == ic2:
                C2 = data[io2][1:-1]
            else:
                C2 = ' '.join(data[io2:ic2+1])[1:-1]
                C2 = C2.split(' / ')[0]
            
            # Gets Tourney Name
            T =  ' '.join(data[ic2+1:])[1:-1]
            
            #print(R,P1,C1,P2,C2,T)
            d[count] = {'R':R, 'T':T, 'P1':P1,'C1':C1, 'P2':P2, 'C2':C2}
            count += 1
        else:
            print("Error on Line: {}".format(count))
            count += 1
    except:
        print("Parsing Error on line: {}".format(count))
        count += 1
        
#Creates the Thumbnail Dictionary
dx = {'Thumbnails': d}

# Creates Filename and Exports Yaml
fn = T.replace(' ','_') + '.yaml'
with open(fn, 'w') as file:
    yaml.dump(dx, file)
print("Exporting Yaml as File: {}".format(fn))

# Runs the Yaml ReadTest Checker
print(sep)
print("Running Read Test")
checker(fn)
print("Read Test Complete")

# Asks if it should run Thumbnail Generator (PS)
print(sep)
print("Thumbnail Generator")
waiting = True
while waiting:
    out = input("Run Thumbnail Generator? [y/n]: ")
    out = str(out)
    if out == 'y' or out == 'Y':
        thumbnails(fn)
        waiting = False
    elif out == 'n' or out == 'N':
        print("Will NOT run Thumbnail Generator\n")
        print("If correcting yaml, run ReadTest.py and Thumbnail_Automation.py afterwards")
        waiting = False
    else:
        print("Unrecognized Command.\nPlease respond with either 'y' or 'n'")
print(sep)
print("Task Complete!")
