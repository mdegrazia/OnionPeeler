#Mari DeGrazia
#arizona4n6@gmail.com
#This script uses OnionPy to batch query the Tor nodes through the Onionoo API
#with a list of IP addresses and outputs the results into a csv file.
#The list of IP address must be in a text file, one per line

try:
	from onion_py.manager import Manager
	from onion_py.caching import OnionSimpleCache
except:
	print "OnionPy must be installed. Try pip install OnionPY"

from Tkinter import *
from tkFileDialog   import askopenfilename,asksaveasfilename
import tkMessageBox
import ttk
import os
import winsound

import csv
import sys

def openfile():
	file1= askopenfilename() 
	ttk.e1.insert(10,file1)
        
def savereport():
	file2= asksaveasfilename(initialfile="report.csv",defaultextension=".csv")
	ttk.e2.insert(10,file2)
	
def About():
	tkMessageBox.showinfo("About", "Onion Peeler v.1\nMari DeGrazia\narizona4n6@gmail.com")
def Help():
	tkMessageBox.showinfo("Help", "This program will query the OnionOO Tor API status to see if there are any matches in a list of IP addresses. It takes a plain text file, one IP address per line for input.")
		
def lookup():

	input_file = ttk.e1.get()
	output_file = ttk.e2.get()
	count = 0
	
	
	try:
		outfile = open(output_file,"w")
		
	except:
		tkMessageBox.showinfo("Error", "Could not open output file. Verify the file is not currently open.")
		return
	outfile.write("Provided IP,Nickname,Tor Address,Running,Fingerprint\n")
	
	master.config(cursor="wait")
	master.update()



	try:
		manager = Manager(OnionSimpleCache())
		s = manager.query('summary')
	except:
		tkMessageBox.showinfo("Issues Accessing Tor Database", "Check to make sure you have Internet access then try again,or site may be down.")
		return

	
	with open(input_file,'r') as f:
		IPs = f.read().splitlines()
	for relay in s.relays:
		for address in relay.addresses:
			#print relay.nickname + "," + address
			for IP in IPs:
				#print "\t" + IP
				if IP in address:
					if relay.nickname is not None:
						nickname = relay.nickname
					else:
						nickname = "BLANK"
					if relay.fingerprint is not None:
						fingerprint = relay.fingerprint
					else:
						fingerprint = "BLANK"
					
					outfile.write(IP + "," + nickname + "," + address + "," + str(relay.running) + "," + fingerprint + "\n")
					count = count + 1
					#exit this loop now that we found a hit
					break
	
	master.config(cursor="")          
	winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
	tkMessageBox.showinfo("Completed", "Found " + str(count) + " Tor matches ")


if __name__ == '__main__':	


	script_path = os.path.realpath(__file__)
	script_path = os.path.dirname(script_path)
	resources_path = os.path.join(script_path,"resources")
	
	master = Tk()
	master.wm_title("Onion Peeler - Batch Tor IP Checker")
	
	icon = os.path.join(resources_path,"onion.ico")

	if os.path.exists(icon):
		master.iconbitmap(icon)
		
	menu = Menu(master)
	master.config(menu=menu)
	helpmenu = Menu(menu)
	menu.add_cascade(label="Help", menu=helpmenu)
	helpmenu.add_command(label="Help...", command=Help)
	helpmenu.add_command(label="About...", command=About)

	ReportType = IntVar()
	ReportType.set(1) 

	ttk.Label(master, justify=LEFT,text="Takes a text file, one IP address per line and checks them against the current Tor Relays and Bridges").grid(row=0,column=0,columnspan=3,sticky=W)

	ttk.Separator(master,orient=HORIZONTAL).grid(row=6, columnspan=3,sticky="ew",pady=10)

	ttk.Button(text='Open IP list...',command=openfile,width=20).grid(row=7,column=0,sticky=W)
	ttk.e1 = Entry(master,width=50)
	ttk.e1.grid(row=7, column=1,sticky=E)

	ttk.Button(text='Save Report...',command=savereport,width=20).grid(row=8,column=0,sticky=W)
	ttk.e2 = Entry(master,width=50)
	ttk.e2.grid(row=8, column=1,sticky=E)

	ttk.Button(text='Process', command=lookup,width=20).grid(row=9,column=0,sticky=W)

	ReportType = IntVar()
	ReportType.set(1) 

	mainloop( )


