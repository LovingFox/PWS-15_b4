import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
   __tablename__ = 'user'
   id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
   first_name = sa.Column(sa.Text)
   last_name = sa.Column(sa.Text)
   gender = sa.Column(sa.Text)
   email = sa.Column(sa.Text)
   birthdate = sa.Column(sa.DATE)
   height = sa.Column(sa.FLOAT)

   def __str__(self):
      return "{id:4} {n:25} {g:7} {b:11} {h:.2f}  {e}".format(
         id=self.id, n=self.first_name+" "+self.last_name,
         g=self.gender, b=str(self.birthdate), e=self.email,
         h=self.height if self.height else 0,)

class MyDataBase():
   def __init__(self, dbp=DB_PATH):
      engine = sa.create_engine(dbp)
      self.sess = sessionmaker(engine)()

   def __enter__(self):
      return self

   def __exit__(self, *argv, **kwargv):
      self.sess.close()

def request_userdata(user=None):
    print("Enter user data...")
    first_name = last_name = gender = email = birthdate = height = None
    while not first_name: first_name = input("First name: ")
    while not last_name: last_name = input("Last name: ")

    while not gender:
       gender = input("Gender (m or f): ").lower()
       if len(gender) > 1 or gender not in 'fm':
          print("incorrect")
          gender = None
       else:
          gender="Male" if gender=="m" else "Female"

    while not email:
       email = input("E-mail: ")
       eml = email.split('@')
       if len(eml) != 2 or eml[1].find('.') < 0:
          print("incorrect")
          email = None

    while not birthdate:
       birthdate = input("Birth date (YYYY-MM-DD): ")
       try:
          birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d')
       except ValueError:
          print("incorrect")
          birthdate = None

    while not height:
       height = input("Heidht (m.cm): ")
       try:
          height = float(height)
       except ValueError:
          print("incorrect")
          height = None

    if not user:
       user = User()

    user.first_name=first_name
    user.last_name=last_name
    user.gender=gender
    user.email=email
    user.birthdate=birthdate
    user.height=height

    return user

def request_userid():
    uid = None
    while not uid:
       uid = input("Enter user id: ")
       try:
          uid = int(uid)
       except ValueError:
          print("incorrect")
          uid = None
    return uid

if __name__ == "__main__":
   command = input(
         "1 - Add user\n" +
         "2 - Modify user\n" +
         "3 - Delete user\n" +
         "* - List all users\n")
   try:
      command = int(command)
   except ValueError:
      command = None

   if command == 1:
      user = request_userdata()
      with MyDataBase() as db:
         db.sess.add(user)
         db.sess.commit()
         print("User added")
   elif command == 2:
      user_id = request_userid()
      with MyDataBase() as db:
         user = db.sess.query(User).filter(User.id == user_id).first()
         if user:
            user = request_userdata(user)
            confirm = input("Change? (y/n):")
            if confirm.lower() == "y":
               db.sess.add(user)
               db.sess.commit()
               print("User changed")
         else:
            print("User id {} not found".format(user_id))
   elif command == 3:
      user_id = request_userid()
      with MyDataBase() as db:
         user = db.sess.query(User).filter(User.id == user_id).first()
         if user:
            confirm = input("Delete? (y/n):")
            if confirm.lower() == "y":
               db.sess.delete(user)
               db.sess.commit()
               print("User deleted")
         else:
            print("User id {} not found".format(user_id))
   else:
      with MyDataBase() as db:
         print("All users:")
         users = db.sess.query(User).all()
         list( map(print, users) )
