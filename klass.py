from admin_functions import *
import pandas as pd


class Klass:
    def __init__(self, class_data):
        # Admin data from k
        self.name = class_data[k.NAME]
        self.spreadsheet_id = class_data[k.ID]
        # Admin data from google
        self.teacher = ""
        self.time = ""
        self.students = []
        # Data
        self.dates = []
        self.books = {}
        self.nt_books = {}

    # Initializes admin data from Google - teacher, schedule (time), and current students
    def set_up(self, client):
        values = fetch_data(client, self.spreadsheet_id, k.INFO_SHEET)
        for value in values:
            if value[0] == 'Teacher':
                self.teacher = value[1]
            elif value[0] == 'Time':
                self.time = value[1]
            elif value[0] == 'Students':
                for student in value[1:len(value)]:
                    self.students.append(student)

    # -----------------------------------------------------------------
    # Writing to canvas functions

    def write_info(self, date, c):
        # Set font for titles - bold, 14
        c.setFont(k.FONT_BOLD, k.SIZE_14)

        # Teacher
        c.drawString(k.TEACHER_X, k.TEACHER_Y, self.teacher)
        # Name
        c.drawString(k.NAME_X, k.NAME_Y, self.name)
        # Date
        c.drawString(k.DATE_X, k.DATE_Y, date)

        # Reset to normal - no bold, 12
        c.setFont(k.FONT, k.SIZE_12)

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

        return c

    def write_books(self, date, c):

        # Set up
        y = k.BOOKS_TOP_START

        # Write to canvas
        for key, value in self.books[date].items():
            c.drawString(k.BOOKS_LEFT_X, y, key)
            c.drawString(k.BOOKS_RIGHT_X, y, value)
            y -= k.BOOKS_GO_DOWN

        # Make nt_books string
        nt_books_string = self.nt_books[date][0]
        for value in self.nt_books[date][1:]:
            nt_books_string += f", {value}"

        # Write to canvas
        c.drawString(k.NT_BOOKS_X, k.NT_BOOKS_Y, nt_books_string)

        return c

    # Looped curriculum writer for each date in dates
    def write_curriculum(self, pdf):

        for date in self.dates:
            c, stream = start_edit()
            c = self.write_info(date, c)
            c = self.write_books(date, c)
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

        # Make dataframe
        df = pd.DataFrame(filtered_data, columns=column_headers)

        # Make sure there are no None or NaN values
        df.fillna("", inplace=True)

        # Store data appropriately
        for index, row in df.iterrows():

            # Convert index to int instead of hashable
            # noinspection PyTypeChecker
            index = int(index)

            # Set up dict for daily books
            date = row[0]
            daily_books = {}

            # Set up dict for next times books
            if index > 0:
                nt_date = df.iloc[index - 1, 0]
                nt_books = []
            else:
                nt_date = ""
                nt_books = []

            # Go through books for each day
            for column, value in row.iloc[1:].items():

                # Put book from that day into book array if entry is not blank
                if value != "":
                    daily_books[column] = value
                    if index > 0:
                        nt_books.append(column)

            # Put new value sets into appropriate place
            if index < len(df) - 1:
                self.dates.append(date)
                self.books[date] = daily_books
            if index > 0:
                self.nt_books[nt_date] = nt_books
