#!/usr/bin/env python3

from oauth import get_token
import requests
import json
import sys
sys.path.append('../app')
import student_search
import argparse

parser = argparse.ArgumentParser(description='Unit Test for 42 Student Search')
parser.add_argument('list', default='1', nargs='?', action='store', help='choose between 0, 1 and 2 to random intra_id lists (default: 1)')
parser.add_argument('ids', nargs='*', action='store', help='id\'s to test (if empty will run "random" tests)')
args = parser.parse_args()

param_args = {'id': '', 'ccache': False, 'ncache': False, 'raw': False, 'photo': False, 'all': False}

lists = []
if args.list:
	lists.append('?sort=created_at')
	lists.append('?sort=login')
	lists.append('?sort=last_name')

if args.ids:
	for user in args.ids:
		param_args['id'] = user
		student_search.main(param_args)
else:
	base_url = 'https://api.intra.42.fr'
	headers = {'Authorization': f'Bearer {get_token(base_url)}'}
	try:
		s = requests.get(f'{base_url}/v2/users{lists[int(args.list)]}', headers=headers)
		s.raise_for_status()
	except requests.exceptions.ConnectionError:
		quit()
	users = json.loads(s.text)
	try:
		for user in users:
			param_args['id'] = user['login']
			student_search.main(param_args)
	except KeyboardInterrupt:
		quit()
