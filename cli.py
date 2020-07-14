#!/usr/bin/env python3

import json
import requests
import sys
import time
import pickle
from terminaltables import AsciiTable, SingleTable
from datetime import datetime
import argparse
import calendar

#validation args
parser = argparse.ArgumentParser(description='Search for 42 student information.')
parser.add_argument('id', help='id of student')
parser.add_argument('--raw',  dest='raw', help='show information line by line')
parser.add_argument('--no-cache',  dest='nocache', help='dont use cache')
parser.add_argument('--photo', dest='photo', help='show intra url of current photo')
args = parser.parse_args()

intra_id = args.id;
base_url = 'https://api.intra.42.fr'
authorization = 'Bearer 21bacae2412f985f6779e714190f32c53f9525a6391c6a1b90028436a737abb6'
headers = {'Authorization': authorization}

try:
	s = requests.get(f"{base_url}/v2/users/{intra_id}", headers=headers)
	s.raise_for_status()
except requests.exceptions.HTTPError:
	print('Sorry, unavailable id')
	quit()

sample_url = '{}/v2/users/{}'.format(base_url, intra_id)

endpoints = [
	'', 'apps', 'events', 'events_users',
	'exams', 'coalitions', 'coalitions_users',
	'cursus_users', 'campus_users', 'expertises_users',
	'groups', 'groups_users', 'languages_users',
	'locations', 'projects_users', 'quests_users',
	'roles', 'scale_teams', 'scale_teams/as_corrector',
	'scale_teams/as_corrected', 'tags', 'teams',
	'titles', 'titles_users',
]

endpoints = ['']

formatedEndpoints = []

for endpoint in endpoints:
	formatedEndpoints.append(('{}/' + endpoint).format(sample_url))

id_info = []

#import os, fnmatch

#def getCacheFile():
#    result = []
#    for root, dirs, files in os.walk("."):
#        for name in files:
#            if fnmatch.fnmatch(name, ".student-*"):
#                result.append(os.path.join(name))
#    return result[0]


#if getCacheFile()[9:] == intra_id:

try:
	with open(f'.student-{intra_id}', 'rb') as f:
		id_info = pickle.load(f)
except EnvironmentError:
	for i, endpoint in enumerate(formatedEndpoints):
		try:
			s = requests.get(endpoint, headers=headers)
			s.raise_for_status()
		except requests.exceptions.HTTPError as errc:
			print(errc)
		print("ENDPOINT:", endpoint)
		if s.status_code == 200:
			#print(json.loads(s.text)['email'])
			r = json.loads(s.text)
			id_info.append(r)
		else:
			id_info.append({})
		#time.sleep(0.5)
	with open(f".student-{intra_id}", 'wb') as f:
		pickle.dump(id_info, f)

oncampus = 'No' if id_info[0]["location"] is None else f'Yes ({id_info[0]["location"]})'
poolmonth = list(calendar.month_name).index(f'{id_info[0]["pool_month"]}'.title())
bocal = 'No' if id_info[0]["staff?"] is False else 'Yes'

finished = 0
inprogress = []
for i, project in enumerate(id_info[0]["projects_users"]):
	if project["status"] == 'finished':
		finished += 1;
	elif project["status"] == 'in_progress':
		inprogress.append(project["project"]["name"])

table_data = [
		['Name:', f'{id_info[0]["first_name"]}'.title()],
		['Email:', f'{id_info[0]["email"]}'.lower()],
		['Campus', f'42 {id_info[0]["campus"][0]["name"]}'],
		['On Campus', oncampus],
		['Pool', f'{poolmonth}/{id_info[0]["pool_year"]}'],
		['Wallet', f'₳ {id_info[0]["wallet"]}'],
		['Correction Points', f'{id_info[0]["correction_point"]}'],
		['Is Bocal?', f'{bocal}'],
		['Last Cursus', f'{id_info[0]["cursus_users"][len(id_info[0]["cursus_users"]) - 1]["cursus"]["name"]}'],
		['Finished projects', f'{finished}'],
		['In progress projects', f'{",".join(inprogress)}'],
]

table = SingleTable(table_data, intra_id)
table.inner_heading_row_border = False
table.inner_row_border = True
table.justify_columns = {0: 'center', 1: 'center', 2: 'center'}

print(table.table)

#print(json.dumps(student_information[0]["campus"][0]["name"], indent=4, sort_keys=True))
