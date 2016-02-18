#!/bin/python3
"""Usage:
    contactbook.py (add|((del|find) [--id=ID])) [--first_name=FNAME][--last_name=LNAME][--middle_name=MNAME][--phone=PHONE][--bday=BDAY][--data=DATA]
    contactbook.py [list [--sort=ITEM [--reverse]]][--data=DATA]

Options:
    add     add contact to the base
    find    find contact in the base
    del     delete contact from the base
        -f FNAME --first_name=FNAME     first name of contact
        -l LNAME --last_name=LNAME      last name of contact
        -m MNAME --middle_name=MNAME    middle name of contact
        -p PHONE --phone=PHONE          phone of contact
        -b BDAY  --bday=BDAY            birthday of contact
        -d DATA  --data=DATA            path to database
        -i ID    --id=ID                id of contact in database
    list    list all contacts in database
        -s --sort=ITEM                  set sort in the list
        -r --reverse                    reverse sort or not

"""
try:
    from docopt import docopt
    import sqlite3
    from schema import Schema, And, Or, Use, SchemaError
    from tabulate import tabulate
    import time
    from contact import Contact
    import sys
except ImportError:
    exit("This app requires docopt, schema, sqlite3, tabulate is installed")


database="./contacts.db"

def set_data(string):
    database=string
def set_reverse(string):
    reverse=string
def set_sort(string):
    reverse=string
def set_sort(string):
    sort=string

if __name__ == '__main__':
    args= docopt(__doc__)
    contact = Contact()
    # contact.set_bday(args["--bday"])
    schema = Schema({
        '--id': Or(None,And(Use(int),Use(contact.set_id, error='id is not correct, it should be integer number'))),
        '--first_name': Or(None,Use(contact.set_fname, error='fname is not correct')),
        '--last_name': Or(None,Use(contact.set_lname, error='lname is not correct')),
        '--middle_name': Or(None,Use(contact.set_mname, error='mname is not correct')),
        '--phone': Or(None,Use(contact.set_phone, error='phone is not correct')),
        '--bday': Or(None,Use(contact.set_bday, error='birtday is not correct it should be one of the formats ' + str(contact.bday_types))),
        '--data': Or(None,Use(set_data, error='name was not correct')),
        '--reverse': Or(None,True,False),
        '--sort': Or(None,"fname","lname","mname","phone","bday", error="--sort should be one of the fname,lname,mname,phone,bday"),
        'add': Or(False,True),
        'del': Or(False, True),
        'find': Or(False,True),
        'list': Or(False,True),
        })
    try:
        schema.validate(args)
    except SchemaError as e:
        exit(e)
    connection = sqlite3.connect(database)
    c = connection.cursor()
    try:
        c.execute("create table contacts(id integer primary key autoincrement, fname text, lname text, mname text, phone text, bday text)")
    except sqlite3.Error as e:
        print("Existing database " + database)

    if args["add"]:
        if contact.add(contact, c):
            print("contact" + str(contact.get_tuple()) + " was added")
        else:
            print("this contact is already exist")
    elif args["find"]:
        print(tabulate(contact.find(contact, c), headers=["first name","last name","middle name","phone","birthday date"]))
    elif args["del"]:
        if contact.delete(contact, c):
            print("contact="+str(contact.get_tuple())+"was deleted")
        else:
            print("there is no contact="+str(contact.get_tuple()))
            sys.exit(100)
    elif args["list"]:
        print(tabulate(contact.lst(args, c), headers=["ID","first name","last name","middle name","phone","birthday date"]))
    else:
        print("reminder")
    connection.commit()
    connection.close()
