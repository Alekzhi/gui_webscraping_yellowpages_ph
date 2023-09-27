
"""
A Simple Copy-paste Assistant for Kelizha's Home Job 
Sample input is a website:
https://www.yellow-pages.ph/business/feria-tantoco-daos-law-offices-3

This program will scrape information like below:
    'Business Name':"Feria Law",
    'Short Description':"Feria Tantoco Daos Law Offices",
    'Address':"8/F, DPC Place, 2322, Chino Roces Avenue Extension, Makati City 1200 Metro Manila",
    'Contact Number':"+63 (2) 8 889 8677",
    'Email Address':"contactus@ferialaw.com",
    'Website': "ferialaw.com" 
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

class LawFirmScraper:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Excel Encoder  Assistant ni Kelizha v1")
        self.window.geometry("1020x600")
        self.window.configure(bg="#225479")
        # self.window.resizable(False, False)
        self.font_default = ("Cambria", 11)
        self.font_small = ("Cambria", 10)
        self.font_bold = ("Cambria", 11, "bold")
        self.default_url = "https://www.yellow-pages.ph/business/feria-tantoco-daos-law-offices-3"
        self.captured_url = ""
        self.save_filepath = "kryzzas_law_firm_excel.xlsx"
        self.dict_business_firm = {
            'Business Name':"",
            'Short Description':"",
            'Address':"",
            'Contact Number':"",
            'Email Address':"",
            'Website':""
        }
        self.dict_entries_law_firm = {
            'Business Name':"",
            'Short Description':"",
            'Address':"",
            'Contact Number':"",
            'Email Address':"",
            'Website':""
        }
        self.data_law_firm = {
            'Business Name':[""],
            'Short Description':[""],
            'Address':[""],
            'Contact Number':[""],
            'Email Address':[""],
            'Website':[""]
        }
        self.df_law_firms = pd.DataFrame(self.data_law_firm)
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
        ## Open Exisitng ## entry_excel_filepath ## Save Law Firm Info ##
        #################################################################
        
        # Row 0  ----------------------------
        frame_0 = tk.Frame(master=self.window, relief=tk.FLAT, borderwidth=3, bg="#225479")  #  bg="#225479
        frame_0.pack()
        # Image - Logo
        self.script_dir = os.path.dirname(__file__)  # To help python locate image
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
            self.dict_entries_law_firm[key] = tk.Entry(master=frame_1_0, width=40, font=self.font_default)
            self.dict_entries_law_firm[key].pack(fill=tk.X, ipadx=10, padx=5)
            self.dict_entries_law_firm[key].delete(0, tk.END)
            self.dict_entries_law_firm[key].insert(0, self.dict_business_firm[key])
            if key == "Short Description":
                button_random_description = tk.Button(master=frame_1_0, text="Generate a description.", 
                                                      command=self.get_random_description, font=self.font_default)
                button_random_description.pack(pady=5)
        # Row 1, Col 1  ------------------------------  
        frame_1_1 = tk.LabelFrame(master=frame_1, relief=tk.SUNKEN, borderwidth=3, bg="#225479")
        frame_1_1.grid(row=1, column=1, sticky=tk.NS)
        # SIMPLE DF VIEWER for now
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
           
                
    # Check clipboard if a URL is copied
    def capture_clipboard(self):
        while True:
            new_clipboard_content = pyperclip.paste() 
            if new_clipboard_content.startswith("http"):
                self.captured_url = new_clipboard_content
                self.update_entry_webpage()
            time.sleep(2) 

    # Clipboard checking background process
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
                self.dict_law_firm['Website'] = soup.find("a", class_="website-link").text
                if self.dict_law_firm['Website'].endswith("/"): 
                    self.dict_law_firm['Website'] = self.dict_law_firm['Website'].replace("/", "") 
            except AttributeError:
                self.dict_law_firm['Website'] = ""
                
        self.update_entries()
      
        
    def get_random_description(self):
        lawfirm_descriptions = [ 
            "Providing legal expertise for over two decades.",
            "Your trusted partner in legal matters.",
            "Dedicated to delivering justice and solutions.",
            "Committed to upholding the law and your rights.",
            "Experienced professionals serving your legal needs.",
            "Solving complex legal challenges with creativity.",
            "Your advocate in legal matters big and small.",
            "Providing expert legal counsel for individuals and businesses.",
            "Your partner in navigating legal complexities.",
            "Dedicated to justice and client success.",
            "Upholding the law with integrity and excellence.",
            "Experienced attorneys serving your legal needs.",
            "Tailoring legal solutions to your unique situation.",
            "Advocates for your rights and interests.",
            "Solving legal challenges with creativity and precision.",
            "Personalized legal guidance for every client.",
            "Your trusted source for legal expertise.",
            "Defending your rights with passion and skill.",
            "Building bridges to legal success.",
            "Delivering results through strategic legal solutions.",
            "Making legal matters simple and clear.",
            "Your advocates in and out of the courtroom.",
            "Crafting legal strategies that deliver.",
            "Protecting your interests with unwavering dedication.",
            "Leading the way in legal innovation.",
            "Expertise you can rely on for every case.",
            "Your legal ally for a brighter future.",
            "Problem solvers for complex legal issues.",
            "Guiding you through legal challenges, step by step.",
            "Champions of justice, one case at a time.",
            "Navigating the legal landscape with confidence.",
            "Defending your interests with determination.",
            "Resolving disputes efficiently and effectively.",
            "Empowering you with legal knowledge.",
            "Your legal partner in times of uncertainty.",
            "Achieving favorable outcomes with proven strategies.",
            "Your first choice for comprehensive legal support.",
            "Expert counsel for a changing world.",
            "Fighting for your rights and interests.",
            "Tailored legal solutions for peace of mind.",
            "Trusted advisors in complex legal matters.",
            "Responsive, reliable, and results-oriented.",
            "Creative problem solvers for legal challenges.",
            "Delivering justice through skilled representation.",
            "Excellence in legal advocacy.",
            "Your voice in the legal arena.",
            "Advocates for justice and fairness.",
            "Committed to ethical and effective legal representation.",
            "Crafting solutions that stand the test of time.",
            "Building a solid foundation for legal success.",
            "Dedicated to achieving your legal goals.",
            "Guiding you through the legal maze.",
            "Solutions that align with your objectives.",
            "Resolving disputes with integrity and professionalism.",
            "Your compass in the world of law.",
            "Solving legal puzzles with expertise.",
            "Advocating for your rights with determination.",
            "Personalized legal strategies for your needs.",
            "Providing clarity in complex legal situations.",
            "Your path to justice and resolution.",
            "Respected advocates for individuals and businesses.",
            "Your legal peace of mind starts here.",
            "Navigating legal complexities with ease.",
            "Skilled negotiators and litigators.",
            "Empowering you with legal knowledge and options.",
            "Fierce defenders of your rights.",
            "Transforming legal challenges into opportunities.",
            "Guiding you towards legal victory.",
            "Excellence in legal advocacy and strategy.",
            "Advocates for fairness and justice.",
            "Personalized legal solutions that work for you.",
            "Trusted partners in legal matters.",
            "Building bridges to favorable outcomes.",
            "Experts in understanding and applying the law.",
            "Dedicated to client-centered legal services.",
            "Your advocates for a just resolution.",
            "Advocating for what matters most to you.",
            "Experienced attorneys, compassionate advisors.",
            "Solving legal puzzles with precision.",
            "Your voice in the legal arena.",
            "Your legal journey starts with us.",
            "Committed to ethical and effective representation.",
            "Crafting solutions that make a difference.",
            "Navigating legal challenges with confidence.",
            "Achieving success through collaboration and expertise.",
            "Guiding you towards a legal victory.",
            "Excellence in legal counsel and strategy.",
            "Advocates for fairness and equal representation.",
            "Customized legal solutions for your needs.",
            "Empowering you with legal options and insights.",
            "Dedicated to protecting your rights and interests.",
            "Transforming challenges into opportunities with legal expertise.",
            "Your path to a just resolution.",
            "Trusted allies in legal matters.",
            "Excellence in advocacy and strategy.",
            "Advocates for justice and client success.",
            "Solving legal challenges with innovation and insight.",
            "Guiding you towards favorable legal outcomes.",
            "Your trusted legal advisors, committed to your success.",
            "Crafting solutions that uphold your rights and objectives.",
            "Advocating for your interests with determination.",
            "Delivering personalized legal strategies for every case.",
            "Resolving disputes efficiently and effectively.",
            "Your legal partners in navigating complexities.",
            "Trusted advocates for individuals and businesses.",
            "Your first choice for comprehensive legal support.",
            "Excellence in legal counsel, committed to achieving results."
        ]

        picked_description = random.choice(lawfirm_descriptions)
        lawfirm_descriptions.remove(picked_description)
        self.dict_entries_law_firm['Short Description'].delete(0, tk.END)
        self.dict_entries_law_firm['Short Description'].insert(tk.END, picked_description)
        
        
    def update_entry_webpage(self):
        self.entry_webpage.delete(0, tk.END)
        self.entry_webpage.insert(tk.END, self.default_url \
            if self.captured_url=="" else self.captured_url
            )
           
             
    def update_entries(self):
        for key in self.dict_law_firm.keys():
            self.dict_entries_law_firm[key].delete(0, tk.END)
            self.dict_entries_law_firm[key].insert(0, self.dict_law_firm[key])
    
    
    def udpate_text_df(self, delay=0):
        self.text_df.delete("1.0", tk.END)
        self.text_df.insert(tk.END, "Saving new Law Firm entry.") 
        if delay > 1:
            time.sleep(delay-1)
            self.text_df.insert(tk.END, ".") 
            time.sleep(delay-1)
            self.text_df.insert(tk.END, ".") 
        self.text_df.delete("1.0", tk.END)
        self.text_df.insert(tk.END, self.df_law_firms.to_string())        
     
        
    def select_excel_file(self):
        self.save_filepath = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"),
                       ("CSV files", "*.csv")]
            )
        if self.save_filepath:
            self.entry_filepath.delete(0, tk.END)
            self.entry_filepath.insert(0, self.save_filepath)
            self.df_law_firms = pd.read_excel(self.save_filepath) \
                if self.save_filepath.endswith("xlsx") else \
                    pd.read_csv(self.save_filepath)
        self.udpate_text_df(delay=0)
            
            
    def save_file(self):
        filename = self.entry_filepath.get()
        
        for key in self.dict_business_firm.keys():
            self.dict_business_firm[key] = self.dict_entries_law_firm[key].get()
            
        self.df_law_firms = self.df_law_firms._append(self.dict_business_firm, ignore_index=True)
        if filename.endswith("xlsx"):
            self.df_law_firms.to_excel(filename, index=False)
        elif filename.endswith("csv"):
            self.df_law_firms.to_csv(filename, index=False)
        self.udpate_text_df(delay=2)

    def run(self):
        self.start_clipboard_monitoring_thread()
        self.window.mainloop()


if __name__ == "__main__":
    application = LawFirmScraper()
    application.run()
