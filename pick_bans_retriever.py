# imports
import dota2api
import os
import json
# api initialisation
d2api = dota2api.Initialise('6FCA7ABF90D69EA8377C7991168FEF08')
#directory initialisation
l_directory = 'E:\\Work\\Jannus\\Test Data\\Leagues\\JSON'
m_directory = 'E:\\Work\\Jannus\\Test Data\\Matches\\'

with open(m_directory + '2344839178.json') as match_json_data:
    m_json = json.load(match_json_data)
    
players = m_json['players']

players_drop_keys = {'leaver_status_description','backpack_0','backpack_1','backpack_2','item_0_name','item_1_name','item_2_name','item_3_name','item_4_name','item_5_name','item_0','item_1','item_2','item_3','item_4','item_5','leavers_status','leaver_status_name','player_slot','gold_spent','ability_upgrades','account_id'}

for player in players:
	for pdk in players_drop_keys:
		try:
			del player[pdk]
		except KeyError:
			print('Unable to delete key: ' + str(pdk))

try:
	picks_bans = m_json['picks_bans']
except KeyError:
	print('Picks Bans Uncalibrated')

match_drop_keys = {'dire_captian','first_blood_time','radiant_captian','dire_team_id','radiant_team_id','players','picks_bans'}

for mdk in match_drop_keys:
	try:
		del m_json[mdk]
	except KeyError:
		print('Unable to delete key: ' + str(mdk))

data_matcher = []
for player in players:
	for pb in picks_bans:
		if (pb['hero_id'] == player['hero_id']):
			data_temp = pb
			data_temp.update(player)
			data_matcher.append(data_temp)

bans = []

for pb in picks_bans:
	try:
		if(pb['is_pick'] == False):
			del pb['is_pick']
			bans.append(pb)
	except KeyError:
			pass

radiant = []
dire = []
for player in data_matcher:
	try:
		if(player['team'] == 1):
			dire.append(player)
		else:
			radiant.append(player)
	except KeyError:
			pass

print(radiant[0])
#print(dire)
#print(bans)