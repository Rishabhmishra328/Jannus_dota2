# imports
import dota2api
import os
import json
# api initialisation
d2api = dota2api.Initialise('6FCA7ABF90D69EA8377C7991168FEF08')
#directory initialisation
l_directory = 'E:\\Work\\Jannus\\Test Data\\Leagues\\JSON'
m_directory = 'E:\\Work\\Jannus\\Test Data\\Matches\\'
#files and path initialisation
files = os.listdir(l_directory)
paths = []
for f in files:
	paths.append(l_directory + '\\' +  f)

#variable initialisation
m_counter = 0
l_counter = 0
m_done_file_path = 'E:\\Work\\Jannus\\Test Data\\m_done.json'
m_failed_file_path = 'E:\\Work\\Jannus\\Test Data\\m_failed.json'
l_done_file_path = 'E:\\Work\\Jannus\\Test Data\\l_done.json'
l_failed_file_path = 'E:\\Work\\Jannus\\Test Data\\l_failed.json'
m_done = []
m_failed = []
l_done = []
l_failed = []
#looping through paths
for league in paths:
	#refreshing league json
	l_json = []
	try:
		#opening league json
		with open(league) as json_data:
			l_json = json.load(json_data)
			#league matches
			matches = l_json['matches']
			#matches counter in league
			m_l_counter = len(matches)
			#league counter tracker
			l_counter = l_counter + 1
			l_counter
			#league under process
			l_json['leagueid']
			#looping through matches
			for match in matches:
				try:
					#creating match file
					with open( m_directory + str(match['match_id']) + '.json', 'w') as match_file:
						json.dump(match, match_file)
					m_done.append(match['match_id'])
					#match counter tracker
					m_counter = m_counter + 1
					m_counter
				except UnicodeEncodeError:
					m_failed.append(match['match_id'])
				except KeyError:
					m_failed.append(match['match_id'])
				except FileNotFoundError:
					m_failed.append(match['match_id'])
	except FileNotFoundError:
			l_failed.append(l_json['leagueid'])
	except KeyError:
			l_failed.append(l_json['leagueid'])
	#adding completed league to done json
	l_done.append(l_json['leagueid'])

#log files creation
#macthes recorded
with open( str(m_done_file_path), 'w') as m_d_fp:
	json.dump(m_done, m_d_fp)

#matches failed from recording
with open( str(m_failed_file_path), 'w') as m_f_fp:
	json.dump(m_failed, m_f_fp)

#leagues recorded
with open( str(l_done_file_path), 'w') as l_d_fp:
	json.dump(l_done, l_d_fp)

#leagues failed from recording
with open( str(l_failed_file_path), 'w') as l_f_fp:
	json.dump(l_failed, l_f_fp)
