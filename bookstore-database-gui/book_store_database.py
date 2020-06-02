import sqlite3


class BookStoreDB:
	"""SQLite database"""

	def __init__(self, name="books"):
		self.name = name	


	def create_table(self):
		"""create SQL table"""
		sql_conn = sqlite3.connect(self.name)
		sql_cursor = sql_conn.cursor()
		sql_cursor.execute("CREATE TABLE IF NOT EXISTS books (book_id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(200), author VARCHAR(200), year_ YEAR, isbn VARCHAR(13))")
		sql_conn.commit()
		sql_conn.close()


	def delete_table(self):
		"""delete SQL table"""
		sql_conn = sqlite3.connect(self.name)
		sql_cursor = sql_conn.cursor()
		sql_cursor.execute("DROP TABLE IF EXISTS books")
		sql_conn.commit()
		sql_conn.close()


	def view_table(self):
		"""view SQL table"""
		sql_conn = sqlite3.connect(self.name)
		sql_cursor = sql_conn.cursor()
		sql_cursor.execute("SELECT * FROM books")
		rows = sql_cursor.fetchall()
		sql_conn.commit()
		sql_conn.close()
		return rows


	def search_data(self, title="", author="", year_="", isbn=""):
		"""search SQL table for specific row(s)"""
		sql_conn = sqlite3.connect(self.name)
		sql_cursor = sql_conn.cursor()
		sql_cursor.execute("SELECT * FROM books WHERE title=? OR author=? OR year_=? OR isbn=?", (title, author, year_, isbn))
		rows = sql_cursor.fetchall()
		sql_conn.commit()
		sql_conn.close()
		if not rows:
			return ("Could not find specified entry.",)
		return rows


	def view_row(self, title, author, year_, isbn):
		"""view specified row from table"""
		sql_conn = sqlite3.connect(self.name)
		sql_cursor = sql_conn.cursor()
		sql_cursor.execute("SELECT * FROM books WHERE title=? AND author=? AND year_=? AND isbn=?", (title, author, year_, isbn))
		row = sql_cursor.fetchone()
		sql_conn.commit()
		sql_conn.close()
		return row


	def insert_data(self, title, author, year_, isbn):
		"""insert data in SQL table"""
		sql_conn = sqlite3.connect(self.name)
		sql_cursor = sql_conn.cursor()
		sql_cursor.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?)", (None, title, author, year_, isbn))
		sql_conn.commit()
		sql_conn.close()


	def update_data(self, title, author, year_, isbn, book_id):
		"""delete data from SQL table"""
		sql_conn = sqlite3.connect(self.name)
		sql_cursor = sql_conn.cursor()
		sql_cursor.execute("UPDATE books SET title=?, author=?, year_=?, isbn=? WHERE book_id=?", (title, author, year_, isbn, book_id))
		sql_conn.commit()
		sql_conn.close()


	def delete_data(self, book_id):
		"""delete data from SQL table"""
		sql_conn = sqlite3.connect(self.name)
		sql_cursor = sql_conn.cursor()
		sql_cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
		sql_conn.commit()
		sql_conn.close()


BookStore = BookStoreDB("book_store.db")
#BookStore.delete_table()
# BookStore.create_table()

# for book in [("Wild Game: My Mother, Her Lover and Me", "Adrienne Brodeur", "2020", "9781784742584"), 
# 			("Colorless Tsukuru Tazaki and His Years of Pilgrimage", "Haruki Murakami", "2015", "9780099590378"), 
# 			("Jonathan Livingston Seagull", "Richard Bach", "1970", "9780684846842"), 
# 			("Velveteen Rabbit", "Margery Williams", "2006", "9780757303333"), 
# 			("The Little Prince", "Antoine de Saint-Exupery", "2004", "9781405216340"), 
# 			("The Shining", "Stephen King", "2020", "9780307743657"), 
# 			("Isaac Asimov", "I, Robot", "2013", "9780007532278"),
# 			("Rossum's Universal Robots", "Karel Capek", "2004", "9780141182087"),
# 			("Letters from a Stoic", "Seneca", "2017", "9780140442106"),
# 			("Little Women", "Louisa May Alcott", "2013", "9780099572961"),
# 			("To Kill a Mockingbird", "Harper Lee", "2015", "9781784870799"),
# 			("Of Mica and Men", "John Steinbeck", "1993", "9780140177398"),
# 			("The Complete Poetry of Edgar Allan Poe", "Edgar Allan Poe", "2009", "9780451531056")]:
# 	BookStore.insert_data(*book)
