# imports
import dota2api
import json
import logging
import os
import re
from progress.bar import Bar

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

def saveLeagueMatchesAsKeyId():
	#getting leagues list
	leagues = d2api.get_league_listing()
	leagues = leagues['leagues']
	league_pbar = Bar('League Progress', max = len(leagues))

	# getting all league matches
	for m in leagues:
		l_id = m['leagueid']
		league_pbar.next()
		logger.info('Changing league...')
		league_matches = d2api.get_match_history(league_id = l_id)['matches']
		matches_pbar = Bar('Match Progress', max = len(league_matches))
		league_match_id = {}
		league_match_id['id'] = l_id
		league_match_id['matches'] = []
		#dropping unneccesary information from league matches
		keys_to_acquire = matchAcquiringKeyList();

		if not os.path.exists('../data/json/league/' + re.sub(r'[^\x00-\x7F]+','', getLeagueIdAsKeyNameList(l_id)) ):
			for lm in league_matches:
				matches_pbar.next()
				try:	
					league_match_id['matches'].append(str(lm['match_id']))
				except KeyError:
					logger.info('keyError' + str(l_id)  + '\t' + str(lm['match_id']))

				try:		
					if(getLeagueIdAsKeyNameList(l_id) != None):
						league_name = getLeagueIdAsKeyNameList(l_id)
						match_file_path = '../data/json/league/'+ str(league_name)
						createFolder(match_file_path)

						with open('../data/json/league/' + re.sub(r'[^\x00-\x7F]+','', league_name) + '/matches.txt', 'w') as match_file:
							json.dump(league_match_id, match_file)

				except:		
					#creating folder structure
					if not os.path.exists('../data/json/league/others'):
						os.makedirs('../data/json/league/others')
					with open('../data/json/league/others/' + str(l_id) + '.txt', 'w') as match_file:
						json.dump(league_match_id, match_file)
		else:
			logger.info(re.sub(r'[^\x00-\x7F]+','', getLeagueIdAsKeyNameList(l_id)) + ' already exists.')


def saveMatchesAsKeyId():
	#getting match list
	league_directory_paths = os.listdir('../data/json/league')

	league_pbar = Bar('League Progress', max = len(league_directory_paths))

	# getting all league matches
	for league_directory in league_directory_paths:
		league_pbar.next()
		match_directory_list = os.listdir('../data/json/league/' + league_directory)
    		with open('../data/json/league/' + league_directory + '/' + match_directory_list[0], 'r') as m_file:
    			league_matches_list = json.loads(m_file.read())
			matches_pbar = Bar('Match Progress', max = len(league_matches_list['matches']))
    			for matchid in league_matches_list['matches']:
    				match_json = d2api.get_match_details(match_id = matchid)
    				matches_pbar.next()
   				match_filename = match_json['match_id']
				match_file_path = '../data/json/match/'+ league_directory + '/' +re.sub(r'[^\x00-\x7F]+','', matchid)
				createFolder(match_file_path)

				with open('../data/json/match/' + league_directory + '/' +re.sub(r'[^\x00-\x7F]+','', matchid) + '/pick_bans.txt', 'w') as match_file:
					match_picks_bans = match_json['picks_bans']
					json.dump(match_picks_bans, match_file)



'''
		l_id = m['leagueid']
		league_pbar.next()
		logger.info('Changing league...')
		league_matches = d2api.get_match_history(league_id = l_id)['matches']
		matches_pbar = Bar('Match Progress', max = len(league_matches))
		league_match_id = {}
		league_match_id['id'] = l_id
		league_match_id['matches'] = []
		#dropping unneccesary information from league matches
		keys_to_acquire = matchAcquiringKeyList();

		if not os.path.exists('../data/json/league/' + re.sub(r'[^\x00-\x7F]+','', getLeagueIdAsKeyNameList(l_id)) ):
			for lm in league_matches:
				matches_pbar.next()
				try:	
					league_match_id['matches'].append(str(lm['match_id']))
				except KeyError:
					logger.info('keyError' + str(l_id)  + '\t' + str(lm['match_id']))

				try:		
					if(getLeagueIdAsKeyNameList(l_id) != None):
						league_name = getLeagueIdAsKeyNameList(l_id)
						match_file_path = '../data/json/league/'+ str(league_name)
						createFolder(match_file_path)

						with open('../data/json/league/' + re.sub(r'[^\x00-\x7F]+','', league_name) + '/matches.txt', 'w') as match_file:
							json.dump(league_match_id, match_file)

				except:		
					#creating folder structure
					if not os.path.exists('../data/json/league/others'):
						os.makedirs('../data/json/league/others')
					with open('../data/json/league/others/' + str(l_id) + '.txt', 'w') as match_file:
						json.dump(league_match_id, match_file)
		else:
			logger.info(re.sub(r'[^\x00-\x7F]+','', getLeagueIdAsKeyNameList(l_id)) + ' already exists.')
'''

saveMatchesAsKeyId()
