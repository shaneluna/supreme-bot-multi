from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.support.ui import Select
from collections import OrderedDict
import logging
import json
import time
import datetime

class Buyer:
	logging.basicConfig(filename='./logs/errors.log',level=logging.DEBUG)

	#initialization
	def __init__(self, filename, driverOption):
		self.filename = filename
		#load corresponding json file
		self.j = json.load(open(self.filename), object_pairs_hook=OrderedDict)

		#DRIVER TO USE based off driverOption
		if driverOption == 1:
			self.driver = webdriver.Firefox()
		elif driverOption == 2:
			webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'
			self.driver = webdriver.PhantomJS(executable_path='./phantomjs', service_log_path='/dev/null')
		elif driverOption == 3:
			self.driver = webdriver.Chrome(executable_path='./chromedriver')

	#print object's initialized filename
	def printFilename(self):
		print self.filename

	#print the current url of the object driver
	def printCurrUrl(self):
		print self.driver.current_url

	#returns the current url of the object driver (does NOT print)
	def getCurrUrl(self):
		return self.driver.current_url

	#object driver goes to the specified URL
	def goTo(self, url):
		self.driver.get(url)

	#object driver opens a new tab using shortcuts
	def newTab(self):
		self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 

	#object changes tab 1 cycle
	def changeTab(self):
		self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

	#select size of item category
	def selectSize(self, item):
		#create array of listed sizes in json info file for the given item in the size_info object
		self.itemSizesArr = self.j["size_info"][item]
		self.lastSize = len(self.itemSizesArr)-1
		for self.i, self.size in enumerate(self.itemSizesArr):
			try: 
				#Select(WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.NAME, "size")))).select_by_visible_text(self.size)
				#find html select tag and then select size if visible text is the same as size from info file
				Select(WebDriverWait(driver, 0.5).until(EC.presence_of_element_located((By.TAG_NAME, "select")))).select_by_visible_text(self.size)
				break
			except NoSuchElementException as e:
				#size not found (sold out) and that size is the last desired size
				if self.i == self.lastSize:
					self.msg = (str(datetime.datetime.now()) + "- Preferred size not available for %s" % self.filename)
					print "\n" + self.msg + "\n"
					logging.error(self.msg)
					loggin.error(e)
				#pass

	#add the item on current url to cart
	def addToCart(self, url):
		self.currentUrl = url

		try:
			if "jackets" in self.currentUrl:
				selectSize("jackets_size")
				#time.sleep(0.5)
			elif "/shirts" in self.currentUrl:
				selectSize("shirts_size")
			elif "tops_sweaters" in self.currentUrl:
				selectSize("tops-sweaters_size")
			elif "sweatshirts" in self.currentUrl:
				selectSize("sweatshirts_size")
			elif "pants" in self.currentUrl:
				selectSize("pants_size")
			elif "t-shirts" in self.currentUrl:
				selectSize("t-shirts_size")
			elif "hats" in self.currentUrl:
				selectSize("hats_size")
			elif "bags" in self.currentUrl:
				selectSize("bags_size")
			elif "accessories" in self.currentUrl:
				selectSize("accessories_size")
			elif "skate" in self.currentUrl:
				selectSize("skate_size")
			elif "shoes" in self.currentUrl:
				selectSize("shoes_size")
			else:
				selectSize("random_url_size")
		except TimeoutException as e:
			self.msg = (str(datetime.datetime.now()) + " - Could not select proper size - Item might be sold out for %s" % self.filename)
			print "\n" + self.msg + "\n"
			logging.error(self.msg)
			logging.error(e)
		except Exception as e:
			self.msg = (str(datetime.datetime.now()) + " - Could not select size for %s" % self.filename)
			print "\n" + self.msg + "\n"
			logging.error(self.msg)
			logging.error(e)

		try:
			self.driver.find_element_by_name('commit').click()
		except Exception as e:
			self.msg = (str(datetime.datetime.now()) + " - Could not find the ADD TO CART button for %s" % self.filename)
			print "\n" + self.msg + "\n"
			logging.error(self.msg)
			logging.error(e)

	#close/quit driver
	def quit(self):
		self.driver.close();
		self.driver.quit();