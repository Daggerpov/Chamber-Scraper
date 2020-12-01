from selenium import webdriver 


def web_scraper(state_name):
    webdriver.Chrome("./chromedriver")
    
    
    pass
"""    try:
        
        pass
    except:
        
        self.driver.quit()
        

    try:
        

    except:
        self.driver.quit()
        

    self.driver.quit()


    return     """

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
        self.weather_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
        
        #fitting the output
        self.lower_frame = tk.Frame(self.master, highlightcolor="#99aab5", bd=10)
        self.lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')


        #output label
        label = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 36, 'bold'))
        label.place(relwidth=1, relheight=0.5)



        #entry text box for user input
        self.entry = PlaceholderEntry(self.weather_frame, "State Name", '', font=('Courier', 36))
        self.entry.place(relwidth=0.65, relheight=1)

        #button for weather entry
        #I only want its command to run once, when it's clicked so I made a 
        #simple lambda function that invokes the weather_bot function
        self.button = tk.Button(self.weather_frame, text="Get Weather", font=('Courier', 28), bg='white', 
            command=lambda:web_scraper(self.entry.get()))
        self.button.place(relx=0.7, relheight=1, relwidth=0.3)


if __name__ == '__main__':
    main()