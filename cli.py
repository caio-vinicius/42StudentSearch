#!/usr/bin/env python3

import json
import requests
import sys
import time
import pickle
from terminaltables import AsciiTable, SingleTable
from datetime import datetime, date
import argparse
import calendar
from collections import Counter
import os

#validation args
parser = argparse.ArgumentParser(description='Search for 42 student information.')
parser.add_argument('id', help='id of student')
parser.add_argument('--raw',  dest='raw', help='show information line by line')
parser.add_argument('--no-cache',  dest='nocache', help='dont use cache')
parser.add_argument('--photo', dest='photo', help='show intra url of current photo')
args = parser.parse_args()

#setup some api information
intra_id = args.id;
base_url = 'https://api.intra.42.fr'
authorization = 'Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
headers = {'Authorization': authorization}

#id exists?
try:
	s = requests.get(f"{base_url}/v2/users/{intra_id}/titles", headers=headers)
	s.raise_for_status()
except requests.exceptions.HTTPError:
	print('Sorry, something went wrong')
	quit()

sample_url = '{}/v2/users/{}'.format(base_url, intra_id)

endpoints = [
	'', 'locations', 'apps', 'exams'
]

formatedEndpoints = []

for endpoint in endpoints:
	formatedEndpoints.append(('{}/' + endpoint).format(sample_url))

#import os, fnmatch

#def getCacheFile():
#    result = []
#    for root, dirs, files in os.walk("."):
#        for name in files:
#            if fnmatch.fnmatch(name, ".student-*"):
#                result.append(os.path.join(name))
#    return result[0]


#if getCacheFile()[9:] == intra_id:


#requistions happening here
id_info = []

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
		time.sleep(0.5)
	date_requisition = datetime.now()
	with open(f".student-{intra_id}", 'wb') as f:
		pickle.dump(id_info, f)

#abstract some information

#title
title = ''
if id_info[0]["titles"]:
	title = f'{id_info[0]["titles"][0]["name"]}'
else:
	title = 'None'

#on campus
oncampus = 'No'
if id_info[0]["location"]:
	oncampus = f'Yes ({id_info[0]["location"]}'

poolmonth = None
if id_info[0]["pool_month"]:
	poolmonth = list(calendar.month_name).index(f'{id_info[0]["pool_month"]}'.title())

staff = 'No'
if id_info[0]["staff?"]:
	staff = 'Yes'

#finished and in progress projects
finished = 0
inprogress = []
if id_info[0]["projects_users"]:
	for i, project in enumerate(id_info[0]["projects_users"]):
		if project["status"] == 'finished':
			finished += 1;
		elif project["status"] == 'in_progress' or 'waiting_for_correction':
			inprogress.append(project["project"]["name"])


#most apper of a pc
if id_info[1]:
	occurences = []
	for location in id_info[1]:
		occurences.append(location["host"][:6])
	mostlocation = (Counter(occurences)).most_common(1)[0][0]

#apps
apps = []
if id_info[2]:
	for app in id_info[2]:
		apps.append(app["name"])

#place information
#try:
table_data = [
		['Name', id_info[0]["first_name"].title()],
		['Title', title],
		['Email:', id_info[0]["email"].lower()],
		['Country', id_info[0]["campus"][0]["country"]],
		['Campus', f'42 {id_info[0]["campus"][0]["name"]}'],
		['Language', id_info[0]["campus"][0]["language"]["name"]],
		['On Campus', oncampus],
		['Pool', None if not poolmonth else f'{poolmonth}/{id_info[0]["pool_year"]}'],
		['Wallet', f'₳ {id_info[0]["wallet"]}'],
		['Correction Points', id_info[0]["correction_point"]],
		['Is Staff?', staff],
		['Last Cursus', id_info[0]["cursus_users"][len(id_info[0]["cursus_users"]) - 1]["cursus"]["name"]],
		['Finished projects', finished],
		['In progress projects', None if not inprogress else ", ".join(inprogress)],
		['Amount Achievements', len(id_info[0]["achievements"])],
#		['More times on', mostlocation],
		['Registred apps', None if not apps else ", ".join(apps)],
		['Last exam', None if not id_info[3] else id_info[3][0]["name"]],
		['Information obtained on', datetime.fromtimestamp(int(os.path.getctime(f".student-{intra_id}")))]
	]
#except IndexError as e:
	#print("You need to make a new requistion: ", e)

table = SingleTable(table_data, intra_id)
table.inner_heading_row_border = False
table.inner_row_border = True
table.justify_columns = {0: 'center', 1: 'center', 2: 'center'}

print(table.table)

#print(json.dumps(student_information[0]["campus"][0]["name"], indent=4, sort_keys=True))
