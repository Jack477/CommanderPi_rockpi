#!/usr/bin/python
import sys
import os
import resources as rs
import update as up
import tkinter as tk
import theme as th
import importlib
import webbrowser
from tkinter import messagebox as msb
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

### TODO: Move change_theme function to theme.py?
### split resources.py into smaller files
### move window_list from theme.py to resources
home_path = sys.argv[1]
def change_theme(master):
	if int(th.color_mode)==0:
		print("Setting color theme to 1")
		th.color_mode=1
	else:
		th.color_mode=0
	rs.config.set('DEFAULT', 'color_mode', str(th.color_mode))
	with open(home_path+'/CommanderPi/src/cpi.config', 'w') as configfile:
		rs.config.write(configfile)
	th.set_theme(master)
	#print(th.color_mode)

### Use in window class: master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
def on_Window_Close(master):
	if isinstance(master, tk.Tk):
		window_name = master.__class__
		print(window_name)
		th.window_list.pop()
	master.destroy()

### Using to keybind window kill
def killwindow(event, master):
	on_Window_Close(master)

### Open new window with his own master
def bopen(window):
	x = window()


class Network_Window:
	def __init__(master):
		master = tk.Tk()
		master.geometry("480x310")
		master.title("Commander Pi")
		th.window_list.append(master)


		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open(home_path+"/CommanderPi/src/icons/Networkings.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  Networking", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
			
		network_frame = Frame(mainframe)
		network_frame.pack()
		
		ether_title = tk.Label(network_frame, text="Ethernet:", font=("TkDefaultFont", 11, "bold"))
		ether_title.grid(row=0, column=0)
		
		wlan_title = tk.Label(network_frame, text="WiFi:", font=("TkDefaultFont", 11, "bold"))
		wlan_title.grid(row=0, column=1)
		
		ether_label = tk.Label( network_frame, text = rs.eth0_data, borderwidth=2, relief="groove", height=7, width=25, anchor='w', justify=LEFT )
		ether_label.grid(row=1, column=0, sticky = W)
		
		wlan_label = tk.Label( network_frame, text = rs.wlan0_data, borderwidth=2, relief="groove",  height=7, width=25, anchor='w', justify=LEFT )
		wlan_label.grid(row=1, column=1, sticky = W)
		
		cc_frame = Frame(mainframe)
		cc_frame.pack()

		actual_country_code = tk.Label( cc_frame, text="Your country code: "+rs.get_country_code(), font=("TkDefaultFont", 11, "bold"))
		actual_country_code.grid(row=0, column=0, columnspan=2)

		country_code_label = tk.Label( cc_frame, text="Set your country code", font=("TkDefaultFont", 11, "bold"))
		country_code_label.grid(row=1, column=0, columnspan=2)

		country_code_entry = tk.Entry( cc_frame, justify=CENTER, width=5)
		country_code_entry.grid(row=2, column=0, sticky=E)

		country_code_button = tk.Button( cc_frame, text="Apply", command=lambda:push_cc(), font=("TkDefaultFont", 10, "bold"), cursor="hand2")
		country_code_button.grid(row=2, column=1)

		bind_label = tk.Label( mainframe, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(side=BOTTOM)

		def push_cc():
			code = country_code_entry.get()
			if isinstance(code, str) and len(code) == 2:
				code = code.upper()
				rs.set_country_code(code)
				actual_country_code.configure(text="Your country code: "+rs.get_country_code())
				msb.showinfo(title="Done!", message="Your country code is now set as "+code)
			else:
				msb.showwarning(title="Error", message="Country code should be two letters!")

		th.set_theme(master)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
		master.mainloop()			

	

class Proc_Info_Window:

	def __init__(master):
	
		master = tk.Tk()
		master.geometry("350x400")
		master.title("Commander Pi")
		th.window_list.append(master)
		th.set_theme(master)
		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open(home_path+"/CommanderPi/src/icons/CPUs.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  CPU Details", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
	
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=15)
		
		cpu_content_frame = Frame(mainframe)
		cpu_content_frame.pack(fill=X)
		
		cpu_label = tk.Label( cpu_content_frame, text = rs.getproc0(), justify=LEFT, width=20, anchor='w' )
		cpu_label.grid(row=0, column=0, rowspan=14, sticky=W)
		
		cpu_label2 = tk.Label( cpu_content_frame, text = rs.getproc1(), justify=LEFT, width=13, anchor='w' )
		cpu_label2.grid(row=0, column=1, rowspan=14, sticky=W)
		
		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=15)	
		
		bind_label = tk.Label( mainframe, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(side=BOTTOM)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))	
		master.mainloop()
	
		

