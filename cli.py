#!/usr/bin/env python3

import json
import requests
import sys
import time
import pickle



if len(sys.argv) <= 1:
	print('Usage:\n\t ./cli.py id [ --table ] [ --photo ] [ --no-cache ]')
	quit()

authorization = 'Bearer ################################################################'
headers = {'Authorization': authorization}
base_url = 'https://api.intra.42.fr'
intra_id = sys.argv[1]
sample_url = '{}/v2/users/{}'.format(base_url, intra_id)

s = requests.get(f"{base_url}/v2/users/{intra_id}/titles", headers=headers)
if s.status_code == 404:
	print('Sorry, unavailable id')
	quit()

endpoints = [
	'apps', 'events', 'events_users',
	'exams', 'coalitions', 'coalitions_users',
	'cursus_users', 'campus_users', 'expertises_users',
	'groups', 'groups_users', 'languages_users',
	'locations', 'projects_users', 'quests_users',
	'roles', 'scale_teams', 'scale_teams/as_corrector',
	'scale_teams/as_corrected', 'tags', 'teams',
	'titles', 'titles_users',
]

formatedEndpoints = []

for endpoint in endpoints:
	formatedEndpoints.append(('{}/' + endpoint).format(sample_url))

student_information = []

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
		student_information = pickle.load(f)
except EnvironmentError:
	for i, endpoint in enumerate(formatedEndpoints):
		try:
			s = requests.get(endpoint, headers=headers)
			s.raise_for_status()
		except requests.exceptions.HTTPError as errc:
			print(errc)
		print("ENDPOINT:", endpoint)
		if s.status_code == 200:
			json_dict = json.loads(s.text)
			student_information.append(json_dict)
		else:
			student_information.append({})
		time.sleep(0.5)
	with open(f".student-{intra_id}", 'wb') as f:
		pickle.dump(student_information, f)

print(json.dumps(student_information[20], indent=4, sort_keys=True))
