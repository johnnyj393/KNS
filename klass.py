# Klass

# Sections

# Data Initiation
# 1 - init                  Initializes basic data from k file and initializes all other data for klass
# 2 - set_up                Input client, uses variables from klass to initialize teacher and student data

# Write
# 1 - write_info            Input date and canvas, writes teacher, class, date, students, timestamp, and image to canvas
# 2 - write_books           Input date and canvas, writes books and books for next class to canvas
# 3 - write_tests_wcq       Input date and canvas, writes tests and wcq to canvas
# 4 - draw_circle           Input canvas, today or next class, and text, draws circle in correct spot
# 5 - text_wrap             Input canvas, properties, and data to write, wraps text based on dimensions from k
# 6 - write_curriculum      Input pdf file, generates a curriculum plan for every date in dates, returns final pdf

# Fetch data
# 1 - fetch_books           Input client and dates, saves dates, books, nt_books from Google sheets data in self
# 2 - fetch_tests_wcq       Input client, saves tests and wcq from Google sheets data in self

# -----------------------------------------------------------------

# Imports
import pandas as pd
from admin_functions import *


# -----------------------------------------------------------------


class Klass:
    def __init__(self, class_data):
        # Admin data from k
        self.name = class_data[k.NAME]
        self.spreadsheet_id = class_data[k.ID]
        self.image = class_data[k.IMAGE]
        # Admin data from google
        self.teacher = ""
        self.students = []
        self.timestamp = ""
        # Data
        self.dates = {}     # Date: NT Date
        self.books = {}     # Date: {book: page}
        self.nt_books = {}  # Date: nt books
        self.tests = {}     # Date: [today test, nt test]
        self.wcq = {}       # Date: [today wcq, nt wcq]

    # Initializes admin data from Google - teacher, schedule (time), and current students
    def set_up(self, client):
        # Set up timestamp to print later
        self.timestamp = datetime.now().strftime("%m/%d/%Y %H:%M")

        # Get info data from google
        values = fetch_data(client, self.spreadsheet_id, k.INFO_SHEET)
        for value in values:
            if value[0] == 'Teacher':
                self.teacher = value[1]
            elif value[0] == 'Students':
                for student in value[1:len(value)]:
                    self.students.append(student)

    # -----------------------------------------------------------------

    # Writes basic info like teacher, class, date, students, timestamp, and image to canvas
    def write_info(self, date, c):
        # Set font for titles - bold, 14
        c.setFont(k.FONT_BOLD, k.TITLE_SIZE)

        # Teacher
        c.drawString(k.TEACHER_X, k.TEACHER_Y, self.teacher)
        # Name
        c.drawString(k.NAME_X, k.NAME_Y, self.name)
        # Date
        c.drawString(k.DATE_X, k.DATE_Y, date)

        # Reset to normal - no bold, 12
        c.setFont(k.FONT, k.DEFAULT_SIZE)

        # Set up
        alt = True
        y = k.STUDENTS_TOP_START

        # Write to canvas
        for student in self.students:
            if alt:
                c.drawString(k.STUDENTS_LEFT_X, y, student)
                alt = False
            else:
                c.drawString(k.STUDENTS_RIGHT_X, y, student)
                y -= k.STUDENTS_GO_DOWN
                alt = True

        # Image
        c.drawImage(self.image, k.IMAGE_X, k.IMAGE_Y, k.IMAGE_WIDTH, k.IMAGE_HEIGHT)

        # Timestamp
        # Make text smaller for stamp
        c.setFont(k.FONT, k.TIMESTAMP_SIZE)
        # Draw it
        c.drawString(k.TIMESTAMP_X, k.TIMESTAMP_Y, self.timestamp)
        # Return font and size to default
        c.setFont(k.FONT, k.DEFAULT_SIZE)

        return c

    # Writes the books for that day to correct places as well as nt books to canvas
    def write_books(self, date, c):
        # Set up
        y = k.BOOKS_TOP_START

        # Write to canvas
        for key, value in self.books[date].items():
            c.drawString(k.BOOKS_LEFT_X, y, key)
            if len(value) > k.PROP[k.BOOK_PROP][k.BIG_LENGTH]:
                self.text_wrap(c, k.BOOK_PROP, k.BOOKS_RIGHT_X, y, value)
            else:
                c.drawString(k.BOOKS_RIGHT_X, y, value)
            y -= k.BOOKS_GO_DOWN

        # Make nt_books string
        nt_books_string = self.nt_books[date][0]
        for value in self.nt_books[date][1:]:
            nt_books_string += f", {value}"

        # Write to canvas
        c.drawString(k.NT_BOOKS_X, k.NT_BOOKS_Y, nt_books_string)

        return c

    # Writes the test for that day and next times test
    def write_tests_wcq(self, date, c):
        # Set font for tests
        c.setFont(k.FONT, k.TEST_SIZE)

        # Write test for the day
        self.text_wrap(c, k.TEST_PROP, k.TODAY_TEST_X, k.TODAY_TEST_Y, self.tests[date][0])
        self.draw_circle(c, k.TODAY, self.tests[date][0])

        # Write nt test for the next day in dates
        self.text_wrap(c, k.TEST_PROP, k.NT_TEST_X, k.NT_TEST_Y, self.tests[date][1])
        self.draw_circle(c, k.NT, self.tests[date][1])

        # Set font for WCQ
        c.setFont(k.FONT, k.WCQ_SIZE)

        # Write wcq for day if there is one
        if self.wcq[date][0] != "":
            self.text_wrap(c, k.WCQ_PROP, k.WCQ_X, k.WCQ_Y, self.wcq[date][0])

        # Write nt wcq for day if there is one
        if self.wcq[date][1] != "":
            self.text_wrap(c, k.WCQ_PROP, k.NT_WCQ_X, k.NT_WCQ_Y, self.wcq[date][1])

        # Set font back to default
        c.setFont(k.FONT, k.DEFAULT_SIZE)

        return c

    # Draws circle depending on what test it is
    # noinspection PyMethodMayBeStatic
    def draw_circle(self, c, when, text):
        if k.WT in text:
            x = k.CIRCLES[when][k.WT][0]
            y = k.CIRCLES[when][k.WT][1]
            r = k.RADIUS
            c.circle(x, y, r)
        elif k.VT in text:
            x = k.CIRCLES[when][k.VT][0]
            y = k.CIRCLES[when][k.VT][1]
            r = k.RADIUS
            c.circle(x, y, r)
        elif k.ST in text:
            x = k.CIRCLES[when][k.ST][0]
            y = k.CIRCLES[when][k.ST][1]
            r = k.RADIUS
            c.circle(x, y, r)

    # Wraps text neatly given constants in k
    # noinspection PyMethodMayBeStatic
    def text_wrap(self, c, prop, x, y, text):
        # Replace new lines so that there are no weird symbols instead of a new line
        text.replace("\n", "")

        # Modify smaller font for special book case
        if prop == k.BOOK_PROP:
            # Change font
            c.setFont(k.FONT, k.WCQ_SIZE)

        # Set initials
        lines = []
        current_line = ""
        words = text.split()

        # Split into lines
        for word in words:
            if len(current_line) + len(word) <= k.PROP[prop][k.LENGTH]:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        # Add what is left of the current line if necessary
        if current_line:
            lines.append(current_line.strip())

        # If books is more than 1 line we have to adjust and move y value up to have enough space for two lines
        if len(lines) > 1 and prop == k.BOOK_PROP:
            # New height - go up
            y += k.PROP[k.BOOK_PROP][k.NEW_LINE]

        # Print onto canvas accordingly
        for line in lines:
            c.drawString(x, y, line)
            y -= k.PROP[prop][k.NEW_LINE]

        # Change font back if prop was from books
        if prop == k.BOOK_PROP:
            c.setFont(k.FONT, k.DEFAULT_SIZE)

    # Looped curriculum writer - writes a curriculum plan page for each date in self.dates
    def write_curriculum(self, pdf):
        # Generates a pdf page for every day in dates
        for date in self.dates:
            c, stream = start_edit()
            c = self.write_info(date, c)
            c = self.write_books(date, c)
            c = self.write_tests_wcq(date, c)
            new_page = end_edit(c, stream)
            pdf.add_page(new_page)

        return pdf

    # -----------------------------------------------------------------

    # Fetch data and stores them in class instance functions
    def fetch_books(self, client, dates):
        # Get data from API
        data = fetch_data(client, self.spreadsheet_id, k.BOOKS_SHEET)

        # Save column headers
        column_headers = data[0]

        # Get data matching the dates to print daily plans for
        filtered_data = [row for row in data if row[0] in dates]

        # Extra row for next times books
        next_row_index = data.index(filtered_data[len(filtered_data) - 1]) + 1
        filtered_data.append(data[next_row_index])

        # Number of columns in each row must equal number of column headers to avoid error when creating dataframe
        for row in filtered_data:
            while len(row) < len(column_headers):
                row += [""]

        # Make dataframe
        df = pd.DataFrame(filtered_data, columns=column_headers)

        # Make sure there are no None or NaN values
        df.fillna("", inplace=True)

        # Data storage
        for index, row in df.iterrows():

            # Convert index to int instead of hashable
            # noinspection PyTypeChecker
            index = int(index)

            # Initialize variables
            date = row[0]
            daily_books = {}

            # NT books array - will store the same books as for that day but with different date later on
            if index > 0:
                nt_date = df.iloc[index - 1, 0]
                nt_books = []
            else:
                nt_date = ""
                nt_books = []

            # Go through each column with a value in it: column header is book, value in cell in page for that day
            for column, value in row.iloc[1:].items():

                # Store value if not blank
                if value != "":
                    # Exception for +WB - combine with last entry
                    if column == "WB":
                        # noinspection PyUnboundLocalVariable
                        old_value = daily_books[last_column]    # last_column will only EVER be accessed after assigned
                        column = last_column + " + " + column
                        value = old_value + " / " + value
                        del daily_books[last_column]

                    # Still make new entry no matter what
                    daily_books[column] = value

                    # For +WB contingency, must have access to last column title
                    last_column = column

            # Populate nt_books with all the books from the current days books
            for book in daily_books:
                nt_books.append(book)

            # Put new value sets into appropriate place
            if index < len(df) - 1:
                self.dates[date] = df.iloc[index+1, 0]
                self.books[date] = daily_books
            if index > 0:
                self.nt_books[nt_date] = nt_books

    def fetch_tests_wcq(self, client):
        # Get data from API
        data = fetch_data(client, self.spreadsheet_id, k.TESTS_SHEET)
        df = pd.DataFrame(data)

        # Make dataframe for tests
        tests_df = (
            df[df[k.TEST_DATE].isin(self.dates) | df[k.TEST_DATE].isin(self.dates.values())]
            .iloc[:, k.TEST_DATE:k.TEST+1]
        )

        # Put into proper dictionary
        for date, nt_date in self.dates.items():
            if date in tests_df[k.TEST_DATE].values:
                test = tests_df.loc[tests_df[k.TEST_DATE] == date, k.TEST].values[0]
            else:
                test = "?"
            if nt_date in tests_df[k.TEST_DATE].values:
                nt_test = tests_df.loc[tests_df[k.TEST_DATE] == nt_date, k.TEST].values[0]
            else:
                nt_test = "?"
            self.tests[date] = [test, nt_test]

        # Make dataframe for wcq
        wcq_df = (
            df[df[k.WCQ_DATE].isin(self.dates) | df[k.WCQ_DATE].isin(self.dates.values())]
            .iloc[:, k.WCQ_DATE:k.WCQ+1]
        )

        # Put into proper dictionary
        for date, nt_date in self.dates.items():
            if date in wcq_df[k.WCQ_DATE].values:
                wcq = wcq_df.loc[wcq_df[k.WCQ_DATE] == date, k.WCQ].values[0]
            else:
                wcq = ""
            if nt_date in wcq_df[k.WCQ_DATE].values:
                nt_wcq = wcq_df.loc[wcq_df[k.WCQ_DATE] == nt_date, k.WCQ].values[0]
            else:
                nt_wcq = ""

            self.wcq[date] = [wcq, nt_wcq]
