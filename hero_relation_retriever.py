# imports
import dota2api
import os
import json
# api initialisation
d2api = dota2api.Initialise('6FCA7ABF90D69EA8377C7991168FEF08')
#directory initialisation
m_directory = 'E:\\Work\\Jannus\\Test Data\\Matches\\'
p_b_directory = 'E:\\Work\\Jannus\\Test Data\\Picks Bans\\'
#files
files = os.listdir(m_directory)
#paths
path = []
for f in files:
	path.append(m_directory + f)