import tkinter as tk
import book_store_database as dtbs


def command_reset():
	"""empties the four entry boxes"""
	listbox_title("Entries reset")
	entry_title.delete(0, tk.END)
	entry_author.delete(0, tk.END)
	entry_year.delete(0, tk.END)
	entry_isbn.delete(0, tk.END)


def command_view():
	"""displays all books from database"""
	listbox_title("All books:")
	list_box.delete(0, tk.END)
	for row in BOOKSTORE.view_table():
		list_box.insert(tk.END, row)


def command_search():
	"""displays book search results from database"""
	listbox_title("Search results:")
	list_box.delete(0, tk.END)
	for row in BOOKSTORE.search_data(entry_title_value.get(), entry_author_value.get(), entry_year_value.get(), entry_isbn_value.get()):
		list_box.insert(tk.END, row)


def command_add():
	"""adds book in database, then displays it"""
	list_box.delete(0, tk.END)
	book_title = entry_title_value.get()
	book_author = entry_author_value.get()
	book_year = entry_year_value.get()
	book_isbn = entry_isbn_value.get()
	if not all([book_title, book_author, book_year, book_isbn]):
		listbox_title("Cannot be added:")
		list_box.insert(tk.END, MISSING_VALUES_MSG)
	else:
		book = BOOKSTORE.view_row(book_title, book_author, book_year, book_isbn)
		if book:
			listbox_title("Already in database:")
			list_box.insert(tk.END, book)
		else:
			BOOKSTORE.insert_data(book_title, book_author, book_year, book_isbn)
			listbox_title("Book added:")
			list_box.insert(tk.END, BOOKSTORE.view_row(book_title, book_author, book_year, book_isbn))


def command_update():
	"""updates book in database, then displays original and changed"""
	try:
		book_to_update = BOOKSTORE.view_row(book_info[1], book_info[2], book_info[3], book_info[4])
	except Exception:
		pass
	else:
		list_box.delete(0, tk.END)
		if book_to_update:
			BOOKSTORE.update_data(entry_title_value.get(), entry_author_value.get(), entry_year_value.get(), entry_isbn_value.get(), book_info[0])
			listbox_title("Book updated:")
			list_box.insert(tk.END, book_to_update)
			updated_book = BOOKSTORE.view_row(entry_title_value.get(), entry_author_value.get(), entry_year_value.get(), entry_isbn_value.get())
			list_box.insert(tk.END, updated_book)
		else:
			listbox_title("Cannot be updated:")
			list_box.insert(tk.END, MISSING_VALUES_MSG)


def command_delete():
	"""deletes book from database, then displays it"""
	deleted_book = BOOKSTORE.view_row(entry_title_value.get(), entry_author_value.get(), entry_year_value.get(), entry_isbn_value.get())
	list_box.delete(0, tk.END)
	if deleted_book:
		try:
			BOOKSTORE.delete_data(book_info[0])
		except Exception:
			pass
		else:
			listbox_title("Book deleted:")
			list_box.insert(tk.END, deleted_book)
	else:
		listbox_title("Could not delete:")
		list_box.insert(tk.END, MISSING_VALUES_MSG)


def command_close():
	"""closes GUI"""
	window.destroy()


def listbox_title(message):
	"""displays current action above listbox"""
	global label_list
	label_list = tk.Label(window, text=message)
	label_list.grid(row=2+y_adj,column=2+x_adj)


def get_row(event):
	"""grabs the book id when the user selects a row"""
	try:
		global book_info
		index = list_box.curselection()[0]
		book_info = list_box.get(index)
		entry_title.delete(0, tk.END)
		entry_title.insert(tk.END, book_info[1])
		entry_author.delete(0, tk.END)
		entry_author.insert(tk.END, book_info[2])
		entry_year.delete(0, tk.END)
		entry_year.insert(tk.END, book_info[3])
		entry_isbn.delete(0, tk.END)
		entry_isbn.insert(tk.END, book_info[4])
	except Exception:
		pass


BOOKSTORE = dtbs.BookStoreDB("book_store.db")
MISSING_VALUES_MSG = "Missing values"
x_adj = -1  # row positioning
y_adj = 1  # col positioning
window = tk.Tk()
window.title('Bookstore catalogue')


	### LABELS ###

# Title label
label_title = tk.Label(window, text="Title:")
label_title.grid(row=0+y_adj,column=1+x_adj)

# Author label
label_author = tk.Label(window, text="Author:")
label_author.grid(row=0+y_adj,column=3+x_adj)

# Title label
label_year = tk.Label(window, text="Year:")
label_year.grid(row=1+y_adj,column=1+x_adj)

# Author label
label_isbn = tk.Label(window, text="ISBN:")
label_isbn.grid(row=1+y_adj,column=3+x_adj)

# Listbox label
label_list = tk.Label(window, text="")
label_list.grid(row=2+y_adj,column=2+x_adj)

	### ENTRY BOXES ###

# Title entry
entry_title_value = tk.StringVar()
entry_title = tk.Entry(window, textvariable=entry_title_value)
entry_title.grid(row=0+y_adj, column=2+x_adj)

# Author entry
entry_author_value = tk.StringVar()
entry_author = tk.Entry(window, textvariable=entry_author_value)
entry_author.grid(row=0+y_adj, column=4+x_adj)

# Year entry
entry_year_value = tk.StringVar()
entry_year = tk.Entry(window, textvariable=entry_year_value)
entry_year.grid(row=1+y_adj, column=2+x_adj)

# ISBN entry
entry_isbn_value = tk.StringVar()
entry_isbn = tk.Entry(window, textvariable=entry_isbn_value)
entry_isbn.grid(row=1+y_adj, column=4+x_adj)

	### BUTTONS & COMMANDS ###

# Reset button
btn_reset = tk.Button(window, text='Reset', command=command_reset)
btn_reset.grid(row=0, column=0)

# View button
btn_view = tk.Button(window, text='View All', width=7, command=command_view)
btn_view.grid(row=4, column=0)

# Search button
btn_search = tk.Button(window, text='Search', width=7, command=command_search)
btn_search.grid(row=5, column=0)

# Add button
btn_add = tk.Button(window, text='Add', width=7, command=command_add)
btn_add.grid(row=6, column=0)

# Update button
btn_update = tk.Button(window, text='Update', width=7, command=command_update)
btn_update.grid(row=7, column=0)

# Delete button
btn_delete = tk.Button(window, text='Delete', width=7, command=command_delete)
btn_delete.grid(row=8, column=0)

# Close button
btn_close = tk.Button(window, text='Close', width=7, command=command_close)
btn_close.grid(row=9, column=0)

	### LISTBOX ###

list_box = tk.Listbox(window, height=10, width=100)
list_box.grid(row=4, rowspan=6, column=1, columnspan=8)
list_box.bind('<<ListboxSelect>>', get_row)

	### SCROLLBAR ###

scroll_bar = tk.Scrollbar(window)
scroll_bar.grid(row=4, rowspan=6, column=9)
list_box.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_box.yview)


window.mainloop()
