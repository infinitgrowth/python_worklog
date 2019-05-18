import re
from utils import Utils
from datetime import datetime
import pdb


# Search class
class Search(Utils):
    # Error display if there no values returned from the search attempt
    def check_disp(self, datam, data):
        if len(datam) == 0:
            self.clear_screen()
            print("""Your search did not yield any results please try again.               
""")
            err_msg = 1
        else:
            # Display UI and handle csv update
            self.display_records(datam, data)
            err_msg = 0

        return err_msg

    # Search menu
    def search_menu(self):
        err_msg = 0
        while True:
            if err_msg == 0:
                self.clear_screen()
            err_msg = 0
            user_choice = input('''Do you want to search by:
a) Exact Date
b) Range of Dates
c) Time Spent
d) Exact Search
e) Regex Pattern
r) Return to menu
> ''')

            # Find the exact date
            if user_choice.lower() == 'a':
                self.clear_screen()
                data = self.read_csv()  # get the rows from the work log and place it into the array data
                datam = []  # Initialize an empty array for the search entries

                # initialize an empty dictionary and index
                # Goal is to ensure there are no duplicates while giving an accurate index
                # If it's not a duplicate add the index and the value to the dictionary and increment the index
                indr = 1
                dictr = {}
                for record in data:
                    if record[0] in dictr.values():
                        continue
                    else:
                        dictr[f"{indr}"] = record[0]
                        print(f'{indr}. {record[0]}')
                        indr += 1

                sdateind = input('''
Select a date from the list using the index. ie: 1 for 
the first date in the list.                 
>  ''')
                # Using the date append it to datam which is the subset of the search
                sdate = dictr.get(sdateind)
                for record in data:
                    if record[0] == sdate:
                        print(record[0])
                        datam.append(record)

                # check for errors before displaying
                err_msg = self.check_disp(datam, data)

            # Search date range
            elif user_choice.lower() == 'b':
                self.clear_screen()
                print("You'll be asked for two dates consecutively ")

                while True:
                    # Get both dates
                    r1fdate = self.get_dates()
                    r2fdate = self.get_dates()

                    # Change the string into a datetime object
                    r1pdate = datetime.strptime(r1fdate, '%d/%m/%Y')
                    r2pdate = datetime.strptime(r2fdate, '%d/%m/%Y')

                    # Ensure the lowest date is the lowest and the highest is the highest
                    if r1pdate > r2pdate:
                        r2date = r1pdate
                        r1date = r2pdate
                        break
                    elif r1pdate < r2pdate:
                        r1date = r1pdate
                        r2date = r2pdate
                        break
                    else:
                        # If the dates are the same ask the user to start over
                        print("Please select a range and not the same date")
                        continue

                data = self.read_csv()  # get the rows from the work log and place it into the array data
                datam = []  # Initialize an empty array for the search entries

                # Find the dates in between
                for record in data:
                    rec_date = datetime.strptime(record[0], '%d/%m/%Y')
                    if r1date <= rec_date and rec_date <= r2date:
                        datam.append(record)
                print(datam)

                err_msg = self.check_disp(datam, data)

            # Search by time spent
            elif user_choice.lower() == 'c':
                self.clear_screen()
                data = self.read_csv()  # get the rows from the work log and place it into the array data
                datam = []  # Initialize an empty array for the search entries

                # initialize an empty dictionary and index
                # Goal is to ensure there are no duplicates while giving an accurate index
                # If it's not a duplicate add the index and the value to the dictionary and increment the index
                indr = 1
                dictr = {}
                for record in data:
                    if record[2] in dictr.values():
                        continue
                    else:
                        dictr[f"{indr}"] = record[2]
                        print(f'{indr}. {record[2]} minute(s)')
                        indr += 1

                stimeind = input('''
Select a time from the list using the index. ie: 1 for 
the first time in the list.                 
>  ''')
                # Get the value from the index provided by the user
                stime = dictr.get(stimeind)

                # Append search values to the subset array
                for record in data:
                    if record[2] == stime:
                        datam.append(record)
                print(datam)

                # Check for errors
                err_msg = self.check_disp(datam, data)

            # Search for the notes
            elif user_choice.lower() == 'd':
                self.clear_screen()

                def get_search():
                    # Get user search values for the title and notes
                    search = input('''
Enter the exact value to search in either the title 
or the notes section:
> ''')
                    return search

                xsearch = get_search()

                data = self.read_csv()
                datam = []

                # Search both the notes and the title
                for record in data:

                    searchm1 = re.findall(xsearch, record[1])
                    searchm2 = re.findall(xsearch, record[3])
                    if len(searchm1) > 0:
                        datam.append(record)
                    elif len(searchm2) > 0:
                        datam.append(record)

                if len(datam) == 0:
                    self.clear_screen()
                    print("Your search did not yield any results please try again.")
                    err_msg = 1
                    continue

                err_msg = self.check_disp(datam, data)

            elif user_choice.lower() == 'e':
                self.clear_screen()

                def get_searchr():
                    # Get user search values for the title and notes
                    search = input('''
Enter the regex value to search in either the title 
or the notes section:
Ex: regex value of (?<=abc)def (no quotes) searching data 'abcdef' will find 'def' 
> ''')
                    search = r"""{}""".format(search)
                    return search

                searchr = get_searchr()

                data = self.read_csv()  # get the rows from the work log and place it into the array data
                datam = []  # Initialize an empty array for the search entries

                # Search both the notes and the title
                for record in data:

                    searchm1 = re.findall(searchr, record[1])
                    searchm2 = re.findall(searchr, record[3])
                    if len(searchm1) > 0:
                        datam.append(record)
                    elif len(searchm2) > 0:
                        datam.append(record)

                err_msg = self.check_disp(datam, data)

            elif user_choice.lower() == 'r':
                self.clear_screen()
                print("Returning to the main menu!")
                break
            else:
                continue
        return user_choice
