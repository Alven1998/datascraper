from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Docs API authentication
SERVICE_ACCOUNT_FILE = r'C:\Users\AMRYTT2.0\Downloads\deshboard-426016-45b6bea044c6.json'  # Path to your Google Docs credentials JSON file
SCOPES = ['https://www.googleapis.com/auth/documents.readonly', 'https://www.googleapis.com/auth/drive.readonly']
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
docs_service = build('docs', 'v1', credentials=credentials)

# Google Sheets API authentication
SHEET_SERVICE_ACCOUNT_FILE = r'C:\Users\AMRYTT2.0\Downloads\deshboard-426016-45b6bea044c6.json'  # Path to your Google Sheets credentials JSON file (can be the same as Google Docs)
SHEET_SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
sheet_credentials = ServiceAccountCredentials.from_json_keyfile_name(SHEET_SERVICE_ACCOUNT_FILE, SHEET_SCOPES)
sheet_client = gspread.authorize(sheet_credentials)

# Replace with your actual Google Sheet URL
sheet_url = 'https://docs.google.com/spreadsheets/d/1tqau09rHlyQZozQTvIaJ1-LhFq-VMQqr4A3AJPu9KOU/edit?gid=0#gid=0'  # Replace with your Google Sheet URL

# Extract the sheet ID from the URL
sheet_id = sheet_url.split('/')[5]

# Open the Google Sheet by ID
sheet = sheet_client.open_by_key(sheet_id).sheet1  # Open the sheet by its ID and select the first sheet

# Fetch all URLs from column A
document_urls = sheet.col_values(1)[1:]  # Skip the header row

def extract_links(doc_content):
    links = []
    for element in doc_content:
        if 'paragraph' in element:
            for el in element['paragraph']['elements']:
                if 'textRun' in el and 'textStyle' in el['textRun']:
                    text_run = el['textRun']
                    text_style = text_run['textStyle']
                    if 'link' in text_style:
                        url = text_style['link']['url']
                        anchor_text = text_run['content']
                        links.append((anchor_text, url))
    return links

for index, doc_url in enumerate(document_urls, start=2):  # Start from row 2 to skip header
    # Extract the document ID from the URL
    parts = doc_url.split('/')
    if len(parts) > 5:
        doc_id = parts[5]
    
        try:
            # Fetch the document
            doc = docs_service.documents().get(documentId=doc_id).execute()

            # Extract content
            content = doc.get('body').get('content')
            links = extract_links(content)

            # Prepare the row data
            row_data = [doc_url]
            for anchor_text, url in links:
                row_data.extend([anchor_text, url])

            # Determine the range to update
            cell_range = f"B{index}:ZZ{index}"
            sheet.update(range_name=cell_range, values=[row_data])
        
        except Exception as e:
            # Log the error and continue to the next document
            print(f"Failed to process {doc_url}: {e}")
    else:
        print(f"Invalid URL format: {doc_url}")

print("Anchor texts and backlinks have been saved to Google Sheets.")
