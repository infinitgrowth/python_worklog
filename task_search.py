import re
from utils import Utils
from datetime import datetime
import pdb


class Search(Utils):
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
            # Note:
            #
            # When finding by date, I should be presented with a list of dates with entries
            # and be able to choose one to see entries from.

            # When finding by time spent, I should be allowed to enter the number of minutes
            # a task took and be able to choose one to see entries from.

            # When finding by an exact string, I should be allowed to enter a string and
            # then be presented with entries containing that string in the task name or notes.

            # When finding by a pattern, I should be allowed to enter a regular expression
            # and then be presented with entries matching that pattern in their task name or notes.

            # todo write all the user_choices with the corresponding functions
            # todo complete the compile in the csv read test file
            if user_choice.lower() == 'a':
                self.clear_screen()
                data = self.read_csv()
                datam = []

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
''')

                sdate = dictr.get(sdateind)
                for record in data:
                    if record[0] == sdate:
                        print(record[0])
                        datam.append(record)

                err_msg = self.check_disp(datam, data)

            elif user_choice.lower() == 'b':
                self.clear_screen()
                print("You'll be asked for two dates consecutively ")

                while True:
                    r1fdate = self.get_dates()
                    r2fdate = self.get_dates()

                    r1pdate = datetime.strptime(r1fdate, '%d/%m/%Y')
                    r2pdate = datetime.strptime(r2fdate, '%d/%m/%Y')

                    if r1pdate > r2pdate:
                        r2date = r1pdate
                        r1date = r2pdate
                        break
                    elif r1pdate < r2pdate:
                        r1date = r1pdate
                        r2date = r2pdate
                        break
                    else:
                        print("Please select a range and not the same date")
                        continue

                data = self.read_csv()
                datam = []

                pdb.set_trace()
                for record in data:
                    rec_date = datetime.strptime(record[0], '%d/%m/%Y')
                    if r1date <= rec_date and rec_date <= r2date:
                        datam.append(record)
                print(datam)

                err_msg = self.check_disp(datam, data)
            elif user_choice.lower() == 'c':
                self.clear_screen()
                data = self.read_csv()
                datam = []

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
''')

                stime = dictr.get(stimeind)

                for record in data:
                    if record[2] == stime:
                        datam.append(record)
                print(datam)

                err_msg = self.check_disp(datam, data)

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
                # print(data)
                datam = []

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

                data = self.read_csv()
                datam = []

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
