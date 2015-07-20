import urllib2, urllib, os, re
import xml.etree.ElementTree as ET
import lxml
import lxml.html as h
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# driver = webdriver.PhantomJS('C:\phantomjs-2.0.0-windows\phantomjs.exe')
# fp = webdriver.FirefoxProfile()
# fp.add_extension(extension='G:\Downloads\lewa\py\\adblock_plus.xpi')
# fp.set_preference('browser.download.folderList', 2)
# fp.set_preference('browser.download.manager.showWhenStarting', False)
# fp.set_preference('browser.download.dir', "D:\\new week")
# fp.set_preference('browser.helperApps.neverAsk.saveToDisk', "application/forced-download")
# driver = webdriver.Firefox(firefox_profile=fp)
# options = webdriver.ChromeOptions()
# options.set_preference('browser.download.dir', "D:\\new week")
# driver = webdriver.Chrome(chrome_options=options)
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "D:\\new week"}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

def getMatcher(str):
       return re.search("(.*?(\s\d{4})?(?=\s\d{1,4}))|(.*?(?=,\s20\d{2}-\d{2}-\d{2})|(.*?(?=\s#\d\d?\d?)))", str)

def yearCheck(str):
	return re.search("\d{4}", str)

def getImage(str):
	imageURL = urllib2.urlopen(str)
	getHTML = imageURL.read()
	strn_html = "".join(getHTML)
	loc = re.search('/fileName.*\=(small)', str_html)
	head = re.search('http://www\d{1,4}.*com', str_html)
	return head.group() + loc.group()

def downloadComic(str):
	m = getMatcher(str)
	if (m and m.group() in folders.keys()):
		year = yearCheck(str)
		if(year and year.group() > "2013"):
			dst_exists = os.path.isfile(os.path.join(folders[m.group()], str))
			if not dst_exists:
				dwnld_exists = os.path.isfile(os.path.join("D:\\new week", str))
				if not dwnld_exists:
					if str.find("Beige") == -1:
						if str.find("omegaguy edit") == -1:
							if str.find("resized") == -1:
								if str.find("c2c") == -1:
									print m.group()
									print str
									print url
									# print str
									# print dl
									# print year.group()
									driver.get(url)
									button = driver.find_element_by_id('dlbutton')
									button.click()

folders = {}
root = "G:\Downloads\comic"
def buildDatabase(path):
	for dirpath1, dirnames1, filenames1 in os.walk(os.path.join(root, path)):
		for r in filenames1:
			m1 = getMatcher(r)
			if(m1):
				folders[m1.group(0)] = dirpath1
				# print dirpath1, dirnames1, filenames1
				# .*?(?=(\s\d{1,4}.\d)?\s(\(.*?\)\s)?\(20\d{2}\))
				# .*?(?=\s\d{1,4})


buildDatabase("Valiant Comics")	
buildDatabase("Boom! Studios")
buildDatabase("DC Comics\The New 52\Limited Series")
buildDatabase("DC Comics\The New 52\Ongoing")
buildDatabase("Marvel\All-New Marvel NOW!\Ongoing")
buildDatabase("Marvel\All-New Marvel NOW!\Limited")
buildDatabase("Marvel\All-New Marvel NOW!\Global Events")
buildDatabase("Marvel\Icon")
buildDatabase("G:\Downloads\comic\Marvel\Star Wars")
buildDatabase("VERTIGO")
buildDatabase("Image")
buildDatabase("Dark Horse Comics")
buildDatabase("and other")

response = urllib2.urlopen('https://archive.moe/co/search/subject/Official%20Win-O\'-Thread/')
# print response.info()
html = response.read()
# print html
doc = h.fromstring(html)
ll= doc.xpath("//*/article[1]/div[2]/header/div/a[1]/@href")
new = ll[0]
# print ll
response1 = urllib2.urlopen(new)
thread = response1.read()
chan = h.fromstring(thread)
com = chan.xpath("//*/article/div/div[@class='text']/a/@href")
# print com
for url in com:
	if url.find("zippyshare.com/v/") != -1:
		# print url
		resp = urllib2.urlopen(url)
		flee = resp.read()
		name = h.fromstring(flee)
		op = name.xpath("//*/div[@id='lrbox']/div[@class='left']/font[3]/text()")
		dl = name.xpath("//*/div[@id='lrbox']/div[@class='right']/div/a/@id")
		new_com = op[0]
		try:
			downloadComic(new_com)

		except IndexError: 
			pic = getImage(url)
			urllib.urlretrieve(pic, "filename.png")
			img = Image.open("filename.png")
			img = img.resize((1200, 50), Image.ANTIALIAS)
			imageCom = image_to_string(img)
			downloadComic(imageCom)
