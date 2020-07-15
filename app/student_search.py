#!/usr/bin/env python3

from utils import verify_id, remove_archive
from args import parse_args
from oauth import get_token
from request import do_request
from output import raw, table, all
import argparse


def main(args):
	base_url = 'https://api.intra.42.fr'
	headers = {'Authorization': f'Bearer {get_token(base_url)}'}

	#check if arg id is valid
	verify_id(base_url, headers, args["id"])

	#if arg --clean-cache is set clean cache and exit
	if args["ccache"]:
		remove_archive(f'.student-{args["id"]}')
		remove_archive(f'.student-all-{args["id"]}')
		print("Cache clean sucessfully!")
		quit()

	#if arg --photo or -p is set print url and exit
	if args["photo"]:
		print(f'https://cdn.intra.42.fr/users/{args["id"]}.jpg')
		quit()

	#perform requests
	id_info = do_request(base_url, args["id"], args["ncache"], args["all"], headers)

	if not args["all"]:
		if args["raw"]:
			raw(id_info, args["id"])
		else:
			table(id_info, args["id"])
	else:
		all(id_info)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Search for 42 student information.')
	args = parse_args(parser)
	main(args)
