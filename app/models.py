

usertable="""create table IF NOT EXISTS users (id serial primary key not null,username text,email text,password text)"""
entrytable="""create table IF NOT EXISTS entries (id serial primary key not null,title text,content text,date text)"""

