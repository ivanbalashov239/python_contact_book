#!/bin/python3
"""Usage:
    contactbook.py (find|add|del) [--first_name=FNAME][--last_name=LNAME][--middle_name=MNAME][--phone=PHONE][--birthday=BDAY][--data=DATA]
    contactbook.py [(list [--sort=ITEM])][--data=DATA]

Options:
    add     add contact to the base
    find    find contact in the base
    del     delete contact from the base
        -f FNAME --first_name=FNAME     first name of contact
        -l LNAME --last_name=LNAME      last name of contact
        -m MNAME --middle_name=MNAME    middle name of contact
        -p PHONE --phone=PHONE          phone of contact
        -b BDAY  --birthday=BDAY        birthday of contact
        -d DATA  --data=DATA            path to database
    list    list all contacts in database
        -s --sort=ITEM                  set sort in the list

"""
from docopt import docopt
import sqlite3
database="./contacts.db"

def add(args, c):
    c.executemany('insert into contacts(fname, lname, mname, phone, birthday) VALUES (?,?,?,?,?)', [args])
def lst(args, c):
    if args:
        for row in c.execute('select fname, lname, mname, phone, birthday from contacts order by ' + args + 'callate reverse'):
            print(row)
    else:
        for row in c.execute('select fname, lname, mname, phone, birthday from contacts'):
            print(row)


if __name__ == '__main__':
    args= docopt(__doc__)
    print(args)
    contact = (args["--first_name"] or "",args["--last_name"] or "",args["--middle_name"] or "",args["--phone"] or "",args["--birthday"] or "")
    print(contact)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    try:
        c.execute("create table contacts(fname text, lname text, mname text, phone text, birthday text)")
    except sqlite3.Error as e:
        print("Existing database")

    if args["add"]:
        add(contact, c)
    elif args["find"]:
        find(contact, c)
    elif args["del"]:
        delete(contact, c)
    elif args["list"]:
        lst(args["--sort"], c)
    connection.commit()
    connection.close()
