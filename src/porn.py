from downloader import Download
from util import Tools
from bs4 import BeautifulSoup
import urllib2,os
class PornHub:
	'this module is only for Porn-Hub '
	def __init__(self):
		self.helper = Tools()
		self.MAIN_FILE = "%s\MAIN_PH.list" %(os.getenv('APPDATA'))			
		self.TBD_FILE = "%s\TBD_PH.list" %(os.getenv('APPDATA'))
		self.ARCHIVE_FILE = "%s\ARCHIVE_PH.list" %(os.getenv('APPDATA'))
		
	def PH_extractor_(self,resp):
		try:
			parse_tree = BeautifulSoup(resp,"html.parser")			
			tag_finder = parse_tree.findAll("li", {"class" : "videoblock"})
			del resp, parse_tree
			for each_tag in tag_finder:
				link = str(each_tag['_vkey'])				
				if not self.helper.find_link(self.MAIN_FILE,link):
					self.helper.append_link(self.MAIN_FILE,link)
					self.helper.append_link(self.TBD_FILE,link)
			del tag_finder
		except:
			#may be bad connection will try later :)
			pass
				
	def _fetch_CDN_(self,resp):		
		if 'alt="Upgrade to Pornhub Premium to enjoy this video."' in resp:
			#upgrade to premium message with nothing to fetch just remove that link from file and move on
			return True
		if 'var player_quality_' in resp:			
			p720 = resp.find('var player_quality_720p = \'')
			if p720 == -1:
				p420 = resp.find('var player_quality_480p = \'')
				if p420 == -1:
					p240 = resp.find('var player_quality_240p = \'')
					if p240 == -1:
						#nothing is there
						print("\n[None] No Video Format could be found -- Removing the Link")
						return True
					else:
						print("[FETCHED -- 240px]")
						start = p240 + 27
						end = resp.find('\'',p240+30)
				else:
					print("[FETCHED -- 420px]")
					start = p420 + 27
					end = resp.find('\'',p420+30)
			else:
				print("[FETCHED -- 720px]")
				start = p720 + 27
				end = resp.find('\'',p720+30)
			#print resp[start:end]				
			file_name = BeautifulSoup(resp,"html.parser")
			file_name = str(file_name.title.string)
			file_name = file_name.translate(None,"'*:\"\/?<>|")
			download = Download(resp[start:end],"%s.mp4"%(file_name))
			download = download.now()			
			if download:				
				return True
			return False
		else:
			pass
	def __prepare__(self):
		#this will run into infinite loop until there is nothing in the ToBeDownloaded.list file
		while os.stat(self.TBD_FILE).st_size>0:
			link = self.helper.get_me_link(self.TBD_FILE)
			print("\n[Downloading] : http://www.pornhub.com/view_video.php?viewkey=%s" %(link))
			resp = urllib2.Request("http://www.pornhub.com/view_video.php?viewkey=%s"%(link))
			resp.add_header('Cookie',"RNKEY=1043543*1527941:2834309375:3318880964:1;")
			try:
				resp = urllib2.urlopen(resp).read()
				self.PH_extractor_(resp)
				rc=self._fetch_CDN_(resp)
				if rc==True:
					self.helper.remove_link(self.TBD_FILE,link)
					self.helper.append_link(self.ARCHIVE_FILE,link)
					print("\n[WIN] : File Download Complete!")
				else:
					print("\n[ERROR] : Something went wrong!")
			except Exception as e:
				print e
