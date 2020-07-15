#!/usr/bin/env python3

import utils
import args
import oauth
import request
import output
import argparse


def main(args):
	base_url = 'https://api.intra.42.fr'
	headers = {'Authorization': f'Bearer {oauth.get_token(base_url)}'}

	#check if arg id is valid
	utils.verify_id(base_url, headers, args["id"])

	#if arg --clean-cache is set clean cache and exit
	if args["ccache"]:
		utils.remove_archive(f'.student-{args["id"]}')
		utils.remove_archive(f'.student-all-{args["id"]}')
		print("Cache clean sucessfully!")
		quit()

	#if arg --photo or -p is set print url and exit
	if args["photo"]:
		print(f'https://cdn.intra.42.fr/users/{args["id"]}.jpg')
		quit()

	#perform requests
	id_info = request.do_request(base_url, args["id"], args["ncache"], args["all"], headers)

	if not args["all"]:
		if args["raw"]:
			output.raw(id_info, args["id"])
		else:
			output.table(id_info, args["id"])
	else:
		output.all(id_info)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Search for 42 student information.')
	args = args.parse_args(parser)
	main(args)
