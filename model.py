from app.__init__ import db
from werkzeug.security import generate_password_hash, \
     check_password_hash
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, mapper, query

def loadSession():
    """"""
    dbPath = 'app.db'
    engine = create_engine('sqlite:///%s' % dbPath, echo=True)
    metadata = MetaData(engine)
    moz_bookmarks = Table('user', metadata, autoload=True)
    mapper(User, moz_bookmarks, non_primary=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
def isHere(user):
    session=loadSession()
    return session.query(User).filter_by(username=user).first()
class User(db.Model):
    '''Table for storing registered users'''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def check_normall_password(self, password):
        return self.password==password

    def return_password(self):
        return self.password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)




class GLTraits(db.Model):
    '''Local storage for personality-related traits obtained from
    Genomelink API'''
    id = db.Column(db.Integer, primary_key=True)


class Questions(db.Model):
    '''Table for storing questions related to personality traits'''
    id = db.Column(db.Integer, primary_key=True)


class Answers(db.Model):
    '''Table for storing user's answers to the questions.
    Includes self-assessment and replies from other users.'''
    id = db.Column(db.Integer, primary_key=True)
