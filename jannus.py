# imports
import dota2api
import json
import logging
import os
import re
import random
from progress.bar import Bar
import network
import numpy as np

#logger config
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = logging.getLogger('jannus')

#dota api initialisation
d2api = dota2api.Initialise('6FCA7ABF90D69EA8377C7991168FEF08')

def createFolder(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def deleteKey(leagueObj, key):
	del leagueObj[key]

def deletionKeyList():
	return {'description','itemdef','tournament_url'}

def matchAcquiringKeyList():
	return {'season',
	'radiant_win',
	'duration',
	'start_time',
	'match_id',
	'match_seq_num',
	'tower_status_radiant',
	'tower_status_dire',
	'barracks_status_radiant',
	'barracks_status_dire',
	'cluster',
	'cluster_name',
	'first_blood_time',
	'lobby_type',
	'lobby_name',
	'human_players',
	'leagueid',
	'positive_votes',
	'negative_votes',
	'game_mode',
	'game_mode_name',
	'radiant_captain',
	'dire_captain',
	'pick_bans'}

def saveLeagueIdAsKeyNameList():
	#getting leagues list
	leagues = d2api.get_league_listing()
	leagues = leagues['leagues']
	id_name_result = {}
	#removing unnecessary information
	for league in leagues:
		id_name_result[league['leagueid']] = league['name']
	#saving league data
	if not os.path.exists('../data'):
		os.makedirs('../data')
	with open('../data/league_id_as_key_name.txt', 'w') as league_file:
		json.dump(id_name_result, league_file)
		logging.info('Saving league_id_as_key_name.txt')

def getLeagueIdAsKeyNameList(id):
	#getting leagues list
	leagues = d2api.get_league_listing()
	leagues = leagues['leagues']
	id_name_result = {}
	#removing unnecessary information
	for league in leagues:
		if(league['leagueid'] == id):
			id_name_result = league['name']

	return id_name_result

def saveLeagueMatchesAsKeyId(league_num):
	#getting leagues list
	leagues = d2api.get_league_listing()
	leagues = leagues['leagues']
	print (len(leagues))
	league_pbar = Bar('League Progress', max = len(leagues))
	league_data_subset = []

	for num in range(league_num):
		league_data_subset.append(random.choice(leagues))

	match_dataset = []
	# getting all league matches
	for m in league_data_subset:
		l_id = m['leagueid']
		league_pbar.next()
		logger.info('\nChanging league...')
		league_matches = d2api.get_match_history(league_id = l_id)['matches']
		matches_pbar = Bar('Match Progress', max = len(league_matches))
		league_match_id = {}
		league_match_id['id'] = l_id
		league_match_id['matches'] = []
		#dropping unneccesary information from league matches
		keys_to_acquire = matchAcquiringKeyList();

		for lm in league_matches:
			matches_pbar.next()
			try:    
				league_match_id['matches'].append(str(lm['match_id']))
			except KeyError:
				logger.info('keyError' + str(l_id)  + '\t' + str(lm['match_id']))

		match_dataset.append(league_match_id)

	return(match_dataset)

#def getHeroNameWithIdList():


def saveMatchesAsKeyId(match_dataset):

	league_pbar = Bar('League Progress', max = len(match_dataset))

	picks_ban_data = []
	logger.info('\nLeague datatset %s', len(match_dataset))
	# getting all league matches
	for league_data in match_dataset:
		league_pbar.next()
		matches_pbar = Bar('Match Progress', max = len(league_data['matches']))
		for matchid in league_data['matches']:
			#logger.info(matches_in_league)
			try:
				match_json = d2api.get_match_details(match_id = matchid)
			except:
				pass

			matches_pbar.next()
			try:
				if(match_json['game_mode'] == 2):
					match = {}
					match['pb'] = match_json['picks_bans']                  
					match['radiant_win'] = match_json['radiant_win']
					picks_ban_data.append(match)
			except KeyError:
				logger.info('Picks ban not found for match id : %s', str(matchid))

	return picks_ban_data

def getMatchPicksBansAsTeams(match_details):    

	pick_ban_result = []

	for match_entry in match_details:
		match_pick_ban_element = {}
		match_pick_ban_element['radiant'] = {}
		match_pick_ban_element['dire'] = {}
		match_pick_ban_element['victory'] = match_entry['radiant_win']
		match_pick_ban_element['radiant']['picks'] = []
		match_pick_ban_element['radiant']['bans'] =  []
		match_pick_ban_element['dire']['picks'] = []
		match_pick_ban_element['dire']['bans'] = []
		for pick_bans in match_entry['pb']:
			#logger.info(pick_bans)
			#hero_element ={}
			if(pick_bans['team'] == 0):
				if(pick_bans['is_pick'] == True):
					#hero_element[str(pick_bans['hero_id'])] = pick_bans['order']
					match_pick_ban_element['radiant']['picks'].append(str(pick_bans['hero_id']))
			else:
				if(pick_bans['is_pick'] == True):
					#hero_element[str(pick_bans['hero_id'])] = pick_bans['order']
					match_pick_ban_element['dire']['picks'].append(str(pick_bans['hero_id']))

			if(pick_bans['team'] == 0):
				if(pick_bans['is_pick'] == False):
					#hero_element[str(pick_bans['hero_id'])] = pick_bans['order']
					match_pick_ban_element['radiant']['bans'].append(str(pick_bans['hero_id']))
			else:
				if(pick_bans['is_pick'] == False):
					#hero_element[str(pick_bans['hero_id'])] = pick_bans['order']
					match_pick_ban_element['dire']['bans'].append(str(pick_bans['hero_id']))

		pick_ban_input_element = prepareNetworkInput(match_pick_ban_element)
		pick_ban_result.append(pick_ban_input_element)

	#logger.info(pick_ban_result)
	return pick_ban_result

def prepareNetworkInput(pb_heroes):
	#logger.info('single mtch picks bans : ' + str(pb_heroes))
	victory = pb_heroes['victory']
	hero_count =  d2api.get_heroes()['count']
	winner = []
	loser =[]
	if(victory):
		winner = pb_heroes['radiant']['picks']
		loser = pb_heroes['dire']['picks']
	else:
		winner = pb_heroes['dire']['picks']
		loser = pb_heroes['radiant']['picks']

	input_data = np.full(hero_count, 0.0)
	output_data = np.full(hero_count, 0.0)

	#logger.info(input_data[20])
	for count in  range(5):
		logger.info('winner id : ' + str(int(winner[count])))
		winner_id = int(winner[count])
		loser_id =int(loser[count])
		if(winner_id > hero_count or loser_id > hero_count):
			logger.info("Hero key error. Winner key : %s, Loser key : %s",(winner_id, loser_id))
		
		output_data[winner_id] = 1.0
		input_data[loser_id] = 1.0


	logger.info('WINNERS : ' + str(winner))
	logging.info('Winner data : ' + str(output_data))
	logger.info('LOSERS : ' + str(loser))
	logging.info('Loser data : ' + str(input_data))
	return (input_data,output_data);


#training
training_data = getMatchPicksBansAsTeams(saveMatchesAsKeyId(saveLeagueMatchesAsKeyId(1)))
h_count = d2api.get_heroes()['count']
net = network.Network([h_count,25,h_count])
net.SGD(training_data, 30, 10, 3.0, test_data=None)

'''
with open('pick_bans_data.json', 'w') as j:
	json.dump(jdata, j, sort_keys=True, indent =4) 
'''