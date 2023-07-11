# Main

# Manual / Auto Toggle
# PDF Generation

# -----------------------------------------------------------------

from klass import Klass
from PyPDF2 import PdfWriter
from admin_functions import *

# -----------------------------------------------------------------

# Manual / Auto Toggle

# Manual Mode
manual_mode = True
start_date = "7/11/2023"
end_date = "7/16/2023"
choose_classes = ["B2c"]

if manual_mode:
    # Get dates from input
    dates, file_name = get_dates(start_date, end_date)
    # Get selected classes
    classes = get_classes(choose_classes)
else:
    # Weekly Auto Mode: today + 6 days ahead
    dates, file_name = get_dates()
    # Select all classes
    classes = k.CLASSES

# -----------------------------------------------------------------

# Proceed with pdf generation

# Create client for API
client = create_client_service_account()

# Generate master pdf
pdf = PdfWriter()

# Master loop to generate all pages
for group in classes:
    klass = Klass(group)
    klass.set_up(client)
    klass.fetch_books(client, dates)
    klass.fetch_tests_wcq(client)
    pdf = klass.write_curriculum(pdf)

# Save file for reference, optional
# with open("practice.pdf", "wb") as file:
#     pdf.write(file)

# Email final pdf
email(pdf, file_name)
