from utils import get_endpoints
import requests
import json
import pickle
from datetime import datetime
import time

def format_endpoints(base_url, intra_id, allinfo):
	sample_url = f'{base_url}/v2/users/{intra_id}'
	endpoints = get_endpoints(allinfo)
	formated_endpoints = []
	for endpoint in endpoints:
		formated_endpoints.append(('{}/' + endpoint).format(sample_url))
	return formated_endpoints

def do_request(base_url, intra_id, nocache, allinfo, headers):
	id_info = []
	formated_endpoints = format_endpoints(base_url, intra_id, allinfo)
	try:
		if not nocache:
			with open(f'.student-{intra_id}', 'rb') as f:
				print("Getting information from cache...")
				id_info = pickle.load(f)
				return (id_info)
		else:
			raise ValueError('--no-cache is true')
	except (EnvironmentError, ValueError):
		print("Getting information from server...")
		for i, endpoint in enumerate(formated_endpoints):
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
		with open(file_name, 'wb') as f:
			pickle.dump(id_info, f)
	return id_info