class About_Window:

	def __init__(master):
	
		master = tk.Tk()
		master.geometry("400x450")
		master.title("Commander Pi")
		th.window_list.append(master)
		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)	
		
		titleframe = Frame(mainframe)
		titleframe.pack(fill=X)
				
		image = Image.open(home_path+"/CommanderPi/src/icons/logo.png")
		photo = ImageTk.PhotoImage(image, master=titleframe) 

		title_label = tk.Label( titleframe, text = "  About Application", font=("TkDefaultFont", 18, "bold"), image = photo, compound=LEFT, anchor='w')
		title_label.image = photo
		title_label.pack(side=LEFT)
	
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=15)		

		content_frame = Frame(mainframe)
		content_frame.pack()
		
		about_label = tk.Label( content_frame, text = "Commander Pi 2020\n", justify=CENTER, font=("TkDefaultFont", 11, "bold"))
		about_label.pack()
		
		text_label = tk.Label( content_frame, text="By Jack477\nFor Twister OS Armbian\n\nGraphic elements by grayduck\nIcon derived from a work by Vectors Market", justify=CENTER)
		text_label.pack(fill=X)
		
		version_label = tk.Label( content_frame, text=rs.get_app_version(), font=("TkDefaultFont", 11, "bold"), justify=CENTER)
		version_label.pack()
		
		link = tk.Label( content_frame, text="Changelog", cursor="hand2", fg="#1D81DA", pady=5)
		link.pack(fill=X)
		mlink = 'https://github.com/Jack477/CommanderPi/blob/master/CHANGELOG.md'
		link.bind("<Button-1>", lambda e: rs.cpi_open_url(mlink))
		
		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=15)
		
		update_button = Button(mainframe, text="Check for updates", command=lambda:update_x(), cursor="hand2", font=("TkDefaultFont", 11, "bold"), state=DISABLED)
		update_button.pack()

		color_buton = Button(mainframe, text="Change color theme", command=lambda:change_theme(master), cursor="hand2", font=("TkDefaultFont", 11, "bold"))
		color_buton.pack()

		def update_x():
			up.update_cpi()

		
		bind_label = tk.Label( mainframe, text="Press [Esc] to close", font=("TkDefaultFont", 11, "bold") )
		bind_label.pack(side=BOTTOM)
		master.bind('<Escape>', lambda e:killwindow(e, master))
		th.set_theme(master)
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))		
		master.mainloop()

