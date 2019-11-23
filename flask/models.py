import os
import datetime
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = SqliteDatabase('still_breaking.sqlite')

# route for after models are set up
# DATABASE = PostgresqlDatabase(
#     'still_breaking', # Database name created using command creatdb <db_name>
#     user='', # your computer profile name
#     password='password',
#     host='localhost',
# )

class User(UserMixin, Model):
    id = PrimaryKeyField(null=False)
    email = CharField(unique=True)
    password = CharField()

    # def __str__(self):
    #     return '<User: {}, id: {}>'.format(self.email,self.id)

    # def __repr__(self):
    #     return '<User: {}, id:{}>'.format(self.email, self.id)

    class Meta:
        db_table = 'users'
        database = DATABASE

class Topic(Model):
    id = PrimaryKeyField(null=False)
    name = CharField()
    user = ForeignKeyField(User, backref='users')
    description = CharField()

    class Meta:
        db_table = 'topics'
        database = DATABASE

class Article(Model):
    id = PrimaryKeyField(null=False)
    topic = ForeignKeyField(Topic, backref='topics')
    source = CharField()
    title = CharField()
    description = CharField()
    url = CharField()
    urlToImage = CharField()
    publishedAt = DateTimeField()

    class Meta:
        db_table = 'articles'
        database = DATABASE

class Note(Model):
    id = PrimaryKeyField(null=False)
    article = ForeignKeyField(Article, backref='articles')
    title = CharField()
    text = CharField()

    class Meta:
        db_table = 'notes'
        database = DATABASE

class Search(Model):
    id = PrimaryKeyField(null=False)
    topic = ForeignKeyField(Topic, backref='topics')
    text = CharField()

    class Meta:
        db_table = 'searches'
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Topic, Article, Note, Search], safe = True)
    print("tables created successfully")
    DATABASE.close()

