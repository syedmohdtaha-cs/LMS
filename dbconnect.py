import sqlite3  
  
con = sqlite3.connect("library1.db")  
print("Database opened successfully")  
  
con.execute("create table Students(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, pswd TEXT NOT NULL)")  
con.execute("CREATE TABLE Admin(book_id	Integer PRIMARY KEY AUTOINCREMENT, book_name TEXT NOT NULL, Author_name TEXT NOT NULL, Category TEXT NOT NULL, url TEXT NOT NULL)"); 
con.execute("CREATE TABLE Record(S_No INTEGER PRIMARY KEY AUTOINCREMENT, book_id NUMERIC NOT NULL, book_name TEXT NOT NULL, Student_id INTEGER NOT NULL, Student_name TEXT NOT NULL,FOREIGN KEY(Student_id) REFERENCES Students(id),FOREIGN KEY(book_id) REFERENCES Admin(book_id))"); 
con.execute("ALTER TABLE Admin ADD COLUMN Count INTEGER")
print("Table created successfully")  
  
con.close() 