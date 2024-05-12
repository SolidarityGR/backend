import pandas as pd
import numpy as np
from scipy.stats import linregress
import sqlite3
from pathlib import Path

class User:
    """
    A class to represent a user in a system, including interactions with a SQLite database.

    Attributes:
        name (str): First name of the user.
        surname (str): Last name of the user.
        email (str): Email address of the user.
        password (str): Password for the user's account.
        location (str): The geographic location associated with the user.
        ranking (float): A numerical rating or ranking for the user, defaulting to 4.8.
    """

    def __init__(self, name, surname, email, password, location):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password  # Passwords should ideally be hashed.
        self.location = location
        self.ranking = 4.8

    @staticmethod
    def connect():
        """ Connect to the SQLite database with an absolute path. """
        parent_path = Path().resolve()
        db_path = f'{parent_path}/users.db'  # Ensure this path exists
        return sqlite3.connect(db_path)

    @staticmethod
    def setup_database():
        """ Setup or create the database and the user table. """
        conn = User.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                location TEXT NOT NULL,
                ranking REAL NOT NULL DEFAULT 4.8
            )
        ''')
        conn.commit()
        conn.close()

    def save(self):
        """ Insert a new user into the database. """
        conn = User.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, surname, email, password, location, ranking) VALUES (?, ?, ?, ?, ?, ?)',
                       (self.name, self.surname, self.email, self.password, self.location, self.ranking))
        conn.commit()
        conn.close()

    def update_email(self, new_email):
        """ Update the email address of the user in the database. """
        self.email = new_email
        conn = User.connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET email = ? WHERE surname = ? AND name = ?', (new_email, self.surname, self.name))
        conn.commit()
        conn.close()

    def update_password(self, new_password):
        """ Update the user's password in the database. """
        self.password = new_password
        conn = User.connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET password = ? WHERE surname = ? AND name = ?', (new_password, self.surname, self.name))
        conn.commit()
        conn.close()

def main():
    print('malakas')
    user = User("John", "Doe", "john.doe@example.com", "securepassword123", "New York")
    User.setup_database()  # Initialize the database and tables
    user.save()  # Save the user to the database



if __name__ == "__main__":
    main()



