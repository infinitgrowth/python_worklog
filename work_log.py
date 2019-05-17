# The Work Log application enables work to be logged to a csv file
# It also allows for the user to search and edit the work log
import csv

from task_search import Search
from utils import Utils
from task import Task


def main_menu():
    Utils().clear_screen()  # This function clears the terminal at the beginning of the application

    # The initial menu the user will see with option on how to proceed
    user_choice = input("""
WORK LOG
What would you like to do?
a) Add new entry
b) Search in existing entries
c) Quit program
> """)

    if user_choice == "a":
        task = Task()  # Call the task object and collect the task info
        # empty = Utils().empty()
        Utils().update_csv(task)  # Updates the csv with the new object
        Utils().clear_screen()  # Clear the screen
        main_menu()  # Show the user the main menu again
    elif user_choice == "b":
        Utils().clear_screen()  # Clear the screen
        with open('log.csv', 'r') as csvfile:
            csv_dict = [row for row in csv.DictReader(csvfile)]
            if len(csv_dict) == 0:
                print('The work log is empty, please add entries to the log before searching.')
                input('Press enter to continue: >')
            else:
                Search().search_menu()  # Go to the search menu
        main_menu()  # Show the user the main menu again
    elif user_choice == "c":
        # Clear the screen and print a goodbye message to the user
        Utils().clear_screen()
        print('Thank you for using the work log application. Please do come again.')
    else:
        Utils().clear_screen()
        print("Your entry is invalid, please select a, b or c from the menu provided")
        main_menu()

    return user_choice


# Ensure program isn't run on import
if __name__ == "__main__":
    # Call the work log function to start the program
    main_menu()
