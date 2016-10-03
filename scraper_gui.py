from Tkinter import *
from tkSimpleDialog import askstring
from tkFileDialog   import asksaveasfilename
import re
import string
import os
from scraper import MetacriticScraper
from tkMessageBox import askokcancel

class Quitter(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)
    def quit(self):
        ans = askokcancel('Verify exit', "Really quit?")
        if ans: Frame.quit(self)

class OuterFrame(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)


class ScrapeWindow(OuterFrame):
    def __init__(self, parent=None, file=None):
    	self.scraper = MetacriticSpider('http://www.metacritic.com')
    	self.selected = {}
    	self.results_window = None
    	
    	self.root = Frame(parent)
        self.root.pack(fill=X)
        
        Quitter(self.root).pack(side=BOTTOM)
        OuterFrame.__init__(self, parent, file=file)
        
        self.url_display = Label(self.root, text = 'URL: \n')
        self.url_display.pack()
        
        self.make_button_menu(self.root, self.scraper.jury_dict, 'jury', 'jury').pack()
        self.make_button_menu(self.root, self.scraper.verdict_dict, 'verdict', 'verdict').pack()
        
        entry_bar = Frame(self.root)
        entry_bar.pack()

        self.search_entry = self.make_search_entry(entry_bar)
        self.search_entry.bind("<Return>", self.search_event)
        
        self.page_entry = self.labeled_entry_field(entry_bar, "Number of pages")
        self.page_entry.pack()
        self.page_entry.bind("<Return>", self.scrape)
        self.page_entry.bind('x', self.x_press)
        
        Button(self.root, text='Scrape',  command=self.onScrape).pack()
    
    def save(self, scraped_text):
    	path = 'texts/'
    	print path
    	s = self.scraper
    	movie = self.selected['result'].replace(' ', '_')
    	path += movie
    	print path
    	if not os.path.isdir(path):
    		os.makedirs(path)
    	path += '/%s' % self.selected['jury']
    	print path
    	if not os.path.isdir(path):
    		os.makedirs(path)
    	path += '/%s' % self.selected['verdict']
    	print path
    	outfilename = path
    	outfile = open(outfilename, 'w')
    	outfile.write(scraped_text)
    	
    def x_press(self, event):
    	print("You hit x.")
    
    def search_event(self, event):
    	self.onSearch(self.search_entry.get())
    
    def scrape(self, event):
    	text = self.scraper.scrape_review_set(self.getURL(), int(self.page_entry.get()))
    	print text
    	self.save(text)
    
    def labeled_entry_field(self, parent, labeltext):
    	entry_field = Frame(parent)
    	Label(entry_field, text = labeltext).pack()
    	entry = Entry(entry_field, bd = 1, width = 5)
    	entry_field.pack()
    	return entry
    	
    def make_search_entry(self, parent):
    	search_box = Frame(parent)
        search_box.pack(side = TOP)
        
        search_label = Label(search_box, text="search term")
        search_entry = Entry(search_box, bd = 5)
        
        search_label.pack()
        search_entry.pack()
        Button(search_box, text='Search',  command= lambda: self.onSearch(search_entry.get())).pack()
        search_box.pack()
        return search_entry
    
    def make_button_menu(self, parent, dictionary, title, var):
    	panel = Frame(parent)
    	Label(panel, text = title).pack()
    	
    	ref_list = []
    	for key in dictionary:
    		b = Radiobutton(panel, text=key, variable=var, value=key, command = lambda key=key: self.configure_settings(var, key))
    		ref_list.append(b)
    		b.pack(anchor=W)
    	ref_list[0].invoke()
    	return panel
    
    def onSearch(self, search_term):
    	if self.results_window is not None:
            self.results_window.destroy()
    	self.results_window = Frame(self.root)
    	result_dict = self.scraper.get_search_results(search_term)
    	self.scraper.result_dict = result_dict
    	menu = self.make_button_menu(self.results_window, result_dict, 'select movie', 'result')
    	menu.pack(side = TOP)
    	self.results_window.pack()
    
    def getURL(self):
    	s = self.scraper
    	url = s.start_url + s.result_dict[self.getSelectedResult()] + s.jury_dict[self.getJuryMode()] + s.verdict_dict[self.getVerdictMode()]
    	print url
    	new_msg = 'URL:\n%s' % url
    	self.url_display.configure(text = new_msg)
    	return url
    
    def onScrape(self):
    	print self.scraper.scrape_review_set(self.getURL(), int(self.page_entry.get()))
    
    def configure_settings(self, var_name, new_value):
    	self.selected[var_name] = new_value
    
    def getJuryMode(self):
    	return self.selected['jury']
    
    def getVerdictMode(self):
    	return self.selected['verdict']
    
    def getSelectedResult(self):
    	return self.selected['result']
    

        
ScrapeWindow().mainloop()