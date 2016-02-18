import sqlite3
import time

class Contact(object):
    id    = ""
    fname = ""
    lname = ""
    mname = ""
    phone = ""
    bday  = ""
    bday_types=["%d/%m/%Y","%d/%m/%y"]
    def __init__(self, *tupl):
        if len(tupl)==5:
            if tupl[0]:
                self.set_fname(tupl[0])
            if tupl[1]:
                self.set_mname(tupl[0])
            if tupl[2]:
                self.set_lname(tupl[0])
            if tupl[3]:
                self.set_phone(tupl[0])
            if tupl[4]:
                self.set_bday(tupl[0])
        else:
            self.fname = ""
            self.lname = ""
            self.mname = ""
            self.phone = ""
            self.bday  = ""

    def set_id(self, integer):
        self.id=integer
    def set_fname(self, string):
        self.fname=string
    def set_lname(self, string):
        self.lname=string
    def set_mname(self, string):
        self.mname=string
    def set_phone(self, string):
        self.phone=string
    def set_bday(self, string):
        for i in " .-_":
            string = string.replace(i,'/')
        types = self.bday_types
        for t in types:
            try:
                struct=time.strptime(string, t)
                self.bday=str(struct.tm_mday) + "/" + str(struct.tm_mon) + "/" +str(struct.tm_year)
                return
            except ValueError:
                t=""
        raise 
    
    def get_tuple(self):
        return (self.id, self.fname, self.lname, self.mname, self.phone, self.bday)

    def __str__(self):
        fname = " first name="+self.fname if self.fname else ""
        lname = " last name="+self.lname if self.lname else ""
        mname = " middle name="+self.mname if self.mname else ""
        phone = " phone="+self.phone if self.phone else ""
        bday  = " birthday date="+self.bday if self.bday else ""
        return fname+mname+lname+phone+bday
    
    def __repr__(self):
        return self.__str__()

    def add(self, contact, c):
        string = ""
        msk = ""
        tup = []
        if contact.fname:
            tup.append(contact.fname)
            string += "fname,"
            msk += "?,"
        if contact.lname:
            tup.append(contact.lname)
            string += "lname,"
            msk += "?,"
        if contact.mname:
            tup.append(contact.mname)
            string += "mname,"
            msk += "?,"
        if contact.phone:
            tup.append(contact.phone)
            string += "phone,"
            msk += "?,"
        if contact.bday:
            tup.append(contact.bday)
            string += "bday,"
            msk += "?,"
        string = string[:-1]
        msk = msk[:-1]
        finded = self.find(contact, c)
        if not finded:
            cnt = Contact()
            cnt.phone = contact.phone
            if len(self.find(cnt, c)) !=0:
                print("this phone number is already in the database")
            c.execute('insert into contacts('+string+') VALUES ('+msk+')', tuple(tup))
            return True
        else:
            return False

    def find(self, contact, c):
        string1 = "select id, fname, lname, mname, phone, bday from contacts "
        string = ""
        if contact.id:
            string+=" id='" + str(contact.id) + "' and "
        if contact.fname:
            string+=" fname='" + contact.fname + "' and "
        if contact.lname:
            string+=" lname='" + contact.lname + "' and "
        if contact.mname:
            string+=" mname='" + contact.mname + "' and "
        if contact.phone:
            string+=" phone='" + contact.phone + "' and "
        if contact.bday:
            string+=" bday='" + contact.bday + "' and "

        string = string[:-4]
        if string != "":
            string = string1 + " where " + string
        else:
            string = string1
        # print(string)
        rows = []
        for row in c.execute(string):
                cont=eval(str(row))
                rows.append(cont)
        return tuple(rows)
    def lst(self, args, c):
        if args["--sort"]:
            ex='select id, fname, lname, mname, phone, bday from contacts order by ' + args["--sort"]
        else:
            ex='select id, fname, lname, mname, phone, bday from contacts '
        if args["--reverse"]:
            ex+=" desc"

        try:
            result = []
            for row in c.execute(ex):
                cont=eval(str(row))
                result.append(cont)
            return tuple(result)

        except sqlite3.Error as e:
            print("there is no column:" + args["--sort"])
            raise
    def delete(self, contact, c):
        string1 = "select id, fname, lname, mname, phone, bday from contacts where"
        string = ""
        if contact.id:
            string+=" id='" + str(contact.id) + "' and "
        if contact.fname:
            string+=" fname='" + contact.fname + "' and "
        if contact.lname:
            string+=" lname='" + contact.lname + "' and "
        if contact.mname:
            string+=" mname='" + contact.mname + "' and "
        if contact.phone:
            string+=" phone='" + contact.phone + "' and "
        if contact.bday:
            string+=" bday='" + contact.bday + "' and "

        string = string[:-4]
        if string == "":
            return False
        try:
            lst=c.execute(string1 + string).fetchall()
            if lst:
                c.execute("delete from contacts where" + string)
                return lst
            else:
                return False
        except sqlite3.Error as e:
            print("there is no contact=" + "in the database")
            raise
