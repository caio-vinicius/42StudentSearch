import requests
import json

def generate_token(base_url):
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	client_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	client_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	data = {'grant_type': 'client_credentials', 'client_id': f'{client_id}', 'client_secret': f'{client_secret}'}
	r = requests.post(f"{base_url}/oauth/token", headers=headers, data=data)
	token = json.loads(r.text)
	with open('.token', 'w') as f:
		json.dump(token['access_token'], f)
	return token['access_token']

def get_token(base_url):
	token = {}
	try:
		with open('.token') as token:
			token = json.load(token)
	except json.decoder.JSONDecodeError as errjson:
		pass

	headers = {'Authorization': f'Bearer {token}'}
	try:
		s = requests.get(f"{base_url}/v2/titles", headers=headers)
		s.raise_for_status()
	except requests.exceptions.HTTPError:
		token = generate_token(base_url)

	return token
