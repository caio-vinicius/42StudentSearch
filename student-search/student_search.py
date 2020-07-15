#!/usr/bin/env python3

#my functions
import utils
import parseargs

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
import pydoc

#validation args
parser = argparse.ArgumentParser(description='Search for 42 student information.')
args = parseargs.parse_args(parser)

nocache = args.nocache
cleancache = args.cleancache
intra_id = args.id
photo = args.photo
raw = args.raw
allinfo = args.all

#setup some api information
base_url = 'https://api.intra.42.fr'
authorization = 'Bearer c816269e14f7893f6785b3f740fd7c619962480a4cf7a2befbc45b311b495ecd'
headers = {'Authorization': authorization}

#id exists?
utils.id_exists(base_url, intra_id, headers)
#photo arg
utils.photo_arg(intra_id, photo)

sample_url = '{}/v2/users/{}'.format(base_url, intra_id)

endpoints = utils.get_endpoints(allinfo)

formatedEndpoints = []

for endpoint in endpoints:
	formatedEndpoints.append(('{}/' + endpoint).format(sample_url))

#requistions happening here
id_info = []

if cleancache:
	utils.remove_archive(f'.student-{intra_id}')
	utils.remove_archive(f'.student-all-{intra_id}')
	print("Cache clean sucessfully!")
	quit()

try:
	if not nocache:
		with open(f'.student-{intra_id}', 'rb') as f:
			print("Getting information from cache...")
			id_info = pickle.load(f)
	else:
		raise ValueError('--no-cache is true')
except (EnvironmentError, ValueError):
	print("Getting information from server...")
	for i, endpoint in enumerate(formatedEndpoints):
		try:
			s = requests.get(endpoint, headers=headers)
			s.raise_for_status()
		except requests.exceptions.HTTPError as errc:
			print(errc)
		#print("ENDPOINT:", endpoint)
		if s.status_code == 200:
			r = json.loads(s.text)
			id_info.append(r)
		else:
			id_info.append({})
		time.sleep(0.5)
	date_requisition = datetime.now()
	file_name = f'.student-{intra_id}' if not allinfo else f'.student-all-{intra_id}'
	print(file_name)
	with open(file_name, 'wb') as f:
		pickle.dump(id_info, f)

#all or table info?
if not allinfo:
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

	mostlocation = 'None'
	#most apper of a pc
	if id_info[1]:
		occurences = []
		for location in id_info[1]:
			occurences.append(location["host"][:7])
		mostlocation = (Counter(occurences)).most_common(1)[0][0]

	#apps
	apps = []
	if id_info[2]:
		for app in id_info[2]:
			apps.append(app["name"])

	table_data = [
		['Information', 'Value'],
		['Name', id_info[0]["first_name"].title()],
		['Title', title],
		['Email', id_info[0]["email"].lower()],
		['Country', id_info[0]["campus"][0]["country"]],
		['Campus', f'42 {id_info[0]["campus"][0]["name"]}'],
		['Language', id_info[0]["campus"][0]["language"]["name"]],
		['On Campus', oncampus],
		['Pool', 'None' if not poolmonth else f'{poolmonth}/{id_info[0]["pool_year"]}'],
		['Wallet', f'₳ {id_info[0]["wallet"]}'],
		['Correction Points', id_info[0]["correction_point"]],
		['Is Staff?', staff],
		['Last Cursus', id_info[0]["cursus_users"][len(id_info[0]["cursus_users"]) - 1]["cursus"]["name"]],
		['Finished projects', finished],
		['In progress projects', 'None' if not inprogress else ", ".join(inprogress)],
		['Amount Achievements', len(id_info[0]["achievements"])],
		['More times on', mostlocation],
		['Registred apps', 'None' if not apps else ", ".join(apps)],
		['Last exam', 'None' if not id_info[3] else id_info[3][0]["name"]],
		['Information obtained on', f'{datetime.fromtimestamp(int(os.path.getctime(f".student-{intra_id}")))}']
	]
	if raw:
		#skip first value (info, value)
		iterinfos = iter(table_data)
		next(iterinfos)
		for info in iterinfos:
			print(": ".join(map(str, info)))
	else:
		table = AsciiTable(table_data, intra_id)
		print(table.table)
		#pydoc.pager(table.table)
else:
	print(id_info)

