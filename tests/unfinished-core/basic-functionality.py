# VERSION: 20181208a
# By boot1110001.

### IMPORTS ############################################################
import os #for a lot of things
from os.path import expanduser #to get the HOME user dir in linux
import re #for regex
import urllib #to download websites
import urllib2 #to download websites
import datetime #to get the time
import subprocess #to execute BASH commands
from os import listdir #for list files in dir
from os.path import isfile, join #for list files in dir

### NON EDITABLE VARIABLES #############################################
HOME = expanduser("~") #to get the HOME user dir in linux
# time wehe this script is executed in format YYYY-mm-dd-HH-MM-SS
NOW = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


### EDITABLE VARIABLES #################################################
# Write the path to the directory where the APOD images will be saved.
APOD1_DIR = HOME+"/00617/apod-dybg-py/tests/apod1"
# Write the path to the directory where the AAPOD2 images will be saved.
APOD2_DIR = HOME+"/00617/apod-dybg-py/tests/apod2"


### CLASSES ############################################################
class BgImg:
	def __init__(self, distinct, url, loc_dir, now):
		patron = re.compile('\.(jpg|jpeg|png|gif)$')
		matcher = patron.findall(url)
		
		self.url = url
		self.distinct = distinct
		self.dir = loc_dir
		self.ext = matcher[0]
		self.fname = now+'-'+distinct+'.'+matcher[0]
		
	def get_loc(self):
		return self.dir+'/'+self.fname

	def to_string(self):
		print("My file name is: "+self.fname)
		print("My URL is: "+self.url)
		print("My localization is: "+self.get_loc())
		print("My directory is: "+self.dir)
		print("My distinct is: "+self.distinct)
		print("My extension is: "+self.ext)


### FUNCTIONS ##########################################################
def get_page1():
	print("Downloading the page to find the image...")
	web_content=urllib2.urlopen('http://apod.nasa.gov/apod/').read()
	patron=re.compile('.*<IMG SRC=\"(.*?)\"')
	matcher=patron.findall(web_content)
	return 'http://apod.nasa.gov/apod/'+matcher[0]
	
def get_page2():
	print("Downloading the page to find the image2...")
	web_content=urllib2.urlopen('http://www.aapodx2.com/').read()
	patron=re.compile('.*href=\"(.*?)\"><img')
	matcher=patron.findall(web_content)
	return 'http://www.aapodx2.com'+matcher[1]
	
def check_url(url):
	try:
		resp = urllib2.urlopen(url)
	except urllib2.URLError, e:
		if not hasattr(e,"code"):
			raise
		print "The URL '"+url+"' gave the error:", e.code, e.msg
		return False
	else:
		print "The URL '"+url+"' gave the code:", resp.code, resp.msg
		return True
	
def download_bg(bg):
	print("Downloading the image '"+bg.url+"' in '"+bg.get_loc()+"'...")
	urllib.urlretrieve(bg.url,bg.get_loc())
		
def set_as_bg(bg):
	# The program should detect the desktop environment and select the correct command.
	bashCommand = 'gsettings set org.gnome.desktop.background picture-uri file://'+bg.get_loc()
	print('CMD: '+bashCommand)
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

def clean_old_bgs(bg1,bg2):
	print("Cleaning the old background images from '"+APOD1_DIR+"':")
	apod1_files = [f for f in listdir(APOD1_DIR) if isfile(join(APOD1_DIR, f))] #save the names of the files in the dir in a list
	apod1_files.remove(bg1.fname)
	for dfile in apod1_files:
		print(" -removing: "+dfile)
		os.remove(APOD1_DIR+'/'+dfile)

	print("Cleaning the old background images from '"+APOD2_DIR+"':")
	apod2_files = [f for f in listdir(APOD2_DIR) if isfile(join(APOD2_DIR, f))] #save the names of the files in the dir in a list
	apod2_files.remove(bg2.fname)
	for dfile in apod2_files:
		print(" -removing: "+dfile)
		os.remove(APOD2_DIR+'/'+dfile)
	
def clean_tmp_files():
	print("Cleaning temporary files...")
	# Temporary files are not yet saved.
	
#¡¡Function that builds a BgImg from the name of an existing file in the folder!!

### MAIN ###############################################################
url1=get_page1()
url2=get_page2()

if (check_url(url1) and check_url(url2)):
	print("The two URLs are correct and work well.")
	bg1 = BgImg('apod1',url1,APOD1_DIR,NOW)
	bg1.to_string()
	bg2 = BgImg('apod2',url2,APOD2_DIR,NOW)
	bg2.to_string()

	download_bg(bg1)
	download_bg(bg2)

	set_as_bg(bg1)
	# ~ #set_as_bg(bg2)
	clean_old_bgs(bg1,bg2)
elif (check_url(url1)):
	print("The AAPOD2 URL gave an error, ending...")
elif (check_url(url2)):
	print("The APOD URL gave an error, ending...")
else:
	print("The two URLs gave an error, ending...")

