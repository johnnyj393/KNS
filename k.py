# Constants

# Sections

# Google and Initialization
# 1 Initialization data for klass
#   - Name
#   - Spreadsheet ID
#   - Image file name for that class
# 2 Sheets names in google
# 3 Column numbers of tests and wcq in sheet in google

# Fonts and Text
# 1 - Fonts: Arial and Arial bold
# 2 - Text sizes: Various text size variables

# PDF Data
# 1 - Margins for PDF generation from image
# 2 - Name of image file used to make new pdf
# 3 - Name of location to save file to

# Email Data
# 1 - Sender info
# 2 - Receiver info
# 3 - Email text info: title, body, email file name

# Coordinates and Data
# 1 - All text placement coordinates
# 2 - Text wrapping coordinates and data
# 3 - Circle coordinates and data
# 4 - Box file names for reference

# -----------------------------------------------------------------

# Imports - for fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# -----------------------------------------------------------------

# Google
NAME = "name"
ID = "spreadsheet_id"
IMAGE = "image"

# Spreadsheet IDs
CLASSES = [
    {
        NAME: "B1a",
        ID: "1hd-OkgrCs7oPbhmr-xH9lpg8JdU04gBgGcEHjjYEK8w",
        IMAGE: "images/boxes/MWThF24.png"
    },
    {
        NAME: "C1a",
        ID: "1I3CQrZhLRUsufYOBz9hql3nECg6jiqxpZn33Y7IKz98",
        IMAGE: "images/boxes/MWTh79.png"
    },
    {
        NAME: "C3b",
        ID: "1NALyxgKDzyHySViGBeQcW8_o5ORrd235XKdbkcrLzTQ",
        IMAGE: "images/boxes/MWTh57.png"
    },
    {
        NAME: "C5b",
        ID: "11IQLWtOu1GL-pgHgQGSOB-mRIX5-uTMjDTvT5bsrM8w",
        IMAGE: "images/boxes/TWF57.png"
    },
    {
        NAME: "PET",
        ID: "1McKp2SA105FXeh-lWlG649w0X9MxM87iSSkLS7knp9s",
        IMAGE: "images/boxes/TF79.png"
    }
]

# Names of sheets for API calls
BOOKS_SHEET = "Books"
TESTS_SHEET = "Tests"
INFO_SHEET = "Class Info"

# Columns of tests and wcq in google sheets
TEST_DATE = 0
TEST = 1
WCQ_DATE = 6
WCQ = 7

# -----------------------------------------------------------------

# Fonts
pdfmetrics.registerFont(TTFont("Arial", 'fonts/ARIAL.TTF'))
pdfmetrics.registerFont(TTFont("Arialbd", "fonts/ARIALBD.TTF"))
FONT = "Arial"
FONT_BOLD = "Arialbd"

# Text sizes
TITLE_SIZE = 14
DEFAULT_SIZE = 12
TEST_SIZE = 10
WCQ_SIZE = 8
TIMESTAMP_SIZE = 7

# -----------------------------------------------------------------

# PDF Generation Data
MARGINS = 23
# Picture to use to generate pdf of blank curriculum plan page
BLANK_IMAGE_FILE = "images/daily_plan.png"
# Generated pdf file save location and name
SAVE_FILE_NAME = "files/daily_plan_new.pdf"

# -----------------------------------------------------------------

# Email data
# Sender data
MY_EMAIL = "johnsantangelo121@gmail.com"
PASSWORD = "vhofcfxceqnuojhw"
# Receiver data
RECEIVER_EMAIL = "johnsantangelo121@yahoo.com"
# Email text data
EMAIL_SUBJECT = "Daily Plans"
EMAIL_BODY = "Here are the daily plans for this week."
EMAIL_FILE_NAME = "daily_plans.pdf"

# -----------------------------------------------------------------

# COORDINATES
# Info Placement
TEACHER_X = 110
TEACHER_Y = 730
NAME_X = 300
NAME_Y = 729
DATE_X = 470
DATE_Y = 729

# Students
STUDENTS_LEFT_X = 35
STUDENTS_TOP_START = 352
STUDENTS_RIGHT_X = 315
STUDENTS_GO_DOWN = 21.5

# Books
BOOKS_LEFT_X = 175
BOOKS_TOP_START = 692
BOOKS_RIGHT_X = 470
BOOKS_GO_DOWN = 27
NT_BOOKS_X = 155
NT_BOOKS_Y = 552

# Tests
TODAY_TEST_X = 65
TODAY_TEST_Y = 500
NT_TEST_X = 343
NT_TEST_Y = 500

# WCQ
WCQ_X = 25
WCQ_Y = 415
NT_WCQ_X = 305
NT_WCQ_Y = 415

# Image box
IMAGE_X = 13
IMAGE_Y = 38
IMAGE_WIDTH = 190
IMAGE_HEIGHT = 60

# Timestamp
TIMESTAMP_X = 510
TIMESTAMP_Y = 42

# Text Wrapping
TEST_PROP = "test"
WCQ_PROP = "wcq"
BOOK_PROP = "book"
LENGTH = "length"
NEW_LINE = "new line"
BIG_LENGTH = "big length"

# Properties
PROP = {
    TEST_PROP: {
        LENGTH: 55,
        NEW_LINE: 18
    },
    WCQ_PROP: {
        LENGTH: 70,
        NEW_LINE: 10
    },
    BOOK_PROP: {
        BIG_LENGTH: 15,
        LENGTH: 28,
        NEW_LINE: 12
    }
}

# Circles
TODAY = "today"
NT = "nt"

# Values for tests
WT = "WT"
VT = "VT"
ST = "ST"

W1 = 40
W2 = 318
H1 = 508
H2 = 489
H3 = 470

RADIUS = 10

CIRCLES = {
    TODAY: {
        WT: [W1, H1],
        VT: [W1, H2],
        ST: [W1, H3]
    },
    NT: {
        WT: [W2, H1],
        VT: [W2, H2],
        ST: [W2, H3]
    }
}

# Boxes
# All codes for boxes so far
# These are the same name as their image file minus .png
# MWThF24
# MWTh57
# TWF57
# MWTh79
# TWF79
# MTh79
# TF79
