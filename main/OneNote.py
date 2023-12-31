from M_OAuth import generate_access_token
from pprint import pprint
import requests
import bleach

# Setup for Azure AD
APP_ID = "98c8b6c2-6df4-4765-ac02-4c32cf868661"
SCOPES = [
    "Notes.Create",
    "Notes.ReadWrite"
]

# Setup Base Graph Endpoint
GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0'

# Generate access token
access_token = generate_access_token(APP_ID, SCOPES)
headers = {
    'Authorization': 'Bearer ' + access_token['access_token']
}




# Generate Notebook
def CreateNoteBook(year):
    # Request for creating Notebook
    notebook_endpoint = GRAPH_ENDPOINT + '/me/onenote/notebooks' # Generate Notebook Endpoint
    request_body = { # Generate Request Body
        "displayName": str(year)
    }
    response = requests.post(notebook_endpoint, headers=headers, json=request_body)

    # Extract Notebook ID
    response_data = response.json()
    notebook_url = response_data['links']['oneNoteWebUrl']['href']
    notebook_id = response_data["id"]

    
    # Return Notebook ID
    return notebook_url,notebook_id


# Generate Section
def CreateSection(month,notebook_id):
    # Request for creating Section
    section_endpoint = GRAPH_ENDPOINT + f'/me/onenote/notebooks/{notebook_id}/sections'
    request_body = {
        "displayName": month
    }
    response = requests.post(section_endpoint, headers=headers, json=request_body)

    # Extract Section ID
    section_id = response.json()["id"]

    # Return Section ID
    return section_id



# Generate Page
def CreatePage(day, events, date, section_id):
    # Request for creating Page
    headers = {
        'Authorization': 'Bearer ' + access_token['access_token'],
        'Content-type': 'text/html; charset=utf-8'  # Set charset to UTF-8
    }

    # Get page endpoint
    page_endpoint = GRAPH_ENDPOINT + f'/me/onenote/sections/{section_id}/pages'

########## CODE SMELL(remove for loop)
########## (Use key to find value)
    # Find matching events
    matching_values = [bleach.clean(event) for key, value in events.items() for event in value if date in key]

    # Return matching events
    if matching_values:
        value_html = "".join([f"<p data-tag='to-do'>{value}</p>" for value in matching_values])

        # Encode the HTML data as UTF-8
        html_encoded = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{day}</title></head><body>{value_html}</body></html>'.encode('utf-8')
    else:
        html_encoded = f'<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{day}</title></head><body></body></html>'.encode('utf-8')


    # Create a page
    response = requests.post(page_endpoint, headers=headers, data=html_encoded)

    # Return log of page creations
    page = response.json()    
    return page