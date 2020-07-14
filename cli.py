#!/usr/bin/env python3

import json
import requests
import sys
import time

print(sys.argv[1])

intra_id = sys.argv[1]

authorization = 'Bearer ################################################################'
headers = {'Authorization': authorization}
base_url = 'https://api.intra.42.fr'
sample_url = '{}/v2/users/{}'.format(base_url, intra_id)

#endpoints
endpoints = [
	'/appss',
	'/events',
	'/events_users',
	'/exams',
	'/coalitions',
	'/coalitions_users',
	'/cursus_users',
	'/campus_users',
	'/expertises_users',
	'/groups',
	'/groups_users',
	'/languages_users',
	'/locations',
	'/projects_users',
	'/quests_users',
	'/roles',
	'/scale_teams',
	'/scale_teams/as_corrector',
	'/scale_teams/as_corrected',
	'/tags',
	'/teams',
	'/titles',
	'/titles_users',
]

for i, endpoint in enumerate(endpoints):
	endpoint = ('{}' + endpoint).format(sample_url)
	endpoints[i] = endpoint

#print(endpoints[0])

student_information = []

try:
	for endpoint in endpoints:
		s = requests.get(endpoint, headers=headers)
		print("ENDPOINT:", endpoint)
		print("request: ", s.status_code)
		if s.status_code == 200:
			student_information.append(s.text)
		else:
			student_information.append(0)
		time.sleep(0.1)
except requests.ConnectionError as errc:
    print("Something went wrong: ", errc)

print(student_information)
print(student_information)
print(student_information)
print(student_information)

#r = json.loads(s.text)

#print(json.dumps(r, indent=4, sort_keys=True))
