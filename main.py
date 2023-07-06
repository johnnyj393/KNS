# This is the code that will run weekly
import k
# Generate dates to print (next week classes)

# Have current classes variables - which ones to print
# How to get all info into one place: dict? So only prints those

# Call master loop

from admin_functions import *
from klass import Klass

# Assign all data to class practice
B2c = Klass(k.CLASSES[0])

# Create client
client = create_client_service_account()

B2c.set_up(client)

# Try to add the values to the pdf
new, blank, can, stream = start_edit()

can.drawString(100, 100, "One more step")

# End the edit and generate the pdf
end_edit(new, blank, can, stream)
