# imports
import dota2api

# api initialisation
d2api = dota2api.Initialise('6FCA7ABF90D69EA8377C7991168FEF08')

# getting leagues list
leagues = d2api.get_league_listing()

leagues = leagues['leagues']

# removing unnecessary information
for x in leagues:
	del x['description']
	del x['itemdef']
	del x['tournament_url']

# getting all league matches
matches = leagues

for m in matches:
	l_id = m['leagueid']
	league_matches = d2api.get_match_history(league_id = l_id)['matches']
	#dropping unneccesary information from league matches
	for lm in league_matches:
		del lm['cluster']
		del lm['cluster_name']
		del lm['lobby_name']
		del lm['flags']
		del lm['engine']
		del lm['lobby_type']
		del lm['human_players']
		del lm['negative_votes']
		del lm['positive_votes']




