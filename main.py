from bs4 import BeautifulSoup
import requests
import time

def web_scraper(state, name, website, phone_number, address, address2, chamber_member_bool='This is not a U.S. Chamber Member.'):
    if len(state.split()) == 2: 
        state = state.replace(' ', '-')
    url = f'https://www.uschamber.com/co/chambers/{state.lower()}'
    
    header = {"From":"Daniel Agapov <danielagapov1@gmail.com>"}

    response = requests.get(url, headers=header)
    if response.status_code != 200: print("Failed to get HTML:", response.status_code, response.reason); exit()

    soup = BeautifulSoup(response.text, "html5lib")
    
    chambers = soup.select(".chamber-finder__item")
    current_chamber = chambers[index]
    lines = current_chamber.text.split('\n')

    for line in lines:
        if 'U.S. Chamber Member' in line:
            chamber_member_bool['text'] = 'This is a U.S. Chamber Member.'
        
        if 'Website—' in line:
            website['text'] = line.replace('Website—', '').replace(' ', '')
        
        if 'Phone Number—' in line:
            phone_number['text'] = line.replace('Phone Number—', '').replace(' ', '')

        if 'Address—' in line:
            line_number = lines.index(line)
            split_address = lines[line_number+2:line_number+4]
            address['text'] = str(split_address[0]).replace('  ', '')
            address2['text'] = str(split_address[1]).replace('  ', '')

        
    name['text'] = lines[2].replace('  ', '')    

global index ; index = 0

def increase_index():
    print("increase")
    global index
    index += 1

def decrease_index():
    print("decrease")
    global index
    index -= 1

#everything past this point is just for the GUI and doesn't matter for the web scraper. 
#------------------------------------------------------------------------------------------#

import tkinter as tk
from tkinter import ttk


HEIGHT = 768
WIDTH = 1366

def main():
    #initializing module
    root = tk.Tk()
    
    #setting the current screen to start menu
    app = main_screen(root)
    
    #overall GUI loop which will run constantly, accepting input and such
    root.mainloop()


class PlaceholderEntry(ttk.Entry):
    #initializing the arguments passed in
    def __init__(self, container, placeholder, validation, *args, **kwargs):
        super().__init__(container, *args, style="Placeholder.TEntry", **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        
        #runs the appropriate method for when the user is focused in/out of the element
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        #if this argument is given (like for the instagram password, 
        # then the entry box will hide its text with asterisks)
        self.validation = validation

    
    def _clear_placeholder(self, e):
        #deleting all text placed automatically with the placeholder
        if self["style"] == "Placeholder.TEntry":
            self.delete("0", "end")
            self["style"] = "TEntry"
        
        #editing the property of the entry box 'show' to display asterisks ,
        #instead of any of the entered characters
        if self.validation == 'password':
            self['show'] = "*"
        
    def _add_placeholder(self, e):
        #if there isn't any text entered in AND the user isn't focused in 
        #on this, then it'll add the placeholder
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = "Placeholder.TEntry"


class main_screen():
    def __init__(self, master):
        #these properties will mostly stay constant throughout all windows
        self.master = master
        self.master.title("Chamber Scraper GUI")
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH, bg = '#23272a')
        self.canvas.pack()
        self.master.config(bg = "#23272a")
        self.master.resizable(width=False, height=False)

        
        #making the style of this window compatible with my custom entry class
        self.style = ttk.Style(self.master)
        self.style.configure("Placeholder.TEntry", foreground="#d5d5d5")
        

        #fitting the entry and button for weather
        self.weather_frame = tk.Frame(self.master, bg="#99aab5", bd=5)
        self.weather_frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.1, anchor='n')
        
        #fitting the output
        self.lower_frame = tk.Frame(self.master, highlightcolor="#99aab5", bd=10)
        self.lower_frame.place(relx=0.5, rely=0.20, relwidth=0.75, relheight=0.7, anchor='n')



        name = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        name.place(rely=0, relwidth=1, relheight=0.165)

        chamber_member_bool = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        chamber_member_bool.place(rely=0.165, relwidth=1, relheight=0.165)

        phone_number = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        phone_number.place(rely=0.33, relwidth=1, relheight=0.165)

        website = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        website.place(rely=0.495, relwidth=1, relheight=0.165)

        address = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        address.place(rely=0.66, relwidth=1, relheight=0.165)

        address2 = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        address2.place(rely=0.825, relwidth=1, relheight=0.165)

        #entry text box for user input
        self.entry = PlaceholderEntry(self.weather_frame, "State Name", '', font=('Courier', 36))
        self.entry.place(relwidth=0.65, relheight=1)

        #button for state entry
        #I only want its command to run once, when it's clicked so I made a 
        #simple lambda function that invokes the web_scraper function
        self.button = tk.Button(self.weather_frame, text="Web Scrape", font=('Courier', 24), bg='white', 
            command=lambda:web_scraper(self.entry.get(), name, website, phone_number, address, address2, chamber_member_bool))
        self.button.place(relx=0.7, relheight=1, relwidth=0.3)




        #next and prev. buttons for chambers navigation
        
        
        #making the picture into a label
        self.previous_pic = tk.PhotoImage(file='./images/previous_pic.png')
        self.previous_pic_label = tk.Label(self.master, image=self.previous_pic)
        self.previous_pic_label.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.0125)

        #putting a button at the same spot as the label, essentially
        #making it into one
        self.previous_pic_button = tk.Button(self.master, image=self.previous_pic, 
        command=lambda:decrease_index())
        self.previous_pic_button.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.0125)

        

        self.next_pic = tk.PhotoImage(file='./images/next_pic.png')
        self.next_pic_label = tk.Label(self.master, image=self.next_pic)
        self.next_pic_label.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.885) #1366/768 = 1.7786, so I set height to 
                                                                                        #this so that it'd be proportional to width.

        self.next_pic_button = tk.Button(self.master, image=self.next_pic, 
        command=lambda:increase_index())
        self.next_pic_button.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.885) 

        
        

if __name__ == '__main__':
    main()