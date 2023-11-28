# Administrative functions

# Sections

# Imaging and PDF generation
# 1 - make_daily_plan_from_img      Creates pdf from image with margins

# Canvas and content management
# 1 - start_edit                    Creates canvas and content stream to write on
# 2 - end_edit                      Merges written data onto blank plan page, returns single pdf page

# API management
# 1 - create_client_service_account Creates client for API calls
# 2 - fetch_data                    Inputs of client, spreadsheet, sheet, returns all data inside

# Data generation
# 1 - get_dates                     Takes optional inputs of start and end date, returns dates between, email file name
# 2 - get_classes                   Takes a string of classes, returns dicts in classes array from k data that match

# Email
# 1 - email                         Input a pdf, sends email with input pdf attached

# -----------------------------------------------------------------

# Imports
import k
from datetime import datetime, timedelta
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
    c.drawImage(image, k.MARGINS / 2, height_margins - 10, width=new_width, height=new_height)
    c.save()


# -----------------------------------------------------------------

# Create canvas and final pdf
def start_edit():
    # In-memory stream for the canvas
    temp_stream = io.BytesIO()

    # Create canvas to write on
    can = canvas.Canvas(temp_stream)

    # Set font and size as normal
    can.setFont(k.FONT, k.DEFAULT_SIZE)

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

# Create client using service account for API call
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


# Fetch all data from inputted spreadsheet and sheet
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

# Gets all dates from start date to number of days in the future
def get_dates(
        start_date=(datetime.now().date() + timedelta(days=7)),
        end_date=(datetime.now() + timedelta(days=12)).date()
):
    # If they get passed in manually, they will be strings, so switch them to dates
    if type(start_date) == str:
        start_date = datetime.strptime(start_date, "%m/%d/%Y").date()  # type: ignore
    if type(end_date) == str:
        end_date = datetime.strptime(end_date, "%m/%d/%Y").date()  # type: ignore

    # Create file name to email including dates
    sm = start_date.month
    sd = start_date.day
    sy = start_date.year
    em = end_date.month
    ed = end_date.day
    ey = end_date.year
    file_name = f"daily_plans_{sm}.{sd}.{sy}-{em}.{ed}.{ey}.pdf"

    # Initialize dates array to store every date
    dates = []

    # Generate and store all days as strings between days including end date
    while start_date <= end_date:
        day = start_date.strftime("%-m/%-d/%Y")
        dates.append(day)
        start_date += timedelta(days=1)

    return dates, file_name


# Return classes to be used manually
def get_classes(classes):
    # Initialize return of classes
    choose_classes = []

    # Edit classes to write curriculum plans for from given input
    for name in classes:
        chosen_class = [group for group in k.CLASSES if group[k.NAME] == name]
        # There will only be one match, so should put [0] to get the value, so it's not an array
        choose_classes.append(chosen_class[0])

    return choose_classes


# -----------------------------------------------------------------

# Email with pdf attached to gmail
def email(pdf, email_file_name):
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
    attachment.add_header('Content-Disposition', 'attachment', filename=email_file_name)
    message.attach(attachment)

    # Create SMTP session
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(k.MY_EMAIL, k.PASSWORD)
    text = message.as_string()
    session.sendmail(k.MY_EMAIL, k.RECEIVER_EMAIL, text)
    session.quit()
