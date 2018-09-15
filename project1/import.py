import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

engine = create_engine("postgresql+psycopg2://lbzjufkvjvtebx:793b53af15d23defb4713e24382f3bbd4bcbb3c9fa49fa5185421eaaa16bcc29@ec2-54-221-237-246.compute-1.amazonaws.com/dfoooegurrluke")
db = scoped_session(sessionmaker(bind=engine))

file = open("books.csv", "r")
reader = csv.reader(file)
next(reader)

def insertRecord():
    for isbn, title, author, year in reader:
        year = int(year)
        db.execute("DELETE FROM BOOKS")
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {'isbn':isbn, 'title':title,'author':author,'year':year})
        print(title+" added to the table.")

    db.commit()

if __name__ == "__main__":
    insertRecord()


