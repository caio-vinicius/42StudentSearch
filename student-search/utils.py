import os
import requests

def remove_archive(file_name):
	try:
		os.remove(file_name)
	except OSError:
		pass

def get_endpoints(allinfo):
	if allinfo:
		return [
			'', 'apps', 'events', 'events_users',
			'exams', 'coalitions', 'coalitions_users',
			'cursus_users', 'campus_users', 'expertises_users',
			'groups', 'groups_users', 'languages_users',
			'locations', 'projects_users', 'quests_users',
			'roles', 'scale_teams', 'scale_teams/as_corrector',
			'scale_teams/as_corrected', 'tags', 'teams',
			'titles', 'titles_users',
		]
	else:
		return [
			'', 'locations', 'apps', 'exams'
		]

def id_exists(base_url, intra_id, headers):
	try:
		s = requests.get(f"{base_url}/v2/users/{intra_id}", headers=headers)
		s.raise_for_status()
	except requests.exceptions.HTTPError:
		if s.status_code == 404:
			print('Unavailable id')
		elif s.status_code == 401:
			print('Expired token')
		quit()

def photo_arg(intra_id, photo):
	if photo:
		print(f'https://cdn.intra.42.fr/users/{intra_id}.jpg')
		quit()