### Main window		
class Window:
	def __init__(master):

		master = tk.Tk()
		master.geometry("420x550")
		master.title("Commander Pi")
		master.resizable(False, False)
		#master.iconbitmap("@"+home_path+"/CommanderPi/src/xicon.ico")
		icon = PhotoImage(file = home_path+"/CommanderPi/src/icon.png")
		master.iconphoto(True, icon)
		th.window_list.append(master)
		mainframe = Frame(master)
		mainframe.pack(padx=10, pady=10)
		
		
		titleframe = Frame(mainframe)
		titleframe.pack()
		
		loadimg = Image.open(home_path+"/CommanderPi/src/icons/title_logo.png")
		img = ImageTk.PhotoImage(image=loadimg)

		img_label = tk.Label ( titleframe, image=img)
		img_label.image = img
		img_label.grid(row=0, column=0, columnspan=2)
		
		#title_label = tk.Label( titleframe, text = "Commander Pi", font=("TkDefaultFont", 22, "bold") )
		#title_label.grid(row=0, column=1)
		
		separator = ttk.Separator(mainframe, orient='horizontal')
		separator.pack(fill=X, expand=True, pady=10)
		
		infoframe = Frame(mainframe)
		infoframe.pack(fill=X)
		
		title2_label = tk.Label( infoframe, text = "ROCK PI VERSION\nReal-time system information:\n", font=("TkDefaultFont", 11, "bold"), anchor='w')
		title2_label.grid(row=0, column=0, columnspan=2, sticky=W)
		
		board_version_label = tk.Label( infoframe, text= rs.board_version, fg="red", anchor='w')
		board_version_label.grid(row=1, column=0, columnspan=2, sticky=W)
		
		kernel_version_label = tk.Label( infoframe, text = "Kernel version: ", width=30, anchor='w' )
		kernel_version_label.grid(row=2, column=0, sticky=W)
		
		kernel_version_label2 = tk.Label( infoframe, text = rs.kernel_version , width=15, anchor='w')
		kernel_version_label2.grid(row=2, column=1)
		
		kernel_mode_label = tk.Label( infoframe, text = "Operating mode: ", width=30, anchor='w')
		kernel_mode_label.grid(row=3, column=0, sticky=W)

		kernel_mode_label2 = tk.Label( infoframe, text = rs.get_kernel_mode(), width=15, anchor='w')
		kernel_mode_label2.grid(row=3, column=1)

		processor_architecture_label = tk.Label( infoframe, text="Processor architecture: ", width=30, anchor='w' )
		processor_architecture_label.grid(row=4, column=0, sticky=W)
		
		processor_architecture_label2 = tk.Label( infoframe, text=rs.processor_architecture, width=15, anchor='w')
		processor_architecture_label2.grid(row=4, column=1)


		memory_use_label = tk.Label( infoframe, text = "Memory usage: ", width=30, anchor='w' )
		memory_use_label.grid(row=5, column=0, sticky=W)
		
		memory_use_label2 = tk.Label( infoframe, text = "", width=15, anchor='w' )
		memory_use_label2.grid(row=5, column=1)
		
		actual_gpu_temp_label = tk.Label( infoframe, text = "Actual GPU temperature: ", width=30, anchor='w' )
		actual_gpu_temp_label.grid(row=6, column=0, sticky=W)

		actual_gpu_temp_label2 = tk.Label( infoframe, text = "", width=15, anchor='w' )
		actual_gpu_temp_label2.grid(row=6, column=1)


		actual_cpu_temp_label = tk.Label( infoframe, text = "Actual CPU temperature: ", width=30, anchor='w' )
		actual_cpu_temp_label.grid(row=7, column=0, sticky=W)
		
		actual_cpu_temp_label2 = tk.Label( infoframe, text = "", width=15, anchor='w' )
		actual_cpu_temp_label2.grid(row=7, column=1)
		
		actual_cpu_usage_label = tk.Label( infoframe, text = "Processor frequency usage is: ", width=30, anchor='w')
		actual_cpu_usage_label.grid(row=8, column=0, sticky=W)
		
		actual_cpu_usage_label2 = tk.Label(infoframe, text = "",  width=15, anchor='w')
		actual_cpu_usage_label2.grid(row=8, column=1)
		
		actual_gpu_usage_label = tk.Label( infoframe, text = "GPU frequency (V3D) usage is: ", width=30, anchor='w')
		actual_gpu_usage_label.grid(row=9, column=0, sticky=W)
		
		actual_gpu_usage_label2 = tk.Label(infoframe, text = "",  width=15, anchor='w')
		actual_gpu_usage_label2.grid(row=9, column=1)

		used_label = tk.Label ( infoframe, text="Used disk space: ", width=30, anchor='w')
		used_label.grid(row=10, column=0, sticky=W)
		
		##BORDER TO TABLE borderwidth=2, relief="groove",
		used_label2 = tk.Label ( infoframe, text=rs.used+"/"+rs.total+" GiB", width=15, anchor='w')
		used_label2.grid(row=10, column=1)
		
		
		separator2 = ttk.Separator(mainframe, orient='horizontal')
		separator2.pack(fill=X, expand=True, pady=10)

				#REFRESH CPU USAGE, MEMORY USAGE AND TEMPERATURE
		def refresh():
			#for x in th.window_list:
			#	print(x.__class__)
			ttext = rs.reftemp()
			ptext = rs.refusage()
			mtext = rs.refmem()
			gtext = rs.reftemp2()
			gputext = rs.refgpu()
			#dtext = str(rs.get_disk_percent())
			#dtext = "CPU usage " + rs.cpu_usagex +" MHz"
			memory_use_label2.configure(text = mtext + "/100%")
			actual_cpu_temp_label2.configure(text = ttext)
			actual_cpu_usage_label2.configure(text = ptext)
			actual_gpu_temp_label2.configure(text = gtext)
			actual_gpu_usage_label2.configure(text = gputext)
			master.after(1000, refresh)
			
		refresh()
		
		
		advanced_label = tk.Label( mainframe, text = "Advanced tools", font=("TkDefaultFont", 11, "bold"), anchor='w' )	
		advanced_label.pack(fill=X)
		
		btn_frame = Frame(mainframe)
		btn_frame.pack(fill=X)
		
		photo1 = PhotoImage(file = home_path+"/CommanderPi/src/icons/CPUs.png") 
		#photoimage1 = photo1.subsample(15, 15) 
		
		proc_info_button = Button ( btn_frame, text="CPU details", command = lambda:bopen(Proc_Info_Window), width=60, height=80, cursor="hand2", image = photo1, compound=TOP)
		proc_info_button.grid(row=0, column=0, padx=4)
		
		#photo2 = PhotoImage(file = home_path+"/CommanderPi/src/icons/Bootloaders.png")  
		
		#btn4 = Button (btn_frame, text="Bootloader",  width=60, height=80, cursor="hand2", image = photo2, compound=TOP)
		#btn4.grid(row=0, column=1, padx=4)
		
		photo3 = PhotoImage(file = home_path+"/CommanderPi/src/icons/Networkings.png")  		
		
		btn5 = Button (btn_frame, text="Network", command = lambda:bopen(Network_Window),  width=60, height=80, cursor="hand2", image = photo3, compound=TOP)
		btn5.grid(row=0, column=2, padx=4)
		
		#photo4 = PhotoImage(file = home_path+"/CommanderPi/src/icons/Overclockings.png") 
		
		#btn2 = Button(btn_frame, text="Overclock", command = lambda:bopen(Overclock_Window),  width=60, height=80, cursor="hand2", image = photo4, compound=TOP)
		#btn2.grid(row=0, column=3, padx=4)
		
		
		btn3 = Button( mainframe, text="About/Update", command = lambda:bopen(About_Window), font=("TkDefaultFont", 11, "bold"), cursor="hand2")
		btn3.pack(side=BOTTOM, pady=5)

		
		
		master.protocol("WM_DELETE_WINDOW", lambda:on_Window_Close(master))
		th.set_theme(master)
		#up.check_update()
		master.mainloop()
		
