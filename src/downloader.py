import urllib2, os, time
class Download:
    def __init__(self,url,file_name):
        self.url = url
        self.file_name=file_name
        self.file = open(self.file_name, 'ab')
        self.current_file_size = os.stat(self.file_name).st_size
        self.download_block_size = 8192
    def now(self):
        try:                        
            req = urllib2.Request(self.url)
            already_downloaded_size = self.current_file_size
            if(self.current_file_size>0):
                temp = urllib2.urlopen(self.url).info()
                actual_file_size = int(temp.getheaders("Content-Length")[0])
                if self.current_file_size >= actual_file_size:                    
                    return True
                # file is already there and have some data downloaded  to it (file-size is present in 'self.current_file_size')
                req.add_header('Range', 'bytes=%d-' % self.current_file_size)
                print "[Resuming -- %3.2f MB] : %s"%(self.current_file_size/1048576., self.file_name)
            else:
                print "[Saving] : %s" %(self.file_name)
            req.add_header('User-Agent','fluid v1.0.5')
            req = urllib2.urlopen(req)            
            header = req.info()
            actual_file_size = int(header.getheaders("Content-Length")[0])
            actual_file_size += self.current_file_size
            print("[SIZE] : %3.2f"%(actual_file_size/1048576.))
            clk_start = time.clock()                       
            while True:
                buffer = req.read(self.download_block_size)
                if not buffer:
                    break
                already_downloaded_size += len(buffer)
                self.file.write(buffer)
                done = int(50 * already_downloaded_size / actual_file_size)
                dlMB = float(already_downloaded_size/1048576.)
                print("\r[PROGRESS] : [%3.2f%%] [%3.2f MB] [%s%s] [%3.2fKbps]" %((already_downloaded_size*100./actual_file_size), dlMB, '#' * done, '.' * (50-done), (dlMB*1024/(time.clock() - clk_start)) ) ),            
        except Exception as e:
            print e
        finally:
            self.file.close()
            if already_downloaded_size == actual_file_size :
                return True
            return False
