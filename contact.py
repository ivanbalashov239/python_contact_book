import sqlite3
import time

"""class of contact with fields id,fname,lname,mname,phone,bday"""
class Contact(object):
    _id    = ""
    _fname = ""
    _lname = ""
    _mname = ""
    _phone = ""
    _bday  = ""
    bday_types=["%d/%m/%Y","%d/%m/%y"]
    def __init__(self, *tupl):
        if len(tupl)==5:
            if tupl[0]:
                fname(tupl[0])
            if tupl[1]:
                mname(tupl[0])
            if tupl[2]:
                lname(tupl[0])
            if tupl[3]:
                self.phone(tupl[0])
            if tupl[4]:
                bday(tupl[0])
        else:
            self.fname = ""
            self.lname = ""
            self.mname = ""
            self.phone = ""
            self.bday  = ""

    @property
    def id(self):
        return self._id
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

    @id.setter
    def id(self, integer):
        self._id=integer
    @fname.setter
    def fname(self, string):
        self._fname=string
    @lname.setter
    def lname(self, string):
        self._lname=string
    @mname.setter
    def mname(self, string):
        self._mname=string
    @phone.setter
    def phone(self, string):
        self._phone=string
    @bday.setter
    def bday(self, string):
        self.set_bday(string)

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
        if string == "":
            return
        for i in " .-_":
            string = string.replace(i,'/')
        types = self.bday_types
        for t in types:
            try:
                struct=time.strptime(string, t)
                self._bday=str(struct.tm_mday) + "/" + str(struct.tm_mon) + "/" +str(struct.tm_year)
                return
            except ValueError:
                t=""
        raise Exception("incorrect date format")
    
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


    @staticmethod
    def setcontact(contact, c):
        if contact.id:
            if contact.fname:
                c.execute("UPDATE `contacts` SET `fname`=? WHERE `_rowid_`=?;",(contact.fname,contact.id))
            if contact.lname:
                c.execute("UPDATE `contacts` SET `lname`=? WHERE `_rowid_`=?;",(contact.lname,contact.id))
            if contact.mname:
                c.execute("UPDATE `contacts` SET `mname`=? WHERE `_rowid_`=?;",(contact.mname,contact.id))
            if contact.phone:
                c.execute("UPDATE `contacts` SET `phone`=? WHERE `_rowid_`=?;",(contact.phone,contact.id))
            if contact.bday:
                c.execute("UPDATE `contacts` SET `bday`=? WHERE `_rowid_`=?;",(contact.bday,contact.id))
            return True
        else:
            return False
         
    @staticmethod
    def add(contact, c, *args):
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
        finded = contact.find(contact, c)
        if not finded:
            cnt = Contact()
            cnt.phone = contact.phone
            phone_finded=contact.find(cnt, c)
            if phone_finded:
                phone_contact=phone_finded[0]
                print("This phone number is already in the database")
                print("Do you realy want to add this contact to the database?")
                answer=input("(y(yes)/n(no)/r(replace))").lower()
                yes=["y","yes"]
                replace=["r","replace"]
                if answer in yes:
                    print("Ok, adding this contact to the database")
                elif answer in replace:
                    contact.id=phone_contact[0]
                    contact.setcontact(contact, c)
                    return True
                else:
                    return False

            c.execute('insert into contacts('+string+') VALUES ('+msk+')', tuple(tup))
            return True
        else:
            return False

    @staticmethod
    def find( contact, c):
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

    @staticmethod
    def lst( args, c):
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

    @staticmethod
    def delete(contact, c):
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

    @staticmethod
    def reminder(c):
        contacts=[]
        i=0
        for row in c.execute("select id, fname, lname, mname, phone, bday from contacts"):
            contacts[i]=Contact()
            contacts[i].id=row[0]
            contacts[i].fname=row[1]
            contacts[i].lname=row[2]
            contacts[i].mname=row[3]
            contacts[i].phone=row[4]
            contacts[i].bday=row[5]
                
