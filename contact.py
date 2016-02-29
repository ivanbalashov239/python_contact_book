import sqlite3
from datetime import date
from time import strptime

class Contact(object):
    """class of contact with fields id,fname,lname,mname,phone,bday"""
    _cid    = ""
    _fname = ""
    _lname = ""
    _mname = ""
    _phone = ""
    _bday  = ""
    bday_types=["%d/%m/%Y","%d/%m/%y"]
    def __init__(self, *tupl):
        if len(tupl)==5:
            if tupl[0]:
                self.fname(tupl[0])
            if tupl[1]:
                self.mname(tupl[0])
            if tupl[2]:
                self.lname(tupl[0])
            if tupl[3]:
                self.self.phone(tupl[0])
            if tupl[4]:
                self.bday(tupl[0])
        else:
            self.fname = ""
            self.lname = ""
            self.mname = ""
            self.phone = ""
            self.bday  = ""

    @property
    def cid(self):
        return self._cid
    @property
    def fname(self):
        return self._fname
    @property
    def lname(self):
        return self._lname
    @property
    def mname(self):
        return self._mname
    @property
    def phone(self):
        return self._phone
    @property
    def bday(self):
        return self._bday

    @cid.setter
    def cid(self, integer):
        if integer:
            try:
                self._cid=int(integer)
            except Exception as e:
                raise TypeError("Error: cid should be integer")
    @fname.setter
    def fname(self, string):
        if string:
            self._fname=string
    @lname.setter
    def lname(self, string):
        if string:
            self._lname=string
    @mname.setter
    def mname(self, string):
        if string:
            self._mname=string
    @phone.setter
    def phone(self, string):
        if string:
            self._phone=string
    @bday.setter
    def bday(self, string):
        if string:
            self.set_bday(string)

    def set_cid(self, integer):
        self.cid=integer
    def set_fname(self, string):
        self.fname=string
    def set_lname(self, string):
        self.lname=string
    def set_mname(self, string):
        self.mname=string
    def set_phone(self, string):
        self.phone=string
    def set_bday(self, string):
        if string == "":
            return
        for i in " .-_":
            string = string.replace(i,'/')
        types = self.bday_types
        for t in types:
            try:
                struct=strptime(string, t)
                self._bday=str(struct.tm_mday) + "/" + str(struct.tm_mon) + "/" +str(struct.tm_year)
                return
            except ValueError as e:
                ex=e
        # return False
        raise Exception("incorrect date format"+str(ex))
    
    def get_tuple(self):
        return (self.cid, self.fname, self.lname, self.mname, self.phone, self.bday)

    def __str__(self):
        fname = " first name="+self.fname if self.fname else ""
        lname = " last name="+self.lname if self.lname else ""
        mname = " middle name="+self.mname if self.mname else ""
        phone = " phone="+self.phone if self.phone else ""
        bday  = " birthday date="+self.bday if self.bday else ""
        return fname+mname+lname+phone+bday
    
    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return contactIter(self)



    @staticmethod
    def setcontact(contact, c):
        """set contact by id"""
        if contact.cid:
            if contact.fname:
                c.execute("UPDATE `contacts` SET `fname`=? WHERE `_rowid_`=?;",(contact.fname,contact.cid))
            if contact.lname:
                c.execute("UPDATE `contacts` SET `lname`=? WHERE `_rowid_`=?;",(contact.lname,contact.cid))
            if contact.mname:
                c.execute("UPDATE `contacts` SET `mname`=? WHERE `_rowid_`=?;",(contact.mname,contact.cid))
            if contact.phone:
                c.execute("UPDATE `contacts` SET `phone`=? WHERE `_rowid_`=?;",(contact.phone,contact.cid))
            if contact.bday:
                c.execute("UPDATE `contacts` SET `bday`=? WHERE `_rowid_`=?;",(contact.bday,contact.cid))
            return True
        else:
            return False
         
    @staticmethod
    def add(contact, c, args):
        """add contact method"""
        if args:
            replace=args["--replace"]
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
        if string:
            finded = contact.find(contact, c)
            if not finded:
                if contact.phone:
                    cnt = Contact()
                    cnt.phone = contact.phone
                    phone_finded=contact.find(cnt, c)
                    if phone_finded:
                        if replace:
                            phone_contact=phone_finded[0]
                            contact.cid=phone_contact[0]
                            contact.setcontact(contact, c)
                            return True, True, "Contact with this phone="+contact.phone+" replaced"
                        else:
                            return False, True, "Contact with this phone="+contact.phone+" already exist"

                c.execute('insert into contacts('+string+') VALUES ('+msk+')', tuple(tup))
                return True, False, "Contact was added"
            else:
                return False, True, "This contact already exist"
        else:
            return False, False, "there is empty contact"

    @staticmethod
    def find( contact, c):
        """find contact method"""
        string1 = "select id, fname, lname, mname, phone, bday from contacts "
        string = ""
        if contact.cid:
            string+=" id='" + str(contact.cid) + "' and "
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

    @staticmethod
    def lst( args, c):
        """list all contacts method"""
        if args and args["--sort"]:
            ex='select id, fname, lname, mname, phone, bday from contacts order by ' + args["--sort"]
        else:
            ex='select id, fname, lname, mname, phone, bday from contacts '
        if args and args["--reverse"]:
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

    @staticmethod
    def delete(contact, c):
        """delete contacts"""
        string1 = "select id, fname, lname, mname, phone, bday from contacts where"
        string = ""
        if contact.cid:
            string+=" id='" + str(contact.cid) + "' and "
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
            return False, "empty contact can't be deleted"
        try:
            lst=c.execute(string1 + string).fetchall()
            if lst:
                c.execute("delete from contacts where" + string)
                return lst, "contact(s) deleted"
            else:
                return False, "there is no contact"
        except sqlite3.Error as e:
            return False, "there is no contact=" + contact + "in the database"

    @staticmethod
    def reminder(c):
        """remind about birthdays in this or next month"""
        today = date.today()
        today = str(today.day)+"/"+str(today.month)+"/"+str(today.year)
        contacts=[]
        for row in c.execute("select id, fname, lname, mname, phone, bday from contacts"):
            contact=Contact()
            contact.cid=row[0]
            contact.fname=row[1]
            contact.lname=row[2]
            contact.mname=row[3]
            contact.phone=row[4]
            contact.bday=row[5]
            if contact.bday and contact.monthdelta(today,contact.bday):
                contacts.append(contact)
        return contacts

    @staticmethod
    def monthdelta(date1,date2):
        """let birthdays delta"""
        day1, month1, year1 = date1.split("/")
        day2, month2, year2 = date2.split("/")
        mdelta=int(month2) - int(month1)
        ddelta=int(day2) - int(day1)
        if mdelta == 0 and ddelta >= 0:
            return True
        elif 0 < mdelta < 2:
            return True

        return False

class contactIter(object):
    """Contact Iterator"""
    def __init__(self, contact):
        self.lst = contact.get_tuple()
        self.i = -1
    def __iter__(self):
        return self
    def __next__(self):
        if self.i<len(self.lst)-1:
            self.i += 1         
            return self.lst[self.i]
        else:
            raise StopIteration
