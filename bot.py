from buyer import Buyer
from multiprocessing import Pool
from functools import partial
import getpass
import hashlib
import urllib2
import glob
import getpass
import time

def buy(filename):
	driverObject = Buyer(filename, 1) # 1/Firefox 2/PhantomJS 3/Chrome

	#ADJUST TO CHEAP ITEM TO ADD TO CART AHEAD OF TIME
	driverObject.goTo("http://www.supremenewyork.com/shop/accessories/xwb4vgjm1/m3fsd6wkz")

	driverObject.printFilename()
	driverObject.addToCart(driverObject.getCurrUrl())

	#open CART tab
	driverObject.newTab()
	driverObject.goTo("http://www.supremenewyork.com/shop/cart");

	#open CHECKOUT tab
	driverObject.newTab()
	driverObject.goTo("https://www.supremenewyork.com/checkout");

	driverObject.changeTab()

	#driverObject.printCurrUrl()
	#driverObject.quit()


def pass_ask():
	_pass = getpass.getpass('Enter pass: ')
	hash_file = urllib2.urlopen('http://bahman.hayat.me/info/info.txt').read()
	if hashlib.sha224(_pass).hexdigest() == hash_file:
		print 'Access Granted'
		return True
	else:
		print 'Access Denied'
		return False

if __name__ == '__main__':
	#if pass_ask() == True:
	if True == True:
		#optimal speed is max number of files = number of cores of processor
		info_files = glob.glob("info-files-to-use/info*.json")
		num_files = len(info_files)

		start_time = time.time()
		pool = Pool(num_files)
		#url_input = raw_input("Enter the URL: ")
		#func = partial(buy, url_input)
		pool.map(buy, info_files)
		pool.close()
		pool.join()
		time_took = time.time() - start_time
		print("--- %s seconds ---" % time_took)
	else:
		print 'Incorrect Password'
		sys.exit(0)