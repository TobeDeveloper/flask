from . import db, login_manager
import hashlib, logging
from flask import request
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from config import LOGGING_FORMAT

logging.basicConfig(level=logging.DEBUG,
    format=LOGGING_FORMAT,
    datefmt='%d %b %Y %H:%M:%S',
    filename='app_log.log',
    filemode='w'
)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    last_login = db.Column(db.DateTime(), default=func.now())

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_login(self):
        self.last_login = func.now()
        db.session.add(self)
    
    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('UTF-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)

    def add(user):
        db.session.add(user)
        db.session.commit()
        logging.debug('user information has been saved.')

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    taskname = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    status = db.Column(db.Integer, default = 1)
    progress = db.Column(db.Float)
    due_date = db.Column(db.DateTime())
    create_at = db.Column(db.DateTime(), default = func.now())
    describtion = db.Column(db.String)
    task_type = db.column(db.String)

    def get_tasks(id):
        logging.debug('load current user tasks: %d',id)
        return Task.query.filter(Task.user_id == id)
    
    def get_task_byid(id):
        logging.debug('load task by id: %d',id)
        return Task.query.get(id)

    def statistics(tasks):
        result = {}
        # for t in tasks:
        #     result['type'] = 
        return result

    def add(task):
        db.session.add(task)
        db.session.commit()

class Alembic(db.Model):
    __tablename__ = 'alembic_version'
    version_num = db.Column(db.String(32), primary_key = True,nullable=False)

    @staticmethod
    def clear_version():
        for a in Alembic.query.all():
            db.session.delete(a)
        db.session.commit()   
        print('----------------Alembic versions has been cleared.')
