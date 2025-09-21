# This is a sample Python script.

# Press ⌃F5 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

AGE_BRACKETS = ()
WEIGHT_BRACKETS = ()
EXPERIENCE_LEVELS = ('Beginner', 'Intermediate', 'Advanced')
GENDERS = ('M', 'F')
STYLES = ()
FORM_TYPE = ('Open Hand', 'Short Weapon', 'Long Weapon')


def create_reports():
    """
    - find people in each division
    - find people who have not paid
    :return:
    """
    pass


def create_form_events_report():
    pass


def create_sparring_event_report():
    pass


def create_unpaid_dues_report():
    pass


def create_tickets_report():
    pass


def read_csv():
    import csv
    with open('attendees.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
    pass


def sanitize_csv():
    """
    - fixed weights in lbs
    :return:
    """
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_csv()
    create_reports()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
