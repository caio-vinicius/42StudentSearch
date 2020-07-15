import requests
import json

def generate_token(base_url):
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	client_id = '64c120e70b3e851e4e2c7b047755ed785bd23d01e77e29fb7a52b51ba6df3ccb'
	client_secret = '7097f8d16c9f0eee2515dc8c9abf6b7112a306e9573966d4f55d130d2fe770ab'
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
	except FileNotFoundError:
		token = generate_token(base_url)

	headers = {'Authorization': f'Bearer {token}'}
	try:
		s = requests.get(f"{base_url}/v2/titles", headers=headers)
		s.raise_for_status()
	except requests.exceptions.HTTPError:
		token = generate_token(base_url)

	return token
