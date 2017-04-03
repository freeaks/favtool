#!/usr/bin/env python3
import tkinter
import base64
import os
import urllib.request
import bs4 as bs
import sys
import requests
from tkinter import ttk
from tkinter import *
from PIL import Image
#from bs4 import BeautifulSoup 
#from pyfav import download_favicon

class App(object):

    def __init__(self):
        self.root = tkinter.Tk()
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.root.title('bookmark generator')

        self.mydatabase = os.path.expanduser('~')+'/Documents/mydatabase'
        self.mybookmark = os.path.expanduser('~')+'/Documents/mybook.html'

        self.frm = ttk.Frame(self.root)
        self.frm.grid(column=0, row=0, sticky='nsew')

        self.site_name = StringVar()
        self.site_link = StringVar()
        self.site_nubr = StringVar()

        # check if DB file exists, if so get numbers of bookmarks stored in it
        try:
            myfile = open(self.mydatabase)
        except:
            self.site_nubr = 0
        else:
            self.site_nubr = self.line_count(self.mydatabase)

        self.label_name = ttk.Label(self.frm, text='Site name:')
        self.label_name.grid(column=0, row = 2, sticky=W)
        self.label_link = ttk.Label(self.frm, text='Site link:')
        self.label_link.grid(column=0, row = 3, sticky=W)
        self.label_nbr1 = ttk.Label(self.frm, text='Total site')
        self.label_nbr1.grid(column=0, row = 4, sticky=W)
        self.label_nbr2 = ttk.Label(self.frm, text=str(self.site_nubr))
        self.label_nbr2.grid(column=1, row = 4, sticky=W)

        self.entry_name = ttk.Entry(self.frm, text=self.site_name, width=50)
        self.entry_name.grid(column=1, row = 2)
        self.entry_link = ttk.Entry(self.frm, text=self.site_link, width=50)
        self.entry_link.grid(column=1, row = 3)

        button_make = ttk.Button(self.frm, text='Make bookmark')
        button_make['command'] = self.write_book
        button_make.grid(column=0, row = 5, sticky=W)

        button_add = ttk.Button(self.frm, text='Add site DB')
        button_add['command'] = self.store_link
        button_add.grid(column=1, row = 5, sticky=W)

        button_clear = ttk.Button(self.frm, text='Clear')
        button_clear['command'] = self.clear_entry
        button_clear.grid(column=1, row = 5, sticky=E)


        for child in self.frm.winfo_children(): child.grid_configure(padx=5, pady=5)

    def clear_entry(self):
        self.entry_name.delete(0, 'end')
        self.entry_link.delete(0, 'end')

    def line_count(self, filename):
        num_lines = sum(1 for line in open(filename))
        self.site_nubr=num_lines
        return num_lines

    def get_icon(self, mylink):
        # get site favicon and rename it to 'favicon.ico'
        try:
            print("trying to download icon")
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(mylink,headers=hdr)
            page = urllib.request.urlopen(req).read()
            soup = bs.BeautifulSoup(page,'lxml')
            icon_link = soup.find("link").get("href")
            print(icon_link)

            # urllib gives "urllib.error.HTTPError: HTTP Error 403: Forbidden"
            # using 'requests' instead of urllib
            # urllib.request.urlretrieve(icon_link, os.path.join("/tmp/favicon.ico"))

            r = requests.get(icon_link)
            with open('/tmp/favicon.ico', 'wb') as outfile:
                outfile.write(r.content)

        except:
            print("couldn't get icon", sys.exc_info()[0])
            raise
            

    def store_link(self):
        # grab data from tkinter entry fields
        site_name = self.site_name.get()
        site_link = self.site_link.get()

        # get site icon
        self.get_icon(site_link)

        # if icon exists, convert to png, resize and encode it to base64, else use default icon.
        try:
            im = Image.open('/tmp/favicon.ico')
            im.save('/tmp/temp.png', 'PNG', progressive=True, quality=100)
            im.close()
            im = Image.open('/tmp/temp.png')
            im.thumbnail((16,16),Image.BICUBIC)
            im.save('/tmp/favicon.ico', 'PNG', progressive=True, quality=100)
            im.close()
            with open("/tmp/favicon.ico", "rb") as f:
                data = f.read()
                result = base64.b64encode(data).decode('ascii')
        except:
            print("using default icon")
            result="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAByklEQVR4nI2TO2hUQRSGv13TiZUPUogKEWMasRIrK5sBCyUXG7FIJzoWQWy02E0trClWMKvZJtu5YAKBC4KgEJtgEWMgSwhCMMgWyyKkuNnNzD0Wc5/JDTgwMHDO98+ZM+cvUbCURgD8rs4H2vXS4dyRIrBRa2LDASufuwDsjD/D2JAKLl4khNLIH9OS38OmfPl7XT71xmS5e04+7p4SpRE+/JLKRl8q633B05KrQGlkfrbFzv4cA7PHMNoHJuDABi7TCDNrfTAhlRdVZkBo10vlWOk42FjjEqyACZ3Qai+pvKw00qg1j4UXauDf3E7geLemToOn5cT2BV3tfHvJjVsn/xtWnQnGbn/FdlZdD7Ye9nhdPQPA1PMRjDWEcZsK4LuPQCTTxL3AsHJnl2Bg4dVFHkyTESiG43gZINg3BAOLGVrABSU8KuBf2mDxbRTPVpDARtybZy9z/+lhAfcUf3QdGtcAN6luojwtTE7nvkqtjeNf3czBGIlyBDbfQ7teSkc5gtX3KwBMPgHeTLibzv/MwzYZRNKZ9rSo0TqeTpskoTsvzYF/9kcKb80nfsibIhK59ziF44Ytv8u4M2Omo64idWV2+V1d6MJ/2Gdk/bHzufAAAAAASUVORK5CYII%3D"

        # bookmark final string
        mystring="<div><a href="+site_link+"><img src='data:image/png;base64,"+result+"' width=16 height=16 >&nbsp;"+site_name+"</a></div>&nbsp;"

        # store bookmark in DB file
        myfile = open(self.mydatabase, "a")
        print(mystring,file=myfile)
        myfile.close()

        # if previous icon exits, delete it
        try:
            fullpath = os.path.join("/tmp", "favicon.ico") 
            os.remove(fullpath)
            fullpath = os.path.join("/tmp", "temp.png")
            os.remove(fullpath)
        except:
            print("couldn't delete previous icons")

        # increase bookmark total count
        self.site_nubr+=1
        self.label_nbr2['text']=self.site_nubr


    def write_book(self):
        html_header="""<html><head><style>
            .container {
            display: flex;
            flex-direction: column;
            align-content: flex-start;
            flex-wrap: wrap;
            height:92vh;
            vertical-align:top;
            }
            .container div {
            height: 15px;
            width: 160px;
            }
            a:link {text-decoration: none;}
            </style></head><body><div class=container>"""
        html_footer='</div></body></html>'
        mydata = open(self.mydatabase, "r")
        myfile = open(self.mybookmark,'w')
        print(html_header,file=myfile)
        for line in mydata:
            print(line,file=myfile)
            
        print(html_footer,file=myfile)
        mydata.close()
        myfile.close()


app = App()
app.root.mainloop()