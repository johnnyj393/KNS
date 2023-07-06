import k
from admin_functions import *


class Klass():
    def __init__(self, class_data):
        self.name = class_data[k.NAME]
        self.spreadsheet_id = class_data[k.ID]
        self.teacher = ""
        self.time = ""
        self.students = []

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


    def printall(self):
        print(self.name)
        print(self.spreadsheet_id)
        print(self.teacher)
        print(self.time)
        print(self.students)
