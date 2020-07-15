def parse_args(p):
	p.add_argument('id', action='store', help='id of student')
	p.add_argument('--clean-cache',  action='store_true', default=False,dest='cleancache', help='delete cache files')
	p.add_argument('--no-cache', '-n', action='store_true', default=False,dest='nocache', help='dont use cache, reperform request')
	p.add_argument('--raw', '-r',  action='store_true', default=False,dest='raw', help='show information without a table')
	p.add_argument('--photo', '-p', action='store_true', default=False, dest='photo', help='show intra url image and exit')
	p.add_argument('--all', action='store_true', default=False, dest='all', help='output all possible information in json')
	a = p.parse_args()

	args = {'id': a.id, 'ccache': a.cleancache, 'ncache': a.nocache, 'raw': a.raw, 'photo': a.photo, 'all': a.all}

	return args
