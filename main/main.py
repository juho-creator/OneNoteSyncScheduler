import sys
from OneNote import *
from G_OAuth import * 
import inflect
import calendar
from G_OAuth import retrieve_schedule
import webbrowser
from flask import Flask, request, render_template

# Setting up date tracker
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12']
p = inflect.engine()

creds = get_credentials()

try:
    year = input("Input year > ")

    print(f"\nCREATING NOTEBOOK FOR {year}")
    print("It takes 5~10 min depending on your calendar so go grab yourself a coffee!\n")

    # Retrieve all events
    events = retrieve_schedule(int(year))

    # 1. Create Notebook
    notebook_url,notebook_id = CreateNoteBook(str(year))

    # 2. Create sections for month
    for month in months:
        month_name = calendar.month_name[int(month)]
        section_id = CreateSection(month_name, notebook_id)
        print(f"Creating {month_name}...")
        
        # Caculate number of days in a month
        days = calendar.monthrange(int(year), int(month))[1]
        
        # Create page with events
        for day in range(1,days+1):
            ordinal = p.ordinal(day)
            if day>9:  
                date = f'{year}-{month}-{day}' # Create date format for checking
            else:
                date = f'{year}-{month}-0{day}' # Create date format for checking
            page = CreatePage(ordinal,events,date,section_id)
    print(f"\n{year} Notebook Created : {notebook_url}")

except KeyError:
    print("Notebook Already exists")

input("Press Enter to exit...")
