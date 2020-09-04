# -*- coding: utf-8 -*-
"""
                         SMASH.GG STREAM TRACKER

This code is to track the matches in the stream queue in smash.gg This logs 
matches, telling us which games were played during a tournament afterwards.

@author: johna
"""
import os,sys
import json as js
import pandas as pd
import yaml
import time as t
from collections import Counter
from graphqlclient import GraphQLClient as GQL

'''
To do:
    1. set up correct round titles
    2. determine Tournament name appropriately
    3. set up the yaml creator
    4. set up peak tournament finder
'''


# USER Inputs

sets_file = "Peak_55_stream.txt"
slug = "tournament/10-peak-tournaments-ssbu-online-weekly-55-9-4-20"
caster = "peaktournaments"
auth_path = ""





def GQLclient(*path):
    ''' Opens Auth.yaml and starts GraphQL client '''
    
    # Sorts aurguments 
    if not path or not path[0]:
        path = os.getcwd()
    elif len(path) == 1:
        path = path[0]
    else:
        print('ERROR: Too many arguments')
        sys.exit(0)
        
    # Finds and reads auth.yaml file
    x = path + '/auth.yaml'
    with open(x) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        authToken = data.get('authkey')
    
    # Starts GraphQL file
    client = GQL('https://api.smash.gg/gql/' + 'alpha')
    client.inject_token('Bearer ' + authToken)
    return client
    
def characters():
    ''' loads a yaml with a characters dictionary to decode smash.gg Ids '''
    # Loads yaml in current directory
    path = os.getcwd()
    x = path + '/Character_Codes.yaml'
    with open(x) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data['Characters']

def peak_tourneys(client, owner_id):
    ''' Finds and supplies upcoming peak tournaments and slugs '''

    result = client.execute('''
            query TournamentsByOwner($ownerId: ID!) {
	         tournaments(query: {perPage: 5
	         filter: {ownerId: $ownerId}}) {
	           nodes {id name state slug 
                streamQueue{stream{streamSource streamName}}
		          events {id numEntrants state}
              }}}''', {"ownerId": owner_id})                 # Jamin - 301126
    resData = js.loads(result)
    Tourney = resData['data']['tournaments']['nodes']
    Tourney_dfs = pd.DataFrame(Tourney)
    Active_Tourneys = Tourney_dfs[Tourney_dfs.state == 2]
    #
    # Get Sets List from tournament
    #
    return Active_Tourneys



def select_tourney(client, slug, caster, set_list):
    ''' Finds tourneys based on slug and streams by caster '''
    # Makes request to smash.gg API
    result = client.execute('''
            query StreamQueueOnTournament($tourneySlug: String!)
            {tournament(slug: $tourneySlug){events{state} streamQueue 
            {stream {streamSource streamName} sets {id}}}}''',
            {"tourneySlug": slug})
    resData = js.loads(result)
    # Determines tournament state and finds StreamQueue
    state = resData['data']['tournament']['events'][0]['state']
    streamQueue = resData['data']['tournament']['streamQueue']
    print("Stream State: {}    Steam Queue: {}". format(state, streamQueue))
    if not streamQueue:
        return set_list, state
    else:
        for stream in streamQueue:
            if stream['stream']['streamName'] == caster:
                for sets in stream['sets']:
                    set_list.append(str(sets['id']))
        return set_list, state

#-----------------------------------------------------------------------------#
# Main Script - User Inputs
def stream_scout(client, state):    

    # Creates Set file if doesn't exist 
    files = os.listdir()
    if sets_file not in files:
        f = open(sets_file, 'w')
        f.close()

    # Loop runs until tournament ends 
    while state == 'ACTIVE':
        with open(sets_file, 'r') as f:
            sets = f.readlines()
            if not sets:
                saved_sets = sets
            else:
                saved_sets = sets[0].split(',')

        # Runs "select_tourney" 
        sets_list, state = select_tourney(client, slug, caster, saved_sets)        

        # Writes the new set of sets to the Set File as a csv 
        with open(sets_file, 'w') as f:
            x = set(sets_list)
            if len(x) < 1:
                f.write(str(x))
            else:
                f.write(','.join(x))
                
        # Waits before itterating loop
        print(x)
        tstart = t.time()
        timer = 0
        while timer < 2:
            tend = t.time()
            timer = round((tend-tstart),0)
            if (timer % 1) == 0:
                print(timer)
            t.sleep(1)
    
    # Once tournament ends
    chars_dict = characters()
    
    with open(sets_file, 'r') as f:
            streamed_sets = f.readlines()
            sets_list = streamed_sets[0].split(',')    
    
    for sets in sets_list:
        find_set(client,chars_dict,sets)
    
#-----------------------------------------------------------------------------#
def find_set(client, char_dict, set_id):

    result = client.execute('''
                query EventSets($setId: ID!) {set(id:$setId){
                games{selections {selectionType selectionValue
                entrant{id}}}slots{entrant{id name}}}}''',
                {"setId":set_id})    
    
    resData = js.loads(result)
    players = resData['data']['set']['slots']
    games = resData['data']['set']['games']
    
    if games == None:
        print('- - - - - -')
        print('No Games - DQ')
        return []
    else:
        
        ids = [];    names = [];
        for player in players:
            ids.append(player['entrant']['id'])
            names.append(player['entrant']['name'])
        
        player1 = [];  player2 = []
        for game in games:
    
            p1 = game['selections'][0]['entrant']['id']
            cc1 = game['selections'][0]['selectionValue']
            c1 = char_dict[cc1]
            
            p2 = game['selections'][1]['entrant']['id']
            cc2 = game['selections'][1]['selectionValue']
            c2 = char_dict[cc2]
            
            if p1 == ids[0]:
                player1.append(c1)
                player2.append(c2)
            elif p2 == ids[0]:
                player1.append(c2)
                player2.append(c1)
        
        print('- - - - - -')
        print(names[0],player1,' VS ',names[1],player2)
        p1 = names[0]
        p2 = names[1]
        c1 = Counter(player1).most_common(1)[0][0]
        c2 = Counter(player2).most_common(1)[0][0]
        print(p1,'-',c1, ' VS ', p2,'-',c2)
        
        lst = [p1, p2, c1, c2,]
        
        return lst
    
def yaml_creator(d):
    dx = {'Thumbnails': d}
    return dx

#-----------------------------------------------------------------------------#

def main():
    # MAIN SHOULD BE HERE!
    client = GQLclient()
    char_dict = characters()
    
    with open(sets_file, 'r') as f:
        sets = f.readlines()
        sets_list = sets[0].split(',')
        
    for s in sets_list:
        print(s)
        find_set(client,char_dict,s)

#-----------------------------------------------------------------------------#

if __name__ == "__main__":
    client = GQLclient(auth_path)
    state = 'ACTIVE'
    stream_scout(client, state)
