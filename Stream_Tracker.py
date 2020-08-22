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
from graphqlclient import GraphQLClient as GQL


# USER Inputs

sets_file = 'Peak_53_Streams.txt'
slug = "tournament/10-peak-tournaments-ssbu-online-weekly-53-8-21-20"
caster = 'peaktournaments'
 





def GQLclient(*path):
    ''' Opens Auth.yaml and starts GraphQL client '''
    if not path:
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
    path = os.getcwd()
    x = path + '/Character_Codes.yaml'
    with open(x) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data

def stream_scout(client, owner_id):

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
    result = client.execute('''
            query StreamQueueOnTournament($tourneySlug: String!)
            {tournament(slug: $tourneySlug) {state streamQueue 
            {stream {streamSource streamName} sets {id}}}}''',
            {"tourneySlug": slug})
    resData = js.loads(result)
    state = resData['data']['tournament']['state']
    streamQueue = resData['data']['tournament']['streamQueue']
    for stream in streamQueue:
        if stream['stream']['streamName'] == caster:
            for sets in stream['sets']:
                set_list.append(str(sets['id']))
    return set_list, state

#-----------------------------------------------------------------------------#
# Main Script - User Inputs
def main(client, state):
    while state != 3:
    
        with open(sets_file, 'r') as f:
            sets = f.readlines()
            if not sets:
                saved_sets = sets
            else:
                saved_sets = sets[0].split(',')
            
            
        
        client = GQLclient()
        sets_list, state = select_tourney(client, slug, caster, saved_sets)
        
        with open(sets_file, 'w') as f:
            x = set(sets_list)
            if len(x) <= 1:
                f.write(x)
            else:
                f.write(','.join(x))
            
        print(x)
        tstart = t.time()
        timer = 0
        while timer < 10:
            tend = t.time()
            timer = round((tend-tstart),0)
            if (timer % 5) == 0:
                print(timer)
            t.sleep(1)
    
#-----------------------------------------------------------------------------#

def find_set(client, set_id):

    result = client.execute('''
                query EventSets($setId: ID!) {set(id:$setId){
                games{selections {selectionType selectionValue
                entrant{id}}}slots{entrant{id name}}}}''',
                {"setId":set_id})    
    
    resData = js.loads(result)
    players = resData['data']['set']['slots']
    games = resData['data']['set']['games']
    
    ids = [];    names = [];
    for player in players:
        ids.append(player['entrant']['id'])
        names.append(player['entrant']['name'])
    
    player1 = [];  player2 = []
    for game in games:
        p1 = game['selections'][0]['entrant']['id']
        c1 = game['selections'][0]['selectionValue']
        
        p2 = game['selections'][1]['entrant']['id']
        c2 = game['selections'][1]['selectionValue']
    
    return 1



client = GQLclient()
chars = characters()
find_set(client,31550094)
#-----------------------------------------------------------------------------#
""" 
result = client.execute('''
            query EventSets($eventId: ID!) {event(id: $eventId) {
            sets(sortType: STANDARD) {nodes {games {selections
              {selectionType selectionValue entrant {id}}} slots
              {entrant {id name}}}}}}''', {"eventId":event_id})                # Jamin - 301126
"""
#-----------------------------------------------------------------------------#
    
    
