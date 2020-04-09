#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import argparse
import sys, os
import time

class crackerOffSec:

	source = 'http://cracker.offensive-security.com'
	#####################################################################################
	# Adds colourised notifications to text
	error = '\033[31m[!] \033[0m'       	# [!] Red
	fail = '\033[31m[-] \033[0m'        	# [-] Red
	success = '\033[32m[+] \033[0m'     	# [+] Green
	event = '\033[34m[*] \033[0m'		# [*] Blue
	debug = '\033[35m[%] \033[0m'       	# [%] Magenta
	notification = '\033[33m[-] \033[0m'	# [-] Yellow

	green = '\033[32m'
	nocolor  = '\033[0m'

	#####################################################################################
	# rgparse
	# https://docs.python.org/3.3/library/argparse.html#module-argparse
	
	def get_args(self,):
		parser = argparse.ArgumentParser(description='Simple tool for crack hashes using {}{}{}'.format(self.green, self.source, self.nocolor))
		# Add arguments
		parser.add_argument('-hs','--hash', type=str, help='Add your hash value or a file', required=True)
		parser.add_argument('-p', '--pcode', type=str, help='Add your Priority Code', required=True)
		# Array for all arguments passed to script
		args = parser.parse_args()

		return args

	#####################################################################################

	def make_request(self, hash, pcode):

		proxies = {'http': 'http://localhost:8080'}
		try:
			session = requests.session()
			response = session.get('{}/index.php'.format(self.source))
			headers = {
					'User-Agent' : 'Mozilla/5.0 (X11; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0',
					'Referer' : 'http://cracker.offensive-security.com/index.php',
					'Cookie': 'PHPSESSID={}'.format(session.cookies['PHPSESSID']),
					'Content-Type' : 'application/x-www-form-urlencoded',
				}
			data = {'hash' : hash, 'priority' : pcode}
			res = session.post('{}/insert.php'.format(self.source), headers=headers, data=data)
			soup = BeautifulSoup(res.text, "lxml")
				
			for element in soup.findAll("div",attrs={'id':'success'}):
				if "plaintext is" in element.text:
					val = element.text.split(' plaintext is:')[1]
					print("{}The plaintext is :{}{}{}".format(self.success, self.green, val, self.nocolor))
					return None
			
			for element in soup.findAll("div",attrs={'id':'warning'}):
				if "still in the queue to be cracked" in element.text:
					print ("{}{}".format(self.notification, element.txt))
					return None

			for element in soup.findAll("div",attrs={'id':'error'}):
				if "Bad hash" in element.text:
					print("{}Bad hash format! Try again.".format(self.fail))
					return None
			print("{}Hash not Found. Sorry!".format(self.error))

		except requests.exceptions.RequestException as e:
			sys.exit(self.error + "Something going wrong with the request. Please check the url and the connectivity")

	def use_afile(self, src, pcode):
		for hash in open(src, 'rb').readlines():
			hash = hash.decode("utf-8").strip()
			self.make_request(hash, pcode)
			time.sleep(2)

	def __init__(self,):
		args = self.get_args()
		if os.path.isfile(args.hash):
			self.use_afile(args.hash, args.pcode)
		else:
			self.make_request(args.hash, args.pcode)


crackerOffSec()
