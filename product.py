from uuid import uuid4
import sqlite3
from pathlib import Path

class Product:
    def __init__(self,
                 product_name:str,
                 quantity: int,
                 description: str,
                 photo: str,
                 location: str,
                 category: str,
                 Product_rank: float,
                 Productname: str,
                 Product_id: uuid4,                 
                 ) -> None:
        
        self.name = product_name        
        self.price = quantity
        self.quantity = quantity
        self.description = description
        self.photo = photo
        self.location = location
        self.category = category
        self.Product_rank = Product_rank
        self.Productname = Productname
        self.Product_id = Product_id

    def __str__(self) -> str:
        return f"{self.name} {self.price} {self.quantity} {self.description} {self.photo} {self.location} {self.category} {self.Product_rank} {self.Productname} {self.Product_id}"
    
    
    
    
    @staticmethod
    def connect():
        """ Connect to the SQLite database with an absolute path. """
        parent_path = Path().resolve()
        db_path = f'{parent_path}/products.db'  # Ensure this path exists
        return sqlite3.connect(db_path)

    @staticmethod
    def setup_database():
        """ Setup or create the database and the Product table. """
        conn = Product.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
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

    # def save(self):
    #     """ Insert a new Product into the database. """
    #     conn = Product.connect()
    #     cursor = conn.cursor()
    #     cursor.execute('INSERT INTO Products (name, surname, email, password, location, ranking) VALUES (?, ?, ?, ?, ?, ?)',
    #                    (self.name, self.surname, self.email, self.password, self.location, self.ranking))
    #     conn.commit()
    #     conn.close()

    # def update_email(self, new_email):
    #     """ Update the email address of the Product in the database. """
    #     self.email = new_email
    #     conn = Product.connect()
    #     cursor = conn.cursor()
    #     cursor.execute('UPDATE Products SET email = ? WHERE surname = ? AND name = ?', (new_email, self.surname, self.name))
    #     conn.commit()
    #     conn.close()

    # def update_password(self, new_password):
    #     """ Update the Product's password in the database. """
    #     self.password = new_password
    #     conn = Product.connect()
    #     cursor = conn.cursor()
    #     cursor.execute('UPDATE Products SET password = ? WHERE surname = ? AND name = ?', (new_password, self.surname, self.name))
    #     conn.commit()
    #     conn.close()



def main():
    print('malakas')
    product = Product("psalidi", 2, "psalidi", "psalidi", "psalidi", "psalidi", 4.8, "psalidi", uuid4())
    Product.setup_database()  # Initialize the database and tables
    # Product.save()  # Save the Product to the database



if __name__ == "__main__":
    main()

    