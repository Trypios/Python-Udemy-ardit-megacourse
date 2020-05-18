# WEBSITE BLOCKER - EDITS HOSTS

import time
from datetime import datetime as dt
from datetime import timedelta as td

def user_option():
	"""options for interactive loop"""
	print('\n' * 40)
	print('Select option')
	print('[a] Activate Website Blocker')
	print('[i] Add website to blacklist')
	print('[q] Quit\n')
	while True:
		try:
			user_input = str(input('a/i/q '))
			return user_input[0].lower()
		except:
			print('Invalid input...')
			time.sleep(1)

def active(text):
	"""determines if user wants to continue a certain action"""
	while True:
		try:
			user_input = str(input(text))
			if user_input[0].lower() == 'n':
				return False
			else:
				return True
		except:
			print('Invalid input...')
			time.sleep(1)

def add_to_blacklist():
	"""user adds sites to blacklist.txt"""
	with open("blacklist.txt","a") as blacklist:
		while True:
			website = str(input('Enter website to add to blacklist: '))
			blacklist.write('\n' + website)
			if not active('Continue? Y/n '):
				break

def update_blacklist():
	"""update blacklist list based on blacklist.txt file"""
	with open("blacklist.txt","r") as blacklist:
		website_blacklist = []
		for site in blacklist:
			if 'www' not in site:
				website_blacklist.append('www.' + site.strip())
			website_blacklist.append(site.strip())
	return website_blacklist

def whatTime():
	"""user sets timer for blocker"""
	while True:
		try:
			print('Use military hour (insert number from 0 to 23)')
			start = int(input('Select time to activate Website Blocker: '))
			end = int(input('How many hours will the Website Blocker stay active for? '))
			timer_begins = dt(dt.now().year, dt.now().month, dt.now().day, start)
			timer_ends = timer_begins + td(hours=end)
			return [timer_begins, timer_ends]
		except:
			print('Invalid input...')
			time.sleep(1)

def activate_siteblocker():
	"""user sets timer for blocker activation. Checks once every minute"""
	hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
	redirect = '127.0.0.1'
	website_blacklist = update_blacklist()
	timer = whatTime()
	while True:
		# hosts file updates with blacklist
		print('\n' * 40)
		if timer[0] < dt.now() < timer[1]:
			print('The timer is active between {} and {}'.format(timer[0], timer[1]))
			with open(hosts_path, 'r+') as file:
				content = file.read()
				for site in website_blacklist:
					if site not in content:
						file.write('{} {}\n'.format(redirect, site))

		else:
			# hosts file reverts back
			print('Inactive. The timer will activate between {} and {}'.format(timer[0], timer[1]))
			with open(hosts_path, 'r+') as file:
				content = file.readlines()
				file.seek(0)
				file.truncate()
				for line in content:
					if not any(site in line for site in website_blacklist):
						file.write(line)
		print('ctrl+c to stop')
		time.sleep(60)


# interactive loop
while True:
	user_input = user_option()
	# insert websites to blacklist.txt
	if user_input == 'i':
		add_to_blacklist()
	# activate website blocker
	elif user_input == 'a':
		activate_siteblocker()
	# quit program
	elif user_input == 'q':
		print('Exiting')
		break
	else:
		print('Invalid input...')
		time.sleep(1)
		