import datetime
import logging
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):

        self.root = tk.Tk()
        self.sorting_string = StringVar()

    def delete(self):
        pass

    @staticmethod
    def database_submit(name, price, data, description, ):
        """
        This function submits user input data to a database by checking if the input is valid
        (year <= 2023, month <= 12, and day <= 31) and then inserting the input into the "transactions" table.
        It also includes error handling for invalid data format.
        """

        data_now = datetime.datetime.now()
        date_int = (data[0:4] + data[5:7] + data[8:])
        year_now = int(data_now.year)

        try:

            user_year = int(data[0:4])
            user_month = int(data[5:7])
            user_day = int(data[8:])
            if user_year <= year_now and user_month <= 12 and user_day <= 31:
                conn = sqlite3.connect("baza.db")
                conn.execute(
                    "insert into transactions (name_of_transaction,price_of_transaction,data_of_transaction, "
                    "description_of_transaction) values (?,?, ? ,?)",
                    (name, price, date_int, description))

                conn.commit()

                conn.close()
            else:
                error_window = tk.Tk()
                tk.Label(error_window, text="Year must be less or equal to 2023, month must be in range 1-12 and "
                                            "number of day must be in range 1-30! ").grid(column=1, row=1)
                error_window.mainloop()

        except ValueError as ex:
            logging.error("Data of transaction must be a number, e.g.: 2021.12.30  ( YYYY.MM.DD ) ", ex)

    def database_read(self):
        """
        This function is have to transform data from database to python and return list of data
        which will print data to window (print_transaction function)
        """

        conn = sqlite3.connect("baza.db")
        cursor = conn.execute(f"SELECT * FROM transactions {self.sorting_string.get()}")

        list_of_data = []
        for i in cursor:
            list_of_data.append(i)

        return list_of_data

    def print_transactions(self):
        """
        This function display the transaction data stored in the database in a GUI using tkinter library,
        by creating a treeview widget and inserting the data into it, showing the data in a tabular format.
        """

        list_of_data = self.database_read()
        conn = sqlite3.connect("baza.db")
        win = Tk()
        win.geometry("700x350")
        style = ttk.Style()
        style.theme_use('clam')

        tree = ttk.Treeview(win, show='headings', height=10, columns="#1, #2, #3, #4")
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Name transaction")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="price transaction")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Data transaction")
        tree.column("# 4", anchor=CENTER)
        tree.heading("# 4", text="description transaction")

        for i in list_of_data:
            date = str(i[2])

            date_int = (date[6:8] + "." + date[4:6] + "." + date[0:4])

            tree.insert('', 'end', text="1", values=(i[0], i[1], date_int, i[3]))

        tree.pack()
        win.mainloop()

        conn.commit()
        conn.close()

    def submit_values(self, name, price, data, description):
        """
        This function is have to get text from entries (data of name, price, date, description)
        """
        print(name, price, data, description, "TEST")
        self.database_submit(name, price, data, description)
        self.print_transactions()

    def add(self):
        """
        This function is current when button "Add Transaction" was used.
        She is to create entries and button off submit values which have to save data from the user.
        """
        Name1 = tk.StringVar()
        price1 = tk.StringVar()
        data1 = tk.StringVar()
        description1 = tk.StringVar()
        name_of_transaction = tk.Entry(self.root, textvariable=Name1)
        name_of_transaction.grid(column=1, row=6)
        price_of_transaction = tk.Entry(self.root, textvariable=price1)
        price_of_transaction.grid(column=2, row=6)
        data_of_transaction = tk.Entry(self.root, textvariable=data1)
        data_of_transaction.grid(column=3, row=6)
        description_of_transaction = tk.Entry(self.root, textvariable=description1)
        description_of_transaction.grid(column=4, row=6)

        tk.Button(self.root, text="Submit", command=lambda:
        self.submit_values(Name1.get(), price1.get(), data1.get(), description1.get())).grid(column=4, row=4)

    def create_window(self):
        """
        This function is have to create main window with texts and buttons
        """
        self.root.geometry("960x1024")
        self.root.title("Oszczędności")
        add_transaction = ttk.Button(self.root, text="Add Transaction", command=self.add)
        add_transaction.grid(column=1, row=1)
        delete_transaction = ttk.Button(self.root, text="Delete Transaction", command=self.delete())
        delete_transaction.grid(column=2, row=1)
        tk.Label(self.root, text="Name transaction").grid(column=1, row=5)
        tk.Label(self.root, text="price").grid(column=2, row=5)
        tk.Label(self.root, text="Data ").grid(column=3, row=5)
        tk.Label(self.root, text="    description").grid(column=4, row=5)

        self.sorting_string = tk.StringVar()
        # Buttons of sorting
        Radiobutton(self.root, text="Sort by cheapest", variable=self.sorting_string,
                    value="ORDER BY price_of_transaction",
                    command=lambda: self.print_transactions()).grid(column=16, row=10)
        Radiobutton(self.root, text="Sort by most expensive", variable=self.sorting_string,
                    value="ORDER BY price_of_transaction DESC",
                    command=lambda: self.print_transactions()).grid(column=16, row=11)
        Radiobutton(self.root, text="Sort by most recent", variable=self.sorting_string,
                    value="ORDER BY data_of_transaction",
                    command=lambda: self.print_transactions()).grid(column=16, row=12)
        Radiobutton(self.root, text="Sort by oldest", variable=self.sorting_string,
                    value="ORDER BY data_of_transaction DESC",
                    command=lambda: self.print_transactions()).grid(column=16, row=13)

    def main(self):
        self.create_window()
        self.root.mainloop()


start = App()
start.main()
