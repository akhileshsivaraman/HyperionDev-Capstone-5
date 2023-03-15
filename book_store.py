#==== import libraries ====
import sqlite3


#==== connect to database ====
db = sqlite3.connect("ebookstore.db")
cursor = db.cursor()


#==== books table ====
try:
  # create the books table if it does not exist
  cursor.execute('''
  CREATE TABLE books(
    id int(4),
    Title varchar,
    Author varchar,
    Quantity int,
    PRIMARY KEY (id)
  )
  ''')
  
  # dictionary of data to add to the new table
  dic = {
    "3001" : [3001, "A Tale of Two Cities", "Charles Dickens", 30],
    "3002" : [3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40],
    "3003" : [3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25],
    "3004" : [3004, "The Lord of the Rings", "J.R.R. Tolkien", 37], 
    "3005" : [3005, "Alice in Wonderland", "Lewis Carroll", 12]
  }
  
  # add data to the new table
  for i in dic:
    id_num = dic[i][0]
    title = dic[i][1]
    author = dic[i][2]
    quantity = dic[i][3]
    cursor.execute('''
    INSERT INTO books(id, Title, Author, Quantity)
    VALUES(:id, :Title, :Author, :Quantity)''',
    {"id":id_num, "Title":title, "Author":author, "Quantity":quantity})
  
  # commit changes to the database
  db.commit()
  
except:
  # when the table already exists, pass as there is nothing more to do
  pass


#==== functions ====
# add new book to the database
def add_book():
  
  # find the last ID in the database
  last = cursor.execute('''
  SELECT * FROM books
  ORDER BY ID DESC LIMIT 1
  ''')
  last_id = cursor.fetchone()[0]
  new_id = last_id + 1
  
  # ask the user for inputs
  title = input("Enter the title of the book: ")
  author = input("Enter the name of the author: ")
  quantity = int(input("Enter the quantity of books added to the store: "))
  
  # add the data to the table
  cursor.execute('''
  INSERT INTO books(id, Title, Author, Quantity)
  VALUES(:id, :Title, :Author, :Quantity)''',
  {"id":new_id, "Title":title, "Author":author, "Quantity":quantity})
  
  db.commit()

# update information of a book
def update_book():
  # ask user which book they want to update
  book_id = input("Enter the ID of the book you would like to update: ")
  
  
  # check the ID is valid
  cursor.execute('''
  SELECT * FROM books
  WHERE id = ?
  ''', (book_id,))
  book = cursor.fetchone()
  
  if book == None:
    # if the ID is not valid, tell the user
    print("The ID you have entered does not match a book in the store")
  else:
    # if the ID is valid, print information of the book
    print(f"\nInformation of the book you have selected\n"
    f"ID: {book[0]}\n"
    f"Title: {book[1]}\n"
    f"Author: {book[2]}\n"
    f"Quantity: {book[3]}")
  
    # ask the user what they want to update
    update_option = int(input(f"Would you like to update the title, author or quantity? \n"
    f"1. Title\n"
    f"2. Author\n"
    f"3. Quantity\n"))
    
    if update_option == 1:
      # ask user for new title
      new_title = input("Enter the new title: ")
      
      # update the entry
      cursor.execute('''
      UPDATE books
      SET Title = ?
      WHERE id = ?
      ''', (new_title, book_id))
      
      # show user the update is complete
      cursor.execute('''
      SELECT * FROM books
      WHERE id = ?
      ''', (book_id,))
      updated_entry = cursor.fetchall()
      print(f"ID {updated_entry[0][0]} updated\n"
      f"Title: {updated_entry[0][1]}")
      
    
    elif update_option == 2:
      # ask the user for new author
      new_author = input("Enter the new author's name: ")
      
      # update the entry
      cursor.execute('''
      UPDATE books
      SET Author = ?
      WHERE id = ?
      ''', (new_author, book_id))
      
      # show user the update is complete
      cursor.execute('''
      SELECT * FROM books
      WHERE id = ?
      ''', (book_id,))
      updated_entry = cursor.fetchall()
      print(f"ID {updated_entry[0][0]} updated\n"
      f"Author: {updated_entry[0][2]}")
    
    
    elif update_option == 3:
      # ask the user for quantity
      new_quantity = int(input("Enter the new quantity of books: "))
      
      # update the entry
      cursor.execute('''
      UPDATE books
      SET Quantity = ?
      WHERE id = ?
      ''', (new_quantity, book_id))
      
      # show user the update is complete
      cursor.execute('''
      SELECT * FROM books
      WHERE id = ?
      ''', (book_id,))
      updated_entry = cursor.fetchall()
      print(f"ID {updated_entry[0][0]} updated\n"
      f"Quantity: {updated_entry[0][3]}")
      
    db.commit()
    
# delete book from the database
def delete_book():
  # ask the user which book they want to delete
  book_id = input("Enter the ID of the book you would like to delete: ")
  
  # check the ID is valid
  cursor.execute('''
  SELECT * FROM books
  WHERE id = ?
  ''', (book_id,))
  book = cursor.fetchone()
  
  if book == None:
    # if the ID is not valid, tell the user
    print("The ID you have entered does not match a book in the store")
  else:
    # if the ID is valid, print information of the book
    print(f"\nInformation of the book you have deleted\n"
  f"ID: {book[0]}\n"
  f"Title: {book[1]}\n"
  f"Author: {book[2]}\n"
  f"Quantity: {book[3]}")

  
  # delete the book
  cursor.execute('''
  DELETE FROM books
  WHERE id = ?
  ''', (book_id,))
  
  db.commit()

# search the database for a specific book
def search_bookstore():
  # ask the user which book they want to find
  book_id = input("Enter the ID of the book you would like to view: ")
  
  # check the ID is valid
  cursor.execute('''
  SELECT * FROM books
  WHERE id = ?
  ''', (book_id,))
  book = cursor.fetchone()
  
  if book == None:
    # if the ID is not valid, tell the user
    print("The ID you have entered does not match a book in the store")
  else:
    # if the ID is valid, print information of the book
    print(f"\nInformation of the book you have selected\n"
  f"ID: {book[0]}\n"
  f"Title: {book[1]}\n"
  f"Author: {book[2]}\n"
  f"Quantity: {book[3]}")



#=== menu ====
### remember to close the database connection at the end

while True:
  menu = int(input(f"Select one of the following options: \n"
  f"1. Add a new book to the store\n"
  f"2. Update a book\n"
  f"3. Delete a book from store\n"
  f"4. Search the bookstore\n"
  f"0. Exit\n"))
  
  if menu == 1:
    print("\nAdd a new book to the store\n")
    add_book()
    
  elif menu == 2:
    print("\nUpdate a book\n")
    update_book()
  
  elif menu == 3:
    print("\nDelete a book from the store\n")
    delete_book()
  
  elif menu == 4:
    print("\nSearch the bookstore\n")
    search_bookstore()
  
  elif menu == 0:
    db.close()
    print("\nGoodbye.")
    exit()
  
  else:
    print("You selected an invalid option. Please enter the number of the option you want to select.\n")
