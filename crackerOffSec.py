#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import argparse
import sys

class crackerOffSec:

	source = 'http://cracker.offensive-security.com'
	#####################################################################################
	# Adds colourised notifications to text
	error = '\033[31m[!] \033[0m'       # [!] Red
	fail = '\033[31m[-] \033[0m'        # [-] Red
	success = '\033[32m[+] \033[0m'     # [+] Green
	event = '\033[34m[*] \033[0m'       # [*] Blue
	debug = '\033[35m[%] \033[0m'       # [%] Magenta
	notification = '[-] '               # [-]

	green = '\033[32m'
	nocolor  = '\033[0m'

	#####################################################################################
	# rgparse
	# https://docs.python.org/3.3/library/argparse.html#module-argparse
	
	def get_args(self,):
		parser = argparse.ArgumentParser(description='Simple tool for crack hashes using {}{}{}'.format(self.green, self.source, self.nocolor))
		# Add arguments
		parser.add_argument('-hs','--hash', type=str, help='Add your hash value', required=True)
		parser.add_argument('-p', '--pcode', type=str, help='Add your Priority Code', required=True)
		# Array for all arguments passed to script
		args = parser.parse_args()

		# Assign args to variables
		hash = args.hash
		pcode = args.pcode

		return hash,pcode

#####################################################################################

	def makeRequest(self, hash, pcode):

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
			res = session.post('{}/insert.php'.format(self.source), headers=headers, data=data, proxies=proxies)
			soup = BeautifulSoup(res.text, "lxml")
			for element in soup.findAll("div",attrs={'id':'success'}):
				print(element.text)
				if "plaintext is" in element.text:
					val = element.text.split(' plaintext is:')[1]
					sys.exit("{}The plaintext is :{}{}{}".format(self.success, self.green, val, self.nocolor))
				else:
					sys.exit("{}Hash not Found. Sorry!".format(self.error))
			for element in soup.findAll("div",attrs={'id':'error'}):
				if "Bad hash" in element.text:
					sys.exit("{}Bad hash format! Try again.".format(self.fail))

		except requests.exceptions.RequestException as e:
			sys.exit(self.error + "Something going wrong with the request. Please check the url and the connectivity")

	def __init__(self,):
		args = self.get_args()
		self.makeRequest(args[0],args[1])


crackerOffSec()
