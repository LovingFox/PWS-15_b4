from users import sa, Base, User, MyDataBase, request_userid
from sqlalchemy.sql import func

class Athlete(Base):
   """
   Athlete class
   Can be printed
   """
   __tablename__ = 'athelete'
   id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
   name = sa.Column(sa.Text)
   birthdate = sa.Column(sa.DATE)
   height = sa.Column(sa.FLOAT)
   gender = sa.Column(sa.Text)
   sport = sa.Column(sa.Text)
   country = sa.Column(sa.Text)

   def __str__(self):
      return "{i:4} {n:25} {g:7} {b:11} {h:.2f}  {c:15} {s}".format(
              i=self.id, n=self.name, g=self.gender,
              b=str(self.birthdate), s=self.sport, c=self.country,
              h=self.height if self.height else 0,)

def athlets_by_birthdate(sess, birthdate):
   """
   Return all athlets as Athlet class close by 'birthdate'
   """
   athlet_birthdate = \
      sess.query(Athlete.birthdate)\
      .order_by(
         func.abs(
            func.strftime('%s', Athlete.birthdate)
            - func.strftime('%s', birthdate) ) )\
      .limit(1).first()

   if athlet_birthdate:
      return sess.query(Athlete)\
             .filter(
                Athlete.birthdate.in_(athlet_birthdate) )\
             .all()
   else:
      return None

def athlets_by_height(sess, height):
   """
   Return all athlets as Athlet class close by 'heigth'
   """
   athlete_height = \
      sess.query(Athlete.height)\
         .filter(Athlete.height.isnot(None)).order_by(
            func.abs( Athlete.height - height ) )\
      .limit(1).first()

   if athlete_height:
      return sess.query(Athlete)\
             .filter(
                Athlete.height.in_(athlete_height) )\
             .all()
   else:
      return None

if __name__ == "__main__":
   user_id = request_userid()
   with MyDataBase() as db:
      user = db.sess.query(User).filter(User.id==user_id).first()
      if user:
         print(user, "\n")
         print("Athletes close to user")

         # Print all found by:
         #  - birth date
         #  - height
         for title, athlets_by, value in zip(
               ('by birth date', 'by heigth'),
               (athlets_by_birthdate, athlets_by_height),
               (user.birthdate, user.height)
         ):
            athletes = athlets_by(db.sess, value)
            if athletes:
               print("{t} ({l}):".format(t=title, l=len(athletes)))
               list( map(print, athletes) )
            else:
               print("- athlets close {} not found".format(title))
      else:
         print("User id {} not found".format(user_id))
