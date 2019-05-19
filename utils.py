import os
import csv
import re
from datetime import datetime


# List of utilities:
# clear_screen, csv_empty, row_comp
# update csv, write_csv, read_csv, display_records


class Utils:

    # Clears the terminal to provide a cleaner ui
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Checks if the log csv is empty for the header writer in
    # the method update csv
    def csv_empty(self):
        with open('log.csv', 'r') as csvfile:
            csv_list = []
            for row in csv.reader(csvfile):
                csv_list.append(row)
            if len(csv_list) == 0:
                empty = 'yes'
            else:
                empty = 'no'
        return empty

    # Update the csv with new task entries using the
    # csv dict writer and the task as an object
    def update_csv(self, task):

        with open('log.csv', 'a') as csvfile:
            fieldnames = ['date', 'title', 'time_spent', 'notes']
            taskwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if self.csv_empty() == 'yes':
                taskwriter.writeheader()

            # Writes rows using the dictionary format of {'key': 'value'}
            taskwriter.writerow({
                'date': task.date,
                'title': task.title,
                'time_spent': task.time_spent,
                'notes': task.note
            })

    # overwrites the csv file with the modified data which could
    # be deleted or modified tasks
    def writec_csv(self, data):
        with open('log.csv', 'w') as csvfile:
            fieldnames = ['date', 'title', 'time_spent', 'notes']
            taskwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            taskwriter.writeheader()

            # Writes multiple rows using the dictionary format of {'key': 'value'}
            for record in data:
                taskwriter.writerow({
                    'date': f'{record[0]}',
                    'title': f'{record[1]}',
                    'time_spent': f'{record[2]}',
                    'notes': f'{record[3]}'
                })

    # Compiles the regex pattern to be used more efficiently when
    # called several times in the code
    def row_comp(self):
        row = re.compile('''
        ^(?P<date>\d{2}/\d{2}/\d{4}),
        (?P<title>\w+[\w\s]*),
        (?P<time>\d+\w*),
        (?P<note>[\-'!()&.\s\w]*),
        (?P<id>\d*)\n$
        ''', re.X | re.M)
        return row

    # retrieve the csv line into the class as an object
    def read_csv(self):
        line = self.row_comp()

        # Initiate empty list
        datalist = []

        with open('log.csv') as csvfile:
            logreader = csv.reader(csvfile)
            data = ""

            # Create index used in the update and delete functions
            # of the display_records method
            # - in addition append the data from the csv to the index
            for i, row in enumerate(logreader):
                row.append(f'{i}')
                data += (','.join(row)) + '\n'

            # Using the compiled regex stored in "line"
            for match in line.finditer(data):
                minilist = match.groupdict().values()
                datalist.append(list(minilist))

        # return the correctly matched list with an index
        return datalist

    # Get the date of the task from the user and checks to see if the date is a valid date
    def get_dates(self):
        while True:
            self.clear_screen()
            try:
                date = input('''Date of the task
Please use DD/MM/YYYY: 
> ''')
                result = datetime.strptime(date, '%d/%m/%Y')
                break

                # If the date given doesn't exist throw a value
                # error and print the instructions below
            except ValueError:
                self.clear_screen()
                print("Please enter a correct date with the format suggested")

        # Return the date string in the format dd/mm/yyyy
        return datetime.strftime(result, '%d/%m/%Y')

    # Gets the integer time in minutes of the task
    def get_times(self):

        while True:
            self.clear_screen()
            timesp = input('''How much time in minutes was spent on this task:
> ''')
            try:
                int(timesp)
            # Check if the value is an integer otherwise throw an error
            # loop until an integer is entered
            except ValueError:
                self.clear_screen()
                print("Please enter a valid time in minutes using an integer")
                continue
            break
        return timesp

    # display the records for the user to browse their search results
    def display_records(self, arr, bigArr):
        i = 0
        while True:
            self.clear_screen()
            size = len(arr)
            response = input(f'''
Date: {arr[i][0]}
Title: {arr[i][1]}
Time Spent: {arr[i][2]} minutes
Notes: {arr[i][3]}

Result {i + 1} of {size}

[B]ack, [N]ext, [E]dit, [D]elete, [R]eturn to search menu
''')

            # Function to delete entries
            def delete_arr(index):
                for j in range(len(bigArr)):
                    if arr[i][index] == bigArr[j][index]:
                        del bigArr[j]
                        del arr[i]
                        break

            # Next button logic:
            # Goes forward and at the last entry goes back to the beginning
            if response.lower() == 'n':
                if i < size - 1:
                    i += 1
                else:
                    i = 0

            # Back button logic:
            # Goes backwards and at the first entry goes back to the end
            elif response.lower() == 'b':
                if i > 0:
                    i -= 1
                else:
                    i = size - 1

            # Enables editing of the entry displayed
            # Brings up another editing menu which is in the edit_menu method
            elif response.lower() == 'e':
                self.edit_menu(arr, bigArr, i, size)

            # Delete record in both arrays and write bigArr back to the csv
            elif response.lower() == 'd':
                self.clear_screen()
                delete_arr(4)
                self.writec_csv(bigArr)
                size = len(arr)
                if size == 0:
                    break
                i = 0

            # Return back to the previous menu
            elif response.lower() == 'r':
                self.clear_screen()
                break

    # Edit menu used for editing individual entries
    # As it is large it was taken out of the scope of the e option
    # for better readability
    def edit_menu(self, arr, bigArr, i, size):
        while True:
            self.clear_screen()
            edit = input(f'''
        Date: {arr[i][0]}
        Title: {arr[i][1]}
        TIme Spent: {arr[i][2]} minutes
        Notes: {arr[i][3]}
    
        Result {i + 1} of {size}
    
        To edit please choose from the options below:
        [D]ate, [L]Title, [M]Time, [N]otes, [R]eturn to results menu
        ''')

            # Function enables any changes to the subset array (arr)
            # to be reflected in the large array
            def update_arr(index):
                for j in range(len(bigArr)):
                    if arr[i][index] == bigArr[j][index]:
                        bigArr[j] = arr[i]

            # Edit the date
            if edit.lower() == 'd':
                self.clear_screen()
                dateedit = self.get_dates()
                arr[i][0] = dateedit
                update_arr(4)
                self.writec_csv(bigArr)

            # Edit the title
            elif edit.lower() == 'l':
                while True:
                    self.clear_screen()
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

                arr[i][1] = title
                update_arr(4)
                self.writec_csv(bigArr)

            # Edit the time
            elif edit.lower() == 'm':
                while True:
                    self.clear_screen()
                    timesp = input('''How much time in minutes was spent on this task:
> ''')
                    try:
                        int(timesp)
                    except ValueError:
                        print("Please enter a valid time in minutes using an integer")
                        continue
                    break
                    arr[i][2] = timesp
                    update_arr(4)
                    self.writec_csv(bigArr)

            # Edit the notes
            elif edit.lower() == 'n':
                while True:
                    self.clear_screen()
                    note = input('''Additional notes for this task:
> ''')

                    if ',' in note:
                        Utils().clear_screen()
                        print('Please enter a note without a comma')
                        print('Try dashes instead')
                        continue
                    break
                arr[i][3] = note
                update_arr(4)
                self.writec_csv(bigArr)
            elif edit.lower() == 'r':
                self.clear_screen()
                break
