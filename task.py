from datetime import datetime
from utils import Utils


# the Task object that the class returns
class Task:
    Utils().clear_screen()

    def __init__(self):
        self.date = self.get_date()
        self.title = self.get_title()
        self.time_spent = self.get_time_spent()
        self.note = self.get_note()

    def get_date(self):
        # Get the date of the task from the user and checks to see if the date is a valid date

        while True:
            try:
                date = input('''Date of the task
            Please use DD/MM/YYYY: 
> ''')
                result = datetime.strptime(date, '%d/%m/%Y')
                break
            except ValueError:
                Utils().clear_screen()
                print("Please enter a correct date with the format suggested")

        return datetime.strftime(result, '%d/%m/%Y')

    # gets the title of the task which be anything greater than 1
    def get_title(self):

        while True:
            title = input('''Title of the task:
> ''')
            if len(title) == 0:
                Utils().clear_screen()
                print('Please enter a title that represents your task')
                continue

            if ',' in title:
                Utils().clear_screen()
                print('Please enter a title without a comma')
                continue
            break

        return title

    # Gets the integer time in minutes of the task
    def get_time_spent(self):

        while True:
            timesp = input('''How much time in minutes was spent on this task:
> ''')
            try:
                int(timesp)
            except ValueError:
                print("Please enter a valid time in minutes using an integer")
                continue
            break
        return timesp

    # Optional notes pertinent to the task so the user can enter nothing or anything
    def get_note(self):

        while True:
            note = input('''Additional notes for this task:
> ''')

            if ',' in note:
                Utils().clear_screen()
                print('Please enter a note without a comma')
                print('Try dashes instead')
                continue
            break
        input("Your entry has been added press return to go back to the main menu")
        return note
