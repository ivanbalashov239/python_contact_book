#!/bin/python3
import contactbook
from contact import Contact
import unittest
import random, string
import sqlite3


class TestContactClass(unittest.TestCase):
    database="./test.db"
    added = []
    def setUp(self):
        self.connection = sqlite3.connect(self.database)
        self.c = self.connection.cursor()
        try:
            self.c.execute("create table contacts(id integer primary key autoincrement, fname text, lname text, mname text, phone text, bday text)")
            print("new database " + self.database + " was created")
        except sqlite3.Error as e:
            print("Existing database " + self.database)
    def tearDown(self):
        self.connection.commit()
        self.connection.close()

    def test_add(self):
        contact = randomContact()
        self.added.append(contact)
        added, phoneexist, comment = Contact.add(contact,self.c, ())
        self.assertTrue(added)
    def test_del(self):
        self.test_add()
        if self.added:
            contact = self.added[-1]
            result, string=Contact.delete(contact, self.c)
            self.assertTrue(result)

    def test_add_empty(self):
        contact = Contact()
        added, phoneexist, comment = Contact.add(contact, self.c, ())
        self.assertFalse(added)
        self.assertFalse(phoneexist)
    def test_del_empty(self):
        contact = Contact()
        result, string=Contact.delete(contact, self.c)
        self.assertFalse(result)

def randomContact():
        contact = Contact()
        contact.fname=randomString(10)
        contact.mname=randomString(10)
        contact.lname=randomString(10)
        contact.phone=randomString(10)
        contact.bday=str(random.randint(1,29))+"/"+str(random.randint(1,12))+"/"+str(1950+random.randint(0,60))
        return contact

def randomString(integer):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(integer)])


if __name__ == '__main__':
    unittest.main()

