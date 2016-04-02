from bs4 import BeautifulSoup
import urllib2, os
class Tools:
	def __init__(self):
		if not os.path.exists("%s\MAIN_PH.list" %(os.getenv('APPDATA'))):
			print("[WELCOME] First Run! ")
			open("%s\MAIN_PH.list" %(os.getenv('APPDATA')),"w")
		if not os.path.exists("%s\TBD_PH.list" %(os.getenv('APPDATA'))):
			print("[PREPARING] Files")
			open("%s\TBD_PH.list" %(os.getenv('APPDATA')),"w")
		if not os.path.exists("%s\ARCHIVE_PH.list" %(os.getenv('APPDATA'))):
			print("[DONE] okay Jack we are done ! here we go !")
			open("%s\ARCHIVE_PH.list" %(os.getenv('APPDATA')),"w")
		
	def find_link(self,file_path,link):
		# this will check if the given link is there in the provided file link
		file_object = open(file_path,'rb')
		data = file_object.read()
		data = data.split()
		file_object.close()
		del file_object
		if str(link) in data:
			return True
		return False

	def append_link(self,file_path,link):
		#this will add a new link to the provided file at the end of the file 
		try:
			file_object = open(file_path,'rb')
			data = file_object.read()
			data += "%s "%(str(link))
			file_object.close()
			file_object = open(file_path,'wb')
			file_object.write(data)
			file_object.close()
			del file_object, data
			return True
		except:
			return False

	def remove_link(self,file_path,link):
		try:
			file_object = open(file_path,'rb')
			data = file_object.read()
			data = data.split()
			data.remove(link)
			data = ' '.join(data)
			data += " "
			file_object.close()
			file_object = open(file_path,'wb')
			file_object.write(data)
			file_object.close()
			del data, file_object
			return True
		except:
			return False
				
	def get_me_link(self,file_path):
		file_object = open(file_path,'r')
		data = file_object.read()
		file_object.close()
		del file_object
		if not data:
			return '0'
		else:
			d = data.split()
			del data
			return d[0]
