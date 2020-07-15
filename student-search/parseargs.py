import argparse

def parse_args(parser):
	parser.add_argument('id', action='store', help='id of student')
	parser.add_argument('--raw', '-r',  action='store_true', default=False,dest='raw', help='show information without a table')
	parser.add_argument('--no-cache', '-n', action='store_true', default=False,dest='nocache', help='dont use cache, reperform request')
	parser.add_argument('--clean-cache',  action='store_true', default=False,dest='cleancache', help='delete cache files')
	parser.add_argument('--photo', '-p', action='store_true', default=False, dest='photo', help='show intra url image and exit')
	parser.add_argument('--all', action='store_true', default=False, dest='all', help='output all possible information in json')
	return parser.parse_args()

