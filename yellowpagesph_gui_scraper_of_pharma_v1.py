
"""
A Simple Assistant for Kryzza's Home Job 
Sample input is a website:
https://www.yellow-pages.ph/business/metro-pharma-philippines-incorporated

This program will scrape information like below:
    'Business Name': 
    'Short Description':
    'Address':
    'Contact Number':
    'Email Address':
    'Website':     
"""
import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import threading
import pyperclip
import time
import pandas as pd
import random
import os.path

class Pharma_Scraper:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Excel Encoder  Assistant ni Kelizha v1")
        self.window.geometry("1020x600")
        self.window.configure(bg="#225479")
        # self.window.resizable(False, False)
        self.font_default = ("Cambria", 11)
        self.font_small = ("Cambria", 10)
        self.font_bold = ("Cambria", 11, "bold")
        self.default_url = "https://www.yellow-pages.ph/business/metro-pharma-philippines-incorporated"
        self.captured_url = ""
        self.save_filepath = "list_of_pharmas.xlsx"
        self.dict_business_firm = {
            'Business Name':"",
            'Short Description':"",
            'Address':"",
            'Contact Number':"",
            'Email Address':"",
            'Website':""
        }
        self.dict_pharma_firm = {
            'Business Name':"",
            'Short Description':"",
            'Address':"",
            'Contact Number':"",
            'Email Address':"",
            'Website':""
        }
        self.data_pharma_firm = {
            'Business Name':[""],
            'Short Description':[""],
            'Address':[""],
            'Contact Number':[""],
            'Email Address':[""],
            'Website':[""]
        }
        self.df_pharma_firms = pd.DataFrame(self.data_pharma_firm)
        # Imagine this GUI Window:
        #################################################################
        ##  button_scrape_wpage  ## entry_webpage_url                  ##
        #################################################################
        ##     label_store_name  ########################################
        ##     entry_store_name  ##   text_display_last_5_excel_rows   ##
        ##    label_description  ##   text_display_last_5_excel_rows   ##
        ##    entry_description  ##   text_display_last_5_excel_rows   ##
        ##        label_address  ##   text_display_last_5_excel_rows   ##
        ##        entry_address  ##   text_display_last_5_excel_rows   ##
        ##     label_contact_no  ##   text_display_last_5_excel_rows   ##
        ##     entry_contact_no  ##   text_display_last_5_excel_rows   ##
        ##  label_email_address  ##   text_display_last_5_excel_rows   ##
        ##  entry_email_address  ##   text_display_last_5_excel_rows   ##   
        ##        label_website  ##   text_display_last_5_excel_rows   ##
        ##        entry_website  ##   text_display_last_5_excel_rows   ##
        #################################################################
        ## Open Exisitng ## entry_excel_filepath ## Save Firm Info     ##
        #################################################################
        
        # Row 0  ----------------------------
        frame_0 = tk.Frame(master=self.window, relief=tk.FLAT, borderwidth=3, bg="#225479")  #  bg="#225479
        frame_0.pack()
        # Image - Logo
        self.script_dir = os.path.dirname(__file__)  # To help python locate our image
        self.image_file = os.path.join(self.script_dir, "eeak_logo.jpg")  #  bg="#225479"
        self.imagelogo = Image.open(self.image_file)
        self.imagelogo = self.imagelogo.resize((250, 100))
        self.imagelogo = ImageTk.PhotoImage(self.imagelogo)
        self.label_imagelogo = tk.Label(frame_0, image=self.imagelogo, bg="#225479")
        self.label_imagelogo.pack(side="left")
        
        button_scrape = tk.Button(master=frame_0, text="Scrape Webpage:", command=self.scrape_webpage, \
            font=self.font_bold)
        button_scrape.pack(side=tk.LEFT, fill=tk.X, padx=5)
        
        self.entry_webpage = tk.Entry(master=frame_0, width=80, font=self.font_default)
        self.entry_webpage.pack(side=tk.LEFT, padx=5, pady=5, ipady=5)
        self.update_entry_webpage()
        
        # Row 1  ------------------------------  
        frame_1 = tk.LabelFrame(master=self.window, relief=tk.FLAT, borderwidth=3, bg="#225479")
        frame_1.pack()  
        # Row 1, Col 0  ------------------------------  
        frame_1_0 = tk.LabelFrame(master=frame_1, relief=tk.SUNKEN, borderwidth=3, bg="#225479")
        frame_1_0.grid(row=1, column=0, sticky=tk.NS)
        
        for key in self.dict_business_firm.keys():
            label_key = tk.Label(text=key, master=frame_1_0, font=self.font_bold, bg="#225479", fg="white")
            label_key.pack(fill="both")            
            self.dict_pharma_firm[key] = tk.Entry(master=frame_1_0, width=40, font=self.font_default)
            self.dict_pharma_firm[key].pack(fill=tk.X, ipadx=10, padx=5)
            self.dict_pharma_firm[key].delete(0, tk.END)
            self.dict_pharma_firm[key].insert(0, self.dict_business_firm[key])
            if key == "Short Description":
                button_random_description = tk.Button(master=frame_1_0, text="Generate a description.", 
                                                      command=self.get_random_description, font=self.font_default)
                button_random_description.pack(pady=5)
        # Row 1, Col 1  ------------------------------  
        frame_1_1 = tk.LabelFrame(master=frame_1, relief=tk.SUNKEN, borderwidth=3, bg="#225479")
        frame_1_1.grid(row=1, column=1, sticky=tk.NS)
        
        self.text_df = tk.Text(master=frame_1, width=80, font=self.font_default)
        self.text_df.grid(row=1, column=1, sticky=tk.NSEW, padx=5)
        self.udpate_text_df()
        
        # Row 2 ------------------------------------------ 
        frame_2 = tk.LabelFrame(master=self.window, relief=tk.FLAT, borderwidth=3, bg="#225479")
        frame_2.pack()

        button_savefile = tk.Button(master=frame_2, text="Save Information", command=self.save_file,
                                    font=self.font_bold)
        button_savefile.pack(side="right", padx=10, ipadx=10)
        
        self.entry_filepath = tk.Entry(master=frame_2, width=50, font=self.font_default)
        self.entry_filepath.pack(side="right", padx=5, pady=5, ipadx=5, ipady=5)
        self.entry_filepath.delete(0, tk.END)
        self.entry_filepath.insert(0, self.save_filepath)

        button_openfile = tk.Button(master=frame_2, text="Open Excel file:", command=self.select_excel_file,
                                    font=self.font_bold)
        button_openfile.pack(side="right", padx=0, ipadx=5)
                
    def capture_clipboard(self):
        while True:
            new_clipboard_content = pyperclip.paste()   # From pyperclip module
            if new_clipboard_content.startswith("http"):
                self.captured_url = new_clipboard_content
                self.update_entry_webpage()
            time.sleep(2)  # From time module

    def start_clipboard_monitoring_thread(self):  # Call this function inside main()
        clipboard_thread = threading.Thread(target=self.capture_clipboard)  # From threading module
        clipboard_thread.daemon = True  # This makes the thread exit when the main program exits
        clipboard_thread.start()


    def scrape_webpage(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/116.0.0.0 Safari/537.36"
            }
        url = self.entry_webpage.get()
        try:
            webpage = requests.get(url, headers=headers)
        except requests.exceptions.MissingSchema:
            self.entry_webpage.delete(0, tk.END)
            self.entry_webpage.insert(tk.END, f"Missing 'https://' in URL: {url}")
            return
        
        soup = BeautifulSoup(webpage.content, "html.parser")
        
        try:
            self.dict_business_firm['Business Name'] = soup.find("h1", class_="h1-tradename").text
        except AttributeError:
            try:
                self.dict_business_firm['Business Name'] = soup.find("h1", class_="h1-single-businessname").text
            except AttributeError:
                self.dict_business_firm['Business Name'] = ""
        try:
                self.dict_business_firm['Short Description'] = soup.find("h2", class_="h2-businessname").text
        except AttributeError:
            self.dict_business_firm['Short Description'] = ""
        try:
            self.dict_business_firm['Address'] = soup.find("a", class_="biz-link yp-click").text
        except AttributeError:
            self.dict_business_firm['Address'] = ""
        try:    
            self.dict_business_firm['Contact Number'] = soup.find("span", class_="phn-txt").text
        except AttributeError:
            self.dict_business_firm['Contact Number'] = ""
            
        try:
            self.dict_business_firm['Email Address'] = soup.find("a", class_="email-link").text
        except AttributeError:
            self.dict_business_firm['Email Address'] = ""
        try:
            self.dict_business_firm['Website'] = soup.find("a", class_="biz-link d-block ellipsis yp-click").text
        except AttributeError:
            try:
                self.dict_pharma_firm['Website'] = soup.find("a", class_="website-link").text
                if self.dict_pharma_firm['Website'].endswith("/"): 
                    self.dict_pharma_firm['Website'] = self.dict_pharma_firm['Website'].replace("/", "") 
            except AttributeError:
                self.dict_pharma_firm['Website'] = ""
                
        self.update_entries()
        
        
    def get_random_description(self):
        
        pharmacy_descriptions = [
            "Prescriptions filled here.",
            "Healthcare in one stop.",
            "Your health, our priority.",
            "Expert medication advice.",
            "Care you can trust.",
            "Medicines for all ages.",
            "Wellness delivered daily.",
            "Convenient health solutions.",
            "Your health, our mission.",
            "Healthy lives, our goal.",
            "Medicines with care.",
            "Health starts here.",
            "Caring for your well-being.",
            "Medications made easy.",
            "Better health begins today.",
            "Trusted medical partners.",
            "Medicines for life's moments.",
            "Health in your hands.",
            "Your health, our passion.",
            "Pharmacy for better living.",
            "Supporting healthy communities.",
            "Wellness, your way.",
            "Medications that matter.",
            "Your well-being, our priority.",
            "Expert care, trusted results.",
            "Wellness solutions for you.",
            "Medications, made personal.",
            "Pharmacy care near you.",
            "Your health advocate.",
            "Quality medications, always.",
            "Your health, our care.",
            "Medicines you can count on.",
            "Improving lives daily.",
            "Supporting your well-being.",
            "Caring for healthier futures.",
            "Healthier choices start here.",
            "Your health matters most.",
            "Medications with compassion.",
            "Your health, our commitment.",
            "Well-being at your service.",
            "Medicines tailored to you.",
            "Caring for your health journey.",
            "Wellness starts with us.",
            "Supporting vibrant health.",
            "Medications for life's challenges.",
            "Health solutions made simple.",
            "Pharmacy, your partner in health.",
            "Expert care, trusted solutions.",
            "Wellness, simplified.",
            "Medicines, your way.",
            "Caring for your wellness.",
            "Trusted health advisors.",
            "Medications, well served.",
            "Supporting your best health.",
            "Your health, our expertise.",
            "Wellness delivered with care.",
            "Medications, well prescribed.",
            "Caring for healthier lives.",
            "Your health, our focus.",
            "Wellness solutions near you.",
            "Medications tailored to life.",
            "Your health, our promise.",
            "Quality care, trusted results.",
            "Medicines, your well-being.",
            "Caring for your better health.",
            "Your health, our dedication.",
            "Wellness, our commitment.",
            "Medications that empower.",
            "Supporting lifelong health.",
            "Your health, our mission.",
            "Medications, your choice.",
            "Caring for your vitality.",
            "Expert care, trusted advice.",
            "Wellness at your fingertips.",
            "Medications, well provided.",
            "Your health, our care.",
            "Quality health solutions.",
            "Caring for your comfort.",
            "Supporting your vitality.",
            "Wellness, your choice.",
            "Medications, our expertise.",
            "Your health, our goal.",
            "Medications that support.",
            "Caring for your journey.",
            "Expert care, always here.",
            "Wellness made personal.",
            "Medications, trusted care.",
            "Your health, our passion.",
            "Quality care, trusted care.",
            "Caring for your wellness.",
            "Supporting active lives.",
            "Wellness, our mission.",
            "Medications for your life.",
            "Your health, our service.",
            "Medications that matter.",
            "Caring for better living.",
            "Your well-being, our care.",
            "Expert advice, trusted care.",
            "Wellness, delivered daily.",
            "Medications, your wellness.",
            "Your health, our dedication.",
            "Medications, tailored care.",
            "Caring for your health.",
            "Supporting vibrant wellness.",
            "Wellness, your priority.",
            "Medications, quality care.",
            "Your health, our commitment."
        ]

        picked_description = random.choice(pharmacy_descriptions)
        pharmacy_descriptions.remove(picked_description)
        self.dict_pharma_firm['Short Description'].delete(0, tk.END)
        self.dict_pharma_firm['Short Description'].insert(tk.END, picked_description)
        
    def update_entry_webpage(self):
        self.entry_webpage.delete(0, tk.END)
        self.entry_webpage.insert(tk.END, self.default_url \
            if self.captured_url=="" else self.captured_url
            )
             
    def update_entries(self):
        for key in self.dict_pharma_firm.keys():
            self.dict_pharma_firm[key].delete(0, tk.END)
            self.dict_pharma_firm[key].insert(0, self.dict_pharma_firm[key])
    
    def udpate_text_df(self, delay=0):
        self.text_df.delete("1.0", tk.END)
        self.text_df.insert(tk.END, "Saving new entry.") 
        if delay > 1:
            time.sleep(delay-1)
            self.text_df.insert(tk.END, ".") 
            time.sleep(delay-1)
            self.text_df.insert(tk.END, ".") 
        self.text_df.delete("1.0", tk.END)
        self.text_df.insert(tk.END, self.df_pharma_firms.to_string())        
        
    def select_excel_file(self):
        self.save_filepath = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"),
                       ("CSV files", "*.csv")]
            )
        if self.save_filepath:
            self.entry_filepath.delete(0, tk.END)
            self.entry_filepath.insert(0, self.save_filepath)
            self.df_pharma_firms = pd.read_excel(self.save_filepath) \
                if self.save_filepath.endswith("xlsx") else \
                    pd.read_csv(self.save_filepath)
        self.udpate_text_df(delay=0)
            
    def save_file(self):
        filename = self.entry_filepath.get()
        
        for key in self.dict_business_firm.keys():
            self.dict_business_firm[key] = self.dict_pharma_firm[key].get()
            
        self.df_pharma_firms = self.df_pharma_firms._append(self.dict_business_firm, ignore_index=True)
        if filename.endswith("xlsx"):
            self.df_pharma_firms.to_excel(filename, index=False)
        elif filename.endswith("csv"):
            self.df_pharma_firms.to_csv(filename, index=False)
        self.udpate_text_df(delay=2)

    def run(self):
        self.start_clipboard_monitoring_thread()
        self.window.mainloop()

if __name__ == "__main__":
    application = Pharma_Scraper()
    application.run()
