from terminaltables import AsciiTable
from collections import Counter
from datetime import datetime
import calendar
import os

def format_info(id_info, intra_id):
	#title
	title = ''
	if id_info[0]['titles']:
		title = f'{id_info[0]["titles"][0]["name"]}'
	else:
		title = 'None'

	#on campus
	oncampus = 'No'
	if id_info[0]['location']:
		oncampus = f'Yes ({id_info[0]["location"]}'

	poolmonth = None
	if id_info[0]['pool_month']:
		poolmonth = list(calendar.month_name).index(f'{id_info[0]["pool_month"]}'.title())

	staff = 'No'
	if id_info[0]['staff?']:
		staff = 'Yes'

	#finished and in progress projects
	finished = 0
	inprogress = []
	if id_info[0]['projects_users']:
		for i, project in enumerate(id_info[0]['projects_users']):
			if project['status'] == 'finished':
				finished += 1;
			elif project['status'] == 'in_progress' or 'waiting_for_correction':
				inprogress.append(project['project']['name'])

	mostlocation = 'None'
	#most apper of a pc
	if id_info[1]:
		occurences = []
		for location in id_info[1]:
			occurences.append(location['host'][:7])
		mostlocation = (Counter(occurences)).most_common(1)[0][0]

	#apps
	apps = []
	if id_info[2]:
		for app in id_info[2]:
			apps.append(app['name'])

	table_data = [
		['Information', 'Value'],
		['Name', id_info[0]['first_name'].title()],
		['Title', title],
		['Email', id_info[0]['email'].lower()],
		['Country', id_info[0]['campus'][0]["country"]],
		['Campus', f'42 {id_info[0]["campus"][0]["name"]}'],
		['Language', id_info[0]['campus'][0]['language']['name']],
		['On Campus', oncampus],
		['Pool', 'None' if not poolmonth else f'{poolmonth}/{id_info[0]["pool_year"]}'],
		['Wallet', f'₳ {id_info[0]["wallet"]}'],
		['Correction Points', id_info[0]['correction_point']],
		['Is Staff?', staff],
		['Last Cursus', 'None' if not id_info[0]['cursus_users'] else id_info[0]['cursus_users'][len(id_info[0]['cursus_users']) - 1]['cursus']['name']],
		['Finished projects', finished],
		['In progress projects', 'None' if not inprogress else ", ".join(inprogress)],
		['Amount Achievements', len(id_info[0]['achievements'])],
		['More times on', mostlocation],
		['Registred apps', 'None' if not apps else ", ".join(apps)],
		['Last exam', 'None' if not id_info[3] else id_info[3][0]['name']],
		['Information obtained on', f'{datetime.fromtimestamp(int(os.path.getctime(f".student-{intra_id}")))}']
	]
	return table_data

def table(id_info, intra_id):
	table_data = format_info(id_info, intra_id)
	table = AsciiTable(table_data, intra_id)
	print(table.table)

def raw(id_info, intra_id):
	table_data = format_info(id_info, intra_id)
	#skip first 2 columns of table (info, value)
	iterinfos = iter(table_data)
	next(iterinfos)
	for info in iterinfos:
		print(": ".join(map(str, info)))

def all(id_info):
	print(id_info)
