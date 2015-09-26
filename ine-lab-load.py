import telnetlib
import sys
import time
import os
import concurrent.futures

inputdir = raw_input('Which lab?  ')
pathdir = './' + inputdir + '/'
try:
	os.listdir(pathdir)
except:
	print '\nInvalid lab folder!\n'
	sys.exit(2)

gns3host = '127.0.0.1'
tcpport = '2001'
ports = {
'R1':'2001', 
'R2': '2003',
'R3': '2004',
'R4': '2005',
'R5': '2006',
'R6': '2007',
'R7': '2008',
'R8': '2009',
'R9': '2010',
'R10': '2011'
}

def CrawlDir():
	
	'''Grab relevant files, remove hidden files'''
	
	dirAll = os.listdir(labdir)
	dirTrim = []
	for dir in dirAll:
		if not dir[0] == '.':
			dirTrim.append(dir)
	return dirTrim
	
def push_config(device, tcpport, config):
	try:
		tn = telnetlib.Telnet('127.0.0.1',tcpport)
	
	except:
		print "IP Address <%s> was not found, or login failed!" % device
		sys.exit( -2)

	print 'Successfully logged in to %s' % device

	#print 'Sending enter for good measure'
	x = 0
	while x < 5:
		tn.write('\r')
		x += 1
	tn.write('end\r')
	tn.read_until( "#", 10)
	time.sleep(2)

	print 'Loading blank config....'
	try:
		tn.write('configure replace disk0:blank.cfg\r')
		tn.read_until('[no]')
		tn.write('yes\r')
	except:
		print 'Couldnt load blank config! Exiting'
		sys.exit(2)

	print 'Pushing config to %s' % device
	for line in config:
		line = line + '\r'
		tn.write(line)
		time.sleep(.25)


def main():
	devices = os.listdir(pathdir)
	os.chdir(pathdir)

	futures = []
	with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
		for each in devices:
			device = each.split('.')[0]
			#print device
			tcpport = ports[device]
			configtxt = open(each)
			config = configtxt.read().split('\n')
			futures.append(executor.submit(push_config, device, tcpport,config))	
	#for future in concurrent.futures.as_completed(futures):
	#	print 'COMPLETE A CONFIG'
	#	print future.result()
	
	print 'All configs loaded.'
		
if __name__ == '__main__':
	main()

