# Main
import k
# Manual / Auto Toggle
# PDF Generation

# -----------------------------------------------------------------

from klass import Klass
from PyPDF2 import PdfWriter
from admin_functions import *


# -----------------------------------------------------------------

def master_generate(manual_mode=False, start_date=None, end_date=None, choose_classes=None):
    # Manual / Auto Toggle - governed by input

    if start_date is None:
        start_date = datetime.now().date().strftime("%-m/%-d/%Y")
    if end_date is None:
        end_date = datetime.now().date().strftime("%-m/%-d/%Y")
    if choose_classes is None:
        choose_classes = [item[k.NAME] for item in k.CLASSES]

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


master_generate(True, "8/7/2023", "8/11/2023")
