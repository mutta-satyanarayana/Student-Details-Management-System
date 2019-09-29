# db_setup.py
# for create table to import required
# methods from sqlalchemy module
from sqlalchemy import String
from sqlalchemy import Integer,Column

# To  create columns to one block to
# using "declarative_base"
from sqlalchemy.ext.declarative import \
						declarative_base

# Store table structure in database file to
# use "create_engine"
from sqlalchemy import create_engine

# create declarative_base() object
Base = declarative_base()

# create table structure 
class Student(Base):
	__tablename__ ="students"
	id= Column(Integer,nullable=False,
		primary_key=True)
	name =Column(String(20),nullable=False)
	mobile =Column(Integer,nullable=False)
	gender=Column(String(10),nullable=False)
	email=Column(String(25),nullable=False,\
		unique=True)
	password=Column(String(25),nullable=False)
	image=Column(String,nullable=False)

# batabse file object created
engine =create_engine("sqlite:///mydb.db")

# table structure created in database file
Base.metadata.create_all(engine)

# display status to user 
print("mydb.db created Suceessfully.")