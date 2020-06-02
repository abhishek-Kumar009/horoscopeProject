#Import modules 
import bs4 as bs
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import pytube

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()
    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished!')
    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

#List to store the video links in the playlist
def startDownloadingPlaylist(url, downloadPath):
    links = []    
    page = Page(url)
    

    #/Extract the <a> tags's href and store it in links
    soup = bs.BeautifulSoup(page.html, "html.parser")
    
    for link in soup.find_all('a', id='wc-endpoint'):    
        cLink = link.get('href')
        exact_link = 'https://www.youtube.com'+cLink
        links.append(exact_link)
    
    #Use pytube to download from the links aggregated from the playlist
    
    for link in links:
        yt = pytube.YouTube(link)
        stream = yt.streams.filter(type = 'audio').first()
        try:
            print('Downloading... ', link)
            stream.download(downloadPath)
            print('Downloaded successfully from: ',link)
        except:
            print('Error while downloading with the stream!', link)

#Start the process
url = 'https://www.youtube.com/watch?v=ehchYzwEc2I&list=PLZdXRHYAVxTLYYHcnBePxwYHuR_p-iRoX&index=1'
downloadPath = '/home/abhishek/Desktop/Coding_Stuffs/horoscopeProject'
startDownloadingPlaylist(url, downloadPath)

    
    
    