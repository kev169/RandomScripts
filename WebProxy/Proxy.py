__author__ = 'Kevin Haubris'

from gi.repository import Gtk as gtk
import httplib
from urlparse import urlparse
import sys
import libs.SQLLib as SQLLib
import os
import socket
from threading import Thread
from multiprocessing import Manager
import thread

PORT = 8080
global webpagedict
webpagedict = Manager().dict()
global webpages
webpages = Manager().list()
gladefile = "./Data/Design/StartGui.glade"
global proxy
global httpd
global gclass
global proxygoing
proxygoing = Manager().dict()


def handler(clientsock, addr):
    #while proxygoing["socket"] != 1:
    data = clientsock.recv(2056)
    #print 'data:' + repr(data)
    requestdatain = data
    page = ""
    headers = {}
    if data != "":
        for item in data.split("\r\n"):
            if "GET" in item:
                page = item.split(" ")[1]
                #print(page)
            if "user-agent" in item.lower():
                #print(item)
                headers["User-Agent"] = item.replace(item.split(":")[0]+":", "").strip()
                #print(headers["User-Agent"])
        if page != "" and page.startswith("htt"):
            webpages.append(page)
            #print(headers["User-Agent"])
            location = urlparse(page)
            netloc = "{uri.netloc}".format(uri=location)
            #print(netloc)
            if netloc not in webpagedict.keys():
                webpagedict[netloc] = []
            #opener.addheaders = [('User-Agent', headers["User-Agent"])]
            conn = httplib.HTTPConnection(netloc)
            conn.request("GET", "{uri.path}".format(uri=location), headers=headers)
            data = conn.getresponse()
            inheaders = str(data.getheaders())
            html = data.read()
            gclass.UpdateSites("")
            #SQLHandle.InsertSite(netloc, page, requestdatain, "", html, inheaders)
            gclass.PopulateRequest((netloc, page, requestdatain, "", html, inheaders))
            clientsock.send("HTTP/1.1 "+str(data.status)+" "+str(data.reason) +"\r\n"+inheaders+"\r\n\r\n"+html)
    clientsock.close()


def proxyThread():
    proxygoing["started"] = 0
    ADDR = ('', PORT)
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.bind(ADDR)
    serversock.listen(5)
    while "socket" not in proxygoing.keys():
        #print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        #print '...connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))
    serversock.close()
    sys.exit()


class WindowHandler:

    def run(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.show_all()
        self.treecalled = 0
        gtk.main()

    def onDeleteWindow(self, *args):
        global proxygoing
        proxygoing["socket"] = 1
        if "started" in proxygoing.keys():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 8080))
            s.send("exit")
            s.close()
        gtk.main_quit(*args)

    """def PopulateList(self, variable):
        name_store = gtk.TreeStore(int,str)
        for count, item in enumerate(self.data):
            name_store.append(count, item)
        comboview = self.builder.get_object("combobox1")
        comboview.set_model(name_store)"""

    def AboutButton(self, *args):
        #print("Hit About")
        abuilder = gtk.Builder()
        abuilder.add_from_file(gladefile)
        abuilder.connect_signals(WindowHandler())
        awindow = abuilder.get_object("aboutdialog1")
        awindow.show_all()
        gtk.main()

    def StartProxy(self, *args):
        #httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
        print("serving at port %s" % (PORT))
        #httpd.serve_forever()

    def PopulateRequest(self, args):
        netloc, page, requestdatain, requestheader, html, inheaders = args
        requesttext = self.builder.get_object("textview2")
        requesttext.get_buffer().set_text(str(requestheader)+str(requestdatain))
        responsetext = self.builder.get_object("textview3")
        responsetext.get_buffer().set_text(str(inheaders)+str(html))

    def UpdateSites(self, *args):
        self.treestore = gtk.TreeStore(str)
        treeview = self.builder.get_object("treeview1")
        for item in webpagedict.keys():
            toplayer = self.treestore.append(None, ['%s' % item])
            #print(item)
            for it2 in webpages:
                if item in it2:
                    #print(it2)
                    self.treestore.append(toplayer, ['%s' %(it2)])
        treeview.set_model(self.treestore)
        self.cell = gtk.CellRendererText()
        tcolumn = gtk.TreeViewColumn("Sites")
        tcolumn.pack_start(self.cell, True)
        tcolumn.add_attribute(self.cell, 'text', 0)
        if self.treecalled != 1:
            self.treecalled = 1
            treeview.append_column(tcolumn)


if __name__ == "__main__":
    proxy = Thread(target=proxyThread, args=())
    proxy.start()
    #global SQLHandle
    #SQLHandle = SQLLib.SqlCommands()
    #SQLHandle.CreateDB()
    global gclass
    gclass = WindowHandler()
    gclass.run()
    proxy.join()
    sys.exit()


