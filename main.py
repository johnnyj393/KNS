from admin_functions import *
from klass import Klass
from PyPDF2 import PdfWriter

dates = ["7/10/2023", "7/11/2023", "7/12/2023", "7/13/2023", "7/14/2023"]

# Create client
client = create_client_service_account()

# Output multipage file
final_pdf = PdfWriter()

# Initialize class
B2c = Klass(k.CLASSES[0])
B2c.set_up(client)

# Puts values of class days, books, and nt_books into class
B2c.fetch_books(client, dates)

final_pdf = B2c.write_curriculum(final_pdf)

with open("practice.pdf", "wb") as file:
    final_pdf.write(file)
