# Administrative functions

# - Creates pdf from image
# - Creates canvas and final pdf
# - Merge pdf
# - API to get data
# - Email with pdf attached

# -----------------------------------------------------------------

# Imports
import k
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# PDF editing
import io
from PyPDF2 import PdfWriter, PdfReader

# Google Sheets API
import google.auth
from google.auth.transport.requests import Request
import googleapiclient.discovery
import requests

# Email imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# -----------------------------------------------------------------

# Creates pdf from image
def make_daily_plan_from_img():
    # Open and resize the image
    image = ImageReader(k.BLANK_IMAGE_FILE)
    image_w, image_h = image.getSize()
    paper_w, paper_h = A4
    aspect_ratio = image_h / image_w

    # Scale image to fit within page and margins (width because it always gets scaled bigger)
    scale = (image_w - k.MARGINS) / (paper_w - k.MARGINS)
    new_width = (image_w - k.MARGINS) / scale

    # Account for aspect ratio and difference in height margin
    new_height = new_width * aspect_ratio
    height_margins = paper_h - new_height

    # Put image on canvas and save
    c = canvas.Canvas(k.SAVE_FILE_NAME, pagesize=A4)
    c.drawImage(image, k.MARGINS / 2, height_margins, width=new_width, height=new_height)
    c.save()


# -----------------------------------------------------------------

# Create canvas and final pdf
def start_edit():
    # Get the blank daily plan as a pdf single page
    pdf = PdfReader(open('files/daily_plan.pdf', 'rb'))
    blank_plan_page = pdf.pages[0]

    # Create new pdf page to put canvas and pdf on
    new_page = PdfWriter()

    # In-memory stream for the canvas
    temp_stream = io.BytesIO()

    # Create canvas to write on
    can = canvas.Canvas(temp_stream)

    # Set font and draw
    can.setFont(k.FONT, k.SIZE)

    # Return variables
    return new_page, blank_plan_page, can, temp_stream


def end_edit(new_page, blank_plan_page, can, temp_stream):
    # Save canvas content
    can.save()

    # Seek to the beginning of the stream
    temp_stream.seek(0)

    # Create content stream to merge
    content_stream = PdfReader(temp_stream).pages[0]
    blank_plan_page.merge_page(content_stream)

    new_page.add_page(blank_plan_page)

    with open('practice.pdf', 'wb') as file:
        new_page.write(file)


# -----------------------------------------------------------------

# Merge new pdf file into finished pdf


# -----------------------------------------------------------------

# API

# Create client

# UNUSED Use API key - couldn't get it to work
def create_client():
    return googleapiclient.discovery.build('sheets', 'v4', developerKey="AIzaSyBgq93ghAYXdjXnnUos7dDCeOGxN_YEA4A")


# Use service account for API call - works, so it's used
def create_client_service_account():
    # Load credentials from json file
    credentials, project = google.auth.load_credentials_from_file("json/google_api_credentials.json")
    sa_credentials = credentials.with_scopes(
        ['https://www.googleapis.com/auth/spreadsheets']
    )

    # Refresh credentials if necessary
    if sa_credentials.expired:
        sa_credentials.refresh(Request())

    # Create the Google sheets api client
    sheets_service = googleapiclient.discovery.build('sheets', 'v4', credentials=sa_credentials)
    return sheets_service


# UNUSED function to try to get the range to avoid getting unwanted data
def get_range(client, spreadsheet_id, sheet):
    sheet_properties = client.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=sheet).execute()
    last_row = sheet_properties['gridProperties']['rowCount']
    last_col = sheet_properties['gridProperties']['columnCount']
    return f"A1:{chr(64 + last_col)}{last_row}"


# Fetch
def fetch_data(client, spreadsheet_id, sheet):
    where = f"{sheet}!A1:ZZ"
    response = client.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=where
    ).execute()
    values = response.get('values', [])
    if not values:
        print("No data found.")
        return 1
    else:
        return values


# -----------------------------------------------------------------

# Email with pdf attached to gmail
def email():
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = k.MY_EMAIL
    message['To'] = k.RECEIVER_EMAIL
    message['Subject'] = k.EMAIL_SUBJECT

    # The body and attachment
    message.attach(MIMEText(k.EMAIL_BODY, 'plain'))

    with open(k.EMAIL_FILE_NAME, 'rb') as attach_file:
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload(attach_file.read())
        encoders.encode_base64(payload)

        # Add payload header with filename
        payload.add_header('Content-Disposition', 'attachment', filename=k.EMAIL_FILE_NAME)
        message.attach(payload)

        # Create SMTP session
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(k.MY_EMAIL, k.PASSWORD)
        text = message.as_string()
        session.sendmail(k.MY_EMAIL, k.RECEIVER_EMAIL, text)
        session.quit()
