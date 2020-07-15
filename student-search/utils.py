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
		return ['', 'locations', 'apps', 'exams']

def verify_id(base_url, headers, intra_id):
	try:
		s = requests.get(f"{base_url}/v2/users/{intra_id}/titles", headers=headers)
		s.raise_for_status()
	except requests.exceptions.HTTPError:
		print('Sorry, unavailable id. Try again.')
		quit()












