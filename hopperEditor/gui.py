#!/usr/bin/env python3
from gi.repository import Gtk
import os
import sys

class gui:
    def __init__(self, inputfile = ""):
       self.nothing = ""
       self.inputfile = inputfile
       self.data = ""
       self.functiontext = ""
       self.treecalled = 0
       self.label1data = ""

    def run(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("./lib/gui.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.show_all()
        if self.inputfile != "":
            #print(self.inputfile)
            self.window.set_title(self.inputfile.split("/")[-1])
            fin = open(self.inputfile, "r")
            self.data = fin.read()
            fin.close()
        self.window.set_title("HopperEditor")
        mytextview = self.builder.get_object("textview1").get_buffer()
        mytextview.set_text(self.data)
        self.SetupTree()
        Gtk.main()

    def SetupTree(self):
        self.treestore = Gtk.TreeStore(str)
        self.functionNames = []
        self.treestore.append(None, ['Full Code'])
        self.functionNames.append('Full Code')
        for item in self.data.split("\n"):
            if "function " in item:
                functionName = item.replace("function ", "").split("(ARG")[0]
                #print("Function %s"%(functionName))
                self.treestore.append(None, ['%s'%(functionName)])
                self.functionNames.append(functionName)
        treeview = self.builder.get_object("treeview1")
        treeview.set_model(self.treestore)
        self.cell = Gtk.CellRendererText()
        tcolumn = Gtk.TreeViewColumn('Test')
        tcolumn.pack_start(self.cell, True)
        tcolumn.add_attribute(self.cell, 'text', 0)
        if self.treecalled == 0:
            treeview.append_column(tcolumn)
            self.treecalled = 1 

    def GetValue(self, var, x,y):
        #print("Values %s"%(str(x)))
        #print(self.functionNames[int(str(x))])
        label1 = self.builder.get_object("label1")
        self.label1data = self.functionNames[int(str(x))]
        if self.label1data != 'Full Code':
            label1.set_text(self.label1data)
            self.functiontext = "function %s"%(self.label1data) + self.data.split("function %s"%(self.label1data))[1].split("function")[0]
            mytextview = self.builder.get_object("textview1").get_buffer()
            mytextview.set_text(self.functiontext)
        else :
            mytextview = self.builder.get_object("textview1").get_buffer()
            mytextview.set_text(self.data)


    def ExitFunc(self, *args):
        #print("Called exit")
        Gtk.main_quit(*args)
    
    def OpenFile(self, var):
        #print("Called OpenFile")
        dialog = Gtk.FileChooserDialog("Please choose a file", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_current_folder(os.path.expanduser("~"))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            openfilename = dialog.get_filename()
            #print(openfilename)
            self.window.set_title(openfilename.split("/")[-1])
            fin = open(openfilename, "r")
            self.data = fin.read()
            fin.close()
            mytextview = self.builder.get_object("textview1").get_buffer()
            mytextview.set_text(self.data)
            self.SetupTree()

        dialog.destroy()

    def SaveFile(self, var):
        dialog = Gtk.FileChooserDialog("Save File As...", None,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        dialog.set_current_folder(os.path.expanduser("~"))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            savefilename = dialog.get_filename()
            if not savefilename.endswith(".pseu"):
                savefilename = savefilename + ".pseu"
            #print(savefilename)
            fout = open(savefilename, "w")
            fout.write(self.data)
            fout.close()
            
        dialog.destroy()

    def RenameFunc(self, var):
        #print("Hit Rename")
        entry1 = self.builder.get_object("entry1")
        entryvalue = entry1.get_text()
        #print(entryvalue)
        self.data = self.data.replace(self.label1data, entryvalue)
        self.SetupTree() 
        self.functiontext = self.data.split("function %s"%(entryvalue))[1].split("function")[0]
        mytextview = self.builder.get_object("textview1").get_buffer()
        mytextview.set_text(self.data)
        #mytextview = self.builder.get_object("textview1").get_buffer()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test = gui(sys.argv[1])
    else :
        test = gui()
    test.run()
