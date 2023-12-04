
"""
Specific search for Hospitals
A Simple Encoding Assistant for Kelizha's Part-time work at Home Job Seekers (HJBS) Company
"""
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import threading
import time
from datetime import datetime
import pandas as pd
import random
import os.path

YES = True
NO = False

class YellowPagesPhScraper:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Excel Encoder Assistant ni Kelizha")
        self.window.geometry("1020x760")
        self.window.configure(bg="#225479")
        self.window.resizable(False, False)
        self.font_default = ("Cambria", 12)
        self.font_small = ("Cambria", 10)
        self.font_large = ("Consolas", 13, "bold")
        self.font_bold = ("Cambria", 12, "bold")
        self.search_what_trimmed = "hospital" # Lower case version and without spaces
        self.search_what = "Hospital"
        self.search_location = "Metro Manila"
        self.home_url = "https://www.yellow-pages.ph"
        self.default_url = f"https://www.yellow-pages.ph/search/{self.search_what.lower()}/{self.search_location.lower().replace(' ', '-')}/page-1"
        self.captured_url = ""
        self.list_scraped_webpages = []
        self.save_filepath = "hospitals_within_manila.xlsx"
        self.headers = {  # This my Chrome browser's User-Agent info
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/116.0.0.0 Safari/537.36"
                }
        self.dict_business_info = {
            'Trade Name':"",
            'Category': "",
            'Short Description':"",
            'Address':"",
            'Contact Number':"",
            'Website': "",
            'Facebook URL':"",
            'Email Address': ""
        }
        self.dict_entries_business = {
            'Trade Name':"",
            'Category': "",
            'Short Description':"",
            'Address':"",
            'Contact Number':"",
            'Website': "",
            'Facebook URL':"",
            'Email Address': ""
        }
        self.data_business_info = {
            'Trade Name': [""],
            'Category': [""],
            'Short Description': [""],
            'Address': [""],
            'Contact Number': [""],
            'Website': [""],
            'Facebook URL': [""],
            'Email Address': [""]
        }
        
        self.tuple_not_hospital = [
            "industr", "tech", "electr", "service", "system",
            "steel", "engineer", "environm", "canvas", "plastic", "manufact",
            "transport", "transform", "innovat", "quantum", "glass", "aluminum", "rental",
            "market", "express", "construc", "truck", "press", "security", "enterpr",
            "fabric", "rubber", "marine", "ship", "insular", "pharma", "pedia"
        ]
        
        self.df_business_infos = pd.DataFrame(self.data_business_info)
        self.eeak_logs = []
        self.continue_scraping = NO  # Automated scraping has not started yet
        
        
        self.script_dir = os.path.dirname(__file__)  # To help python locate our image
        self.image_file = os.path.join(self.script_dir, "eeak_logo.jpg")  #  bg="#225479"
        self.imagelogo = Image.open(self.image_file)
        self.imagelogo = self.imagelogo.resize((500, 200))
        self.imagelogo = ImageTk.PhotoImage(self.imagelogo)
        # Window frame rows and columns partition
        self.MAXROWS = 18      
        self.MAXCOLUMNS = 7
        # FRAME 1 of 2: for Logo, Entries and TView
        self.frame_upper = tk.LabelFrame(self.window, bg="#225479")
        self.frame_upper.grid(rowspan=self.MAXROWS, columnspan=self.MAXCOLUMNS, row=0, column=0, padx=5, pady=5)
        
        self.label_imagelogo = tk.Label(self.frame_upper, image=self.imagelogo, bg="#225479")
        self.label_imagelogo.grid(rowspan=4, columnspan=3, row=0, column=0, sticky="nw")
        self.BELOW_LOGO = 4
        
        self.label_webpage = tk.Label(self.frame_upper, text=self.default_url, width=45, font=self.font_default, fg="#9acef5", bg="#134163")
        self.label_webpage.grid(columnspan=5, row=self.BELOW_LOGO, sticky="wes", column=0, ipady=5)
        
        label_search_what = tk.Label(self.frame_upper, text="Search:", font=self.font_large, fg="#c5e4fb", bg="#225479")
        label_search_what.grid(row=1, column=3, sticky="nse", pady=10)
        self.entry_search_what = tk.Entry(self.frame_upper, width=40, font=self.font_bold, fg="grey")
        self.entry_search_what.grid(columnspan=2, row=1, column=4, sticky="w", ipady=10)
        self.entry_search_what.insert(0, self.search_what)
        
        label_search_location = tk.Label(self.frame_upper, text="Location:", font=self.font_large, fg="#c5e4fb", bg="#225479")
        label_search_location.grid(row=2, column=3, sticky="nse")
        self.entry_search_location = ttk.Combobox(self.frame_upper, width=40, font=self.font_bold, foreground="grey",
                                                  values=["Metro Manila", "Makati City, Metro Manila", "Nationwide"])
        self.entry_search_location.grid(columnspan=2, row=2, column=4, sticky="w", ipady=10)
        self.entry_search_location.insert(0, self.search_location)
        
        
        self.button_go = tk.Button(self.frame_upper, text="GO!", font=self.font_bold, command=self.start_auto_scraping)
        self.button_go.grid(row=self.BELOW_LOGO, column=5, columnspan=2, sticky="w", ipadx=20)
        
        self.button_stop = tk.Button(self.frame_upper, text="STOP", font=self.font_bold, command=self.stop_scraping)
        self.button_stop.grid(row=self.BELOW_LOGO, column=5, columnspan=2, sticky="e", ipadx=20)
        
        self.BELOW_WEPAGE = self.BELOW_LOGO+1
        row = self.BELOW_WEPAGE
        # Loop through  our column headers, create their entries and labels, then insert their values from a dataframe
        for key in self.dict_business_info.keys():
            label_key = tk.Label(self.frame_upper, text=key, width=15, font=self.font_bold, fg="white", bg="#225479")
            label_key.grid(row=row, column=0 , sticky="e")            
            self.dict_entries_business[key] = tk.Entry(self.frame_upper, width=30, font=self.font_default)
            self.dict_entries_business[key].grid(columnspan=2, row=row, column=1, sticky="w", ipady=5) 
            self.dict_entries_business[key].delete(0, tk.END)
            self.dict_entries_business[key].insert(0, self.dict_business_info[key])
            row += 1
        self.button_save = tk.Button(self.frame_upper, text=f"Save Details", command=self.save_file, font=self.font_bold)
        self.button_save.grid(columnspan=3, row=row, column=0, ipadx=15, ipady=5) 
        row += 1
        
        # Additional invisible rows if DF Headers less than 6
        # for i in range(2):
        #     tk.Label(self.frame_upper, bg="#225479").grid(columnspan=3, row=row, column=0,  pady=5)
        #     row += i+1
            
        self.frame_ofTview = tk.LabelFrame(self.frame_upper, text="Logs/DataFrames", fg="lightgrey", bg="#225479")
        self.frame_ofTview.grid(row=self.BELOW_WEPAGE, column=3, rowspan=row-4, columnspan=4,  sticky="nswe", ipady=100)
        # Contest Display ==================== Treeview version =================
        self.tview_df_contents = ttk.Treeview(self.frame_ofTview)
        self.tview_df_contents.place(relwidth=1, relheight=1) # Relative to the size of its frame_ofTview container
        tview_xscroll = tk.Scrollbar(self.frame_ofTview, orient="horizontal", command=self.tview_df_contents.xview) # command=update xaxis view of frame_ofTview
        tview_xscroll.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        tview_yscroll = tk.Scrollbar(self.frame_ofTview, orient="vertical", command=self.tview_df_contents.yview) # command=update yaxis view of frame_ofTview
        tview_yscroll.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
        self.tview_df_contents.configure(xscrollcommand=tview_xscroll.set, yscrollcommand=tview_yscroll.set) # assign the scrollbars to frame_ofTview
        
        # FRAME 2 of 2: for Button: Browse File and Entry: Filepath
        self.frame_lower = tk.LabelFrame(self.window, text="Open and Browse DataFrames", fg="lightgrey", bg="#225479")
        self.frame_lower.grid(columnspan=self.MAXCOLUMNS-2, row=row+4, column=1, sticky="nswe", ipadx=10)
        
        button_browse_file = tk.Button(self.frame_lower, text="Open/Browse Excel File:", command=self.select_excel_file,
                                    font=self.font_bold)
        button_browse_file.grid(columnspan=2, row=self.MAXROWS, column=0, sticky="e", ipadx=5, padx=5)
                                
        self.entry_filepath = tk.Entry(self.frame_lower, width=50, font=self.font_default)
        self.entry_filepath.grid(row=self.MAXROWS, column=4, columnspan=5, padx=5, pady=5, ipady=5) 
        self.entry_filepath.delete(0, tk.END)
        self.entry_filepath.insert(0, self.save_filepath)
        
        for widget in self.frame_upper.winfo_children():
            widget.grid_configure(padx=5, pady=5)
        
                
    def capture_search_entries(self):
        while True:
            delay_seconds = 2
            # Check changes in searches (Business name and Location)
            if self.entry_search_what.get() == "":
                self.entry_search_what.insert(0, self.search_what)
                self.entry_search_what.grid()
                delay_seconds += 2
            if self.entry_search_location.get() == "":
                self.entry_search_location.insert(0, self.search_location)    
                self.entry_search_location.grid()        
                delay_seconds += 2
            self.search_what_trimmed = "".join(byte if byte.isalpha() else '-' for byte in self.entry_search_what.get())
            self.search_what_trimmed = self.search_what_trimmed.replace('--', '-')
            search_location = "".join(byte if byte.isalpha() else '-' for byte in self.entry_search_location.get())
            search_location = search_location.replace('--', '-')
            self.captured_url = f"https://www.yellow-pages.ph/search/{self.search_what_trimmed.lower()}/{search_location.lower()}/page-1".replace('--', '-')
            self.update_label_webpage()
            self.save_filepath = self.entry_filepath.get()
            # Check every 2 seconds
            time.sleep(delay_seconds)


    def start_thread_capture_search_entries(self):  # Call this function inside main()
        searchchanges_thread = threading.Thread(target=self.capture_search_entries)  # From threading module
        searchchanges_thread.daemcon = True  # This makes the thread exit when the main program exits
        searchchanges_thread.start()


    def stop_scraping(self):
        self.continue_scraping = NO
        self.button_go['text'] = "GO!"
        self.button_save['text'] = "Save Details"
        self.window.update()
        
        
    def start_auto_scraping(self):
        # self.start_thread_capture_search_entries(self.start_auto_scraping)
        self.continue_scraping = YES
        self.button_go['text'] = "BUSY"
        self.button_go.grid()
        self.button_save['text'] = "Saving Multiple Entries"
        self.button_save.grid()

        # Check/update search inputs
        self.search_what_trimmed = "".join(byte if byte.isalpha() else '-' for byte in self.entry_search_what.get())
        self.eeak_logs.append(self.search_what_trimmed + "\n")
        self.search_what_trimmed = self.search_what_trimmed.replace('--', '-')
        self.eeak_logs.append(self.search_what_trimmed + "\n")
        search_location = "".join(byte if byte.isalpha() else '-' for byte in self.entry_search_location.get())
        self.eeak_logs.append(search_location + "\n")
        search_location = search_location.replace('--', '-')
        self.eeak_logs.append(search_location + "\n")
        self.captured_url = f"https://www.yellow-pages.ph/search/{self.search_what_trimmed.lower()}/{search_location.lower()}/page-1".replace('--', '-')
        self.eeak_logs.append(self.captured_url + "\n")
        self.update_label_webpage()
        
        max_pages = 8  # There are 15 H2 URLs per page, recommended is 9 pages but for testing is 4
        for pagenum in range(1, max_pages+1):
            url = self.captured_url.replace("page-1", f"page-{pagenum}")
            self.update_label_webpage()
            try:  # if Website is valid or available
                webpage_response = requests.get(url, headers=self.headers)
            except requests.exceptions.MissingSchema:
                self.eeak_logs.append(f"Expected 'https://' in URL: {url}\n")
                return
            except ConnectionError:
                self.eeak_logs.append(f"{url} does not exist.\n")
                return
            except requests.exceptions.RequestException:
                self.eeak_logs.append(f"{url} is not availabe.\n")
                return

            soup = BeautifulSoup(webpage_response.text, "html.parser")
            try:
                soup = BeautifulSoup(webpage_response.text, "html.parser")
            except Exception as error:
                self.eeak_logs.append(f"{error}.\n")
            # Local HTML file test==========================================================
            # html_path = os.path.join(self.script_dir, "pharma_metro-manila_page-1.html")
            # with open(html_path, "rb") as webpage_response:            
            #     soup = BeautifulSoup(webpage_response.text, "html.parser")
            #===============================================================================
            
            # Gather all H2 Business names and their HTML elements
            all_h2_contents = soup.find_all("h2", class_="search-tradename")
            # Trim down to h2 family of elements and avoid AttribteError of None / No text found
            all_h2_elements = [h2_element.parent.parent.parent for h2_element in all_h2_contents]
            # Get search results by their H2 header and 
            for count, link in enumerate(all_h2_elements):
                self.check_stop_button_event()
                if self.continue_scraping == NO: 
                    break
                link_url = self.home_url + link.find("a")["href"]
                link_text = str(count) + link.find("h2").text
                h2_link_lowercase_text = str(link_text).lower()
                # Now, let's trim down the possibilty that non-hospital will not be scraped
                not_pharma_count = sum(1 for each in self.tuple_not_hospital if each in h2_link_lowercase_text)
                if not_pharma_count == 0:
                    if "hospital" in h2_link_lowercase_text:
                        self.eeak_logs.append("hospital" + h2_link_lowercase_text + "\n")
                        if link_url not in self.list_scraped_webpages:
                            self.eeak_logs.append("NOT YET SCRAPED!\n")
                            self.scrape_webpage(link_url)
                            self.list_scraped_webpages.append(link_url)
                        else:
                            self.eeak_logs.append("BUT SORRY, IT IS SCRAPED!\n")
                            continue
                    else:
                        self.eeak_logs.append("Maybe IT IS NOT a hospital!\n")
                        continue
                self.eeak_logs.append("\n")
        self.stop_scraping()

    def check_stop_button_event(self):
        self.button_stop = tk.Button(self.frame_upper, text="STOP", font=self.font_bold, command=self.stop_scraping)
        time.sleep(1)
        self.window.update()
        
        
    def scrape_webpage(self, url=""):
        if url == "": return
        try: # if Website is valid or available
            webpage_response = requests.get(url, headers=self.headers)
        except requests.exceptions.MissingSchema:
            self.eeak_logs.append(f"Expected 'https://' in URL: {url}")
            return
        except ConnectionError:
            self.eeak_logs.append(f"{url} does not exist.\n")
            return
        except requests.exceptions.RequestException:
            self.eeak_logs.append(f"{url} is not availabe.\n")
            return
        
        soup = BeautifulSoup(webpage_response.text, "html.parser")
        
        try:
            self.dict_business_info['Trade Name'] = soup.find("h1", class_="h1-tradename").text
        except AttributeError:
            try:
                self.dict_business_info['Trade Name'] = soup.find("h1", class_="h1-single-businessname").text
            except AttributeError:
                self.dict_business_info['Trade Name'] = ""
        try:
                self.dict_business_info['Short Description'] = soup.find("h2", class_="h2-businessname").text
        except AttributeError:
            hospital_descriptions = [
                "Healing at its finest.",
                "Your health, our mission.",
                "Excellence in healthcare.",
                "Caring for your well-being.",
                "Your trusted health partner.",
                "Innovative medical care.",
                "Quality healthcare close by.",
                "Compassion in every cure.",
                "Wellness starts with us.",
                "Your health, our priority.",
                "Care that counts most.",
                "Expertise in health.",
                "Dedicated to your well-being.",
                "Your health, our commitment.",
                "Caring, curing, comforting.",
                "Healthcare you can trust.",
                "In good hands, always.",
                "Healing, one patient at a time.",
                "Committed to your health.",
                "Where health comes first.",
                "Expert care, close to home.",
                "Empowering your well-being.",
                "Health, hope, and healing.",
                "Your journey to health.",
                "Experienced in caring.",
                "Your health, our passion.",
                "Dedicated to better health.",
                "Healing with compassion.",
                "Leading in patient care.",
                "Your trusted healthcare team.",
                "Innovation in medicine.",
                "Your health, our focus.",
                "Caring for life's moments.",
                "Healthcare excellence awaits.",
                "Where health meets heart.",
                "Care, compassion, and cures.",
                "Excellence in medical care.",
                "Your path to recovery.",
                "Committed to wellness.",
                "Healing with heart and soul.",
                "Your health, our promise.",
                "Elevating your well-being.",
                "Leading in healthcare solutions.",
                "Your trusted healing place.",
                "Innovation in patient care.",
                "Your health, our dedication.",
                "Dedicated to your health journey.",
                "Healing with expertise.",
                "Caring for your well-being.",
                "Empowering your health.",
                "Healthcare that matters most.",
                "Your well-being, our care.",
                "Innovating for better health.",
                "Your health, our mission.",
                "Elevating patient care.",
                "Healing, your way.",
                "Quality care, close to you.",
                "Your trusted health resource.",
                "Committed to compassionate care.",
                "Health solutions, your choice.",
                "Expert care, always here.",
                "Your health, our focus.",
                "Innovation in healthcare.",
                "Caring for brighter tomorrows.",
                "Leading in patient outcomes.",
                "Your path to recovery.",
                "Committed to your wellness.",
                "Healing lives, every day.",
                "Your health, our dedication.",
                "Elevating healthcare standards.",
                "Leading in medical excellence.",
                "Your trusted healthcare partner.",
                "Innovation in health solutions.",
                "Your health, our promise.",
                "Dedicated to your well-being.",
                "Healing for all generations.",
                "Quality care, your comfort.",
                "Your well-being, our mission.",
                "Committed to patient well-being.",
                "Healthcare that cares.",
                "Expert care, trusted results.",
                "Your health, our passion.",
                "Innovating for better care.",
                "Your trusted healing center.",
                "Leading in patient satisfaction.",
                "Your path to recovery.",
                "Empowering your health journey.",
                "Caring for your brighter future.",
                "Healing with heart and skill.",
                "Committed to excellence in care.",
                "Your health, our focus.",
                "Innovation in compassionate care.",
                "Quality healthcare, close to you.",
                "Your well-being, our dedication.",
                "Healthcare that listens.",
                "Your health, our promise.",
                "Dedicated to your brighter health.",
                "Leading in healthcare excellence.",
                "Your trusted care partner.",
                "Innovation in patient well-being.",
                "Your path to recovery.",
                "Caring for your brighter tomorrow.",
                "Healing lives, every day.",
                "Committed to your health journey.",
                "Healthcare for generations.",
                "Quality care, your comfort.",
                "Your well-being, our mission.",
                "Compassion in every cure.",
                "Expert care, trusted results.",
                "Your health, our passion.",
                "Innovating for better health.",
                "Your trusted healthcare team."
            ]
            self.eeak_logs.append(str(len(hospital_descriptions)) + "\n")
            if len(hospital_descriptions) > 1:
                picked_description = random.choice(hospital_descriptions)
                hospital_descriptions.remove(picked_description)
            else:
                picked_description = "A healthcare facility for medical treatment."
            self.dict_business_info['Short Description'] = picked_description
        
        if "clinic" in self.dict_business_info['Short Description'].lower():
            self.dict_business_info['Category'] = "Clinic"
        elif "center" in self.dict_business_info['Short Description'].lower():
            self.dict_business_info['Category'] = "Medical Center"
        else:
            self.dict_business_info['Category'] = "Hospital"
            
        try:
            self.dict_business_info['Address'] = soup.find("a", class_="biz-link yp-click").text
        except AttributeError:
            self.dict_business_info['Address'] = ""
        
        try:    
            self.dict_business_info['Contact Number'] = soup.find("span", class_="phn-txt").text
        except AttributeError:
            self.dict_business_info['Contact Number'] = ""
            
        try:
            self.dict_business_info['Email Address'] = soup.find("a", class_="email-link").text
        except AttributeError:
            self.dict_business_info['Email Address'] = ""
            
        try:
            self.dict_business_info['Facebook URL'] = "https://facebook.com/" + soup.find("a", class_="biz-link d-block ellipsis yp-click social-media-link").text
            self.dict_business_info['Facebook URL'] = self.dict_business_info['Facebook URL'].replace(" ", "") 
        except AttributeError:
            self.dict_business_info['Facebook URL'] = ""
        
        try:
            self.dict_business_info['Website'] = soup.find("a", class_="biz-link d-block ellipsis yp-click").text
        except AttributeError:
            try:
                self.dict_business_info['Website'] = soup.find("a", class_="website-link").text
                if self.dict_business_info['Website'].endswith("/"): 
                    self.dict_business_info['Website'] = self.dict_business_info['Website'].replace("/", "") 
            except AttributeError:
                self.dict_business_info['Website'] = ""
                
        self.update_entries()
        self.save_file()
        self.delay_by_randomseconds()
        
        
    def update_label_webpage(self):
        self.label_webpage = tk.Label(self.frame_upper, width=45, font=self.font_default,
                                      fg="#9acef5", bg="#134163",
                                      text=self.default_url if self.captured_url=="" else self.captured_url)
        self.window.update()
             
             
    def update_entries(self):
        for key in self.dict_business_info.keys():
            self.dict_entries_business[key].delete(0, tk.END)
            self.dict_entries_business[key].insert(0, self.dict_business_info[key])
            self.window.update()
    
    
    def udpate_tview_df_contents(self, data_frame):
        self.clear_data()
        self.tview_df_contents["column"] = list(data_frame.columns)
        self.tview_df_contents["show"] = "headings"
        for column in self.tview_df_contents["column"]:
            self.tview_df_contents.heading(column, text=column) # Headers will be all column names

        data_frame_rows = data_frame.to_numpy().tolist() # Rows from Excel will become list of NumPy Arrays, then just list
        for row in data_frame_rows: # Put each row in Treeview (tview_df_contents)
            self.tview_df_contents.insert("", index="end", values=row)      
        self.window.update() 
        
        
    def select_excel_file(self):
        self.save_filepath = filedialog.askopenfilename(
            initialdir="./",
            filetypes=[("Excel files", "*.xlsx"),
                       ("CSV files", "*.csv")]
            )
        if self.save_filepath:
            self.entry_filepath.delete(0, tk.END)
            self.entry_filepath.insert(0, self.save_filepath)
            self.df_business_infos = pd.read_excel(self.save_filepath) \
                if self.save_filepath.endswith("xlsx") else \
                    pd.read_csv(self.save_filepath)
            self.df_business_infos.dropna(inplace = True) # Delete rows with an emtpy cell from original DF
            self.df_business_infos.drop_duplicates(inplace = True) # Delete duplicates
        self.udpate_tview_df_contents(self.df_business_infos)
            
            
    def save_file(self):
        filename = self.save_filepath = self.entry_filepath.get()
        # Transfer dictionary data to tk Entries
        for key in self.dict_business_info.keys():
            self.dict_business_info[key] = self.dict_entries_business[key].get()
        # Add values from those tk Entries into our DataFrame
        self.df_business_infos = self.df_business_infos._append(self.dict_business_info, ignore_index=True)

        # Delete rows with an emtpy cell from original DF
        # self.df_business_infos.dropna(inplace = True)

        # Delete rows of duplicates from original DF
        self.df_business_infos.drop_duplicates(inplace = True)
        
        if filename.endswith("xlsx"):
            self.df_business_infos.to_excel(filename, index=False)
        elif filename.endswith("csv"):
            self.df_business_infos.to_csv(filename, index=False)
        self.udpate_tview_df_contents(self.df_business_infos)
        # time.sleep(2)
        

    def delay_by_randomseconds(self):
        # Setting delay to be gentle and not overload the website with fast and frequent request
        delaysecond = random.randint(3, 5) 
        for i in range(1, delaysecond):  # Applying delay in requesting webpages          
            self.eeak_logs.append(f"Automated in {delaysecond-i} {'second' if delaysecond-i == 1 else 'seconds'}...\n")
            time.sleep(1)
            

    def clear_data(self):
        self.tview_df_contents.delete(*self.tview_df_contents.get_children())
        

    def save_activity_logs(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # convert datetime obj to string
        str_current_datetime = str(current_datetime)
        # create a file object along with extension
        str_errors = "./logs/activities_logged-"
        filename = str_errors+str_current_datetime+".txt"
        if self.eeak_logs:
            self.eeak_logs.append("File of logged activties already exists.\n")
        else:
            self.eeak_logs.append("File of logged activties does not exist.\n")
        with open(filename, "w") as file:
            for each in self.eeak_logs:
                file.writelines(each)
        
        
    def run(self):
        # self.start_thread_capture_search_entries() 
        self.window.mainloop()
        
    
if __name__ == "__main__":
    application = YellowPagesPhScraper()
    application.run()
    application.save_activity_logs()