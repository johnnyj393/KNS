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
from PyPDF2 import PdfReader

# Google Sheets API
import google.auth
from google.auth.transport.requests import Request
import googleapiclient.discovery

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
    c.drawImage(image, k.MARGINS / 2, height_margins-10, width=new_width, height=new_height)
    c.save()


# -----------------------------------------------------------------

# Create canvas and final pdf
def start_edit():
    # In-memory stream for the canvas
    temp_stream = io.BytesIO()

    # Create canvas to write on
    can = canvas.Canvas(temp_stream)

    # Set font and size as normal
    can.setFont(k.FONT, k.SIZE_12)

    # Return variables
    return can, temp_stream


def end_edit(can, temp_stream):
    # Get the blank daily plan as a pdf single page
    pdf = PdfReader(open('files/daily_plan.pdf', 'rb'))
    daily_plan_blank = pdf.pages[0]

    # Save canvas content
    can.save()
    temp_stream.seek(0)
    temp_pdf = PdfReader(temp_stream)
    temp_page = temp_pdf.pages[0]

    # Add stream to pdf
    daily_plan_blank.merge_page(temp_page)

    return daily_plan_blank

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
def email(pdf):
    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = k.MY_EMAIL
    message['To'] = k.RECEIVER_EMAIL
    message['Subject'] = k.EMAIL_SUBJECT

    # The body and attachment
    message.attach(MIMEText(k.EMAIL_BODY, 'plain'))

    # Extract pdf content to be read as a stream
    pdf_stream = io.BytesIO()
    pdf.write(pdf_stream)
    pdf_stream.seek(0)

    # Create attachment from pdf content
    attachment = MIMEBase('application', 'pdf')
    attachment.set_payload(pdf_stream.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=k.EMAIL_FILE_NAME)
    message.attach(attachment)

    # Create SMTP session
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(k.MY_EMAIL, k.PASSWORD)
    text = message.as_string()
    session.sendmail(k.MY_EMAIL, k.RECEIVER_EMAIL, text)
    session.quit()
