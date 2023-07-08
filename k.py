# Constants File

# Imports - for fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# -----------------------------------------------------------------

# Google
NAME = "name"
ID = "spreadsheet_id"

# Names of sheets for API calls
BOOKS_SHEET = "Books"
TESTS_SHEET = "Tests"
INFO_SHEET = "Class Info"

# Spreadsheet IDs
CLASSES = [
    {
        NAME: "B2c",
        ID: "1NALyxgKDzyHySViGBeQcW8_o5ORrd235XKdbkcrLzTQ"
    },
    {
        NAME: "C4e",
        ID: "1xihlr6qmK6YNBqzY6jmgKev_3KKdfRmV6KBOcsckG1I"
    },
    {
        NAME: "C5c",
        ID: "1lq6XSUwLDggocUVSy28cik_Z5FhsGd37GNr6RKcB20c"
    },
    {
        NAME: "KET",
        ID: "1McKp2SA105FXeh-lWlG649w0X9MxM87iSSkLS7knp9s"
    }
]


# -----------------------------------------------------------------
# Font and text size
pdfmetrics.registerFont(TTFont("Arial", 'fonts/ARIAL.TTF'))
pdfmetrics.registerFont(TTFont("Arialbd", "fonts/ARIALBD.TTF"))
FONT = "Arial"
FONT_BOLD = "Arialbd"
SIZE_14 = 14
SIZE_12 = 12


# -----------------------------------------------------------------
# PDF Generation data
MARGINS = 23
BLANK_IMAGE_FILE = "images/daily_plan.png"
SAVE_FILE_NAME = "daily_plan.pdf"

# PDF data
PRACTICE = "practice.pdf"
BLANK_DAILY_PLAN = "daily_plan_blank.pdf"


# -----------------------------------------------------------------
# Email data
MY_EMAIL = "johnsantangelo121@gmail.com"
PASSWORD = "vhofcfxceqnuojhw"
RECEIVER_EMAIL = "johnsantangelo121@yahoo.com"
EMAIL_SUBJECT = "Daily Plans"
EMAIL_BODY = "Here are the daily plans for this week."
EMAIL_FILE_NAME = "daily_plans.pdf"


# -----------------------------------------------------------------
# COORDINATES
# Info
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
