import sqlite3
from book import Book

class BookDAO:
    def __init__(self, db_file):
        """Initialisera anslutningen till databasen och skapa tabellen om den inte finns."""
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row  # Gör att vi kan hämta kolumnnamn som index
        self.create_table()

    def create_table(self):
        """Skapar 'books'-tabellen om den inte redan existerar."""
        query = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            author TEXT NOT NULL
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def clear_table(self):
        """Tömmer 'books'-tabellen på alla rader."""
        query = "DELETE FROM books;"
        self.conn.execute(query)
        self.conn.commit()

    def insert_book(self, book):
        """Infogar en bok i databasen och returnerar det nya bok-id:t."""
        query = """
        INSERT INTO books (title, description, author)
        VALUES (?, ?, ?);
        """
        cur = self.conn.execute(query, (book.title, book.description, book.author))
        self.conn.commit()
        return cur.lastrowid

    def get_all_books(self):
        """Returnerar en lista med alla böcker i databasen."""
        query = "SELECT * FROM books;"
        cur = self.conn.execute(query)
        rows = cur.fetchall()
        return [Book(id=row["id"], title=row["title"], description=row["description"], author=row["author"]) for row in rows]

    def update_book(self, book):
        """Uppdaterar en bok i databasen baserat på ID."""
        if book.id is None:
            raise ValueError("Boken måste ha ett ID för att kunna uppdateras.")

        query = """
        UPDATE books
        SET title = ?, description = ?, author = ?
        WHERE id = ?;
        """
        cur = self.conn.execute(query, (book.title, book.description, book.author, book.id))
        self.conn.commit()
        return cur.rowcount > 0  # Returnerar True om en rad uppdaterades

    def delete_book(self, book):
        """Tar bort en bok från databasen baserat på ID."""
        query = "DELETE FROM books WHERE id = ?;"
        cur = self.conn.execute(query, (book.id,))
        self.conn.commit()
        return cur.rowcount > 0  # Returnerar True om en rad togs bort

    def find_by_title(self, title):
        """Söker efter en bok baserat på titel och returnerar en Book-instans eller None."""
        query = "SELECT * FROM books WHERE title = ? LIMIT 1;"
        cur = self.conn.execute(query, (title,))
        row = cur.fetchone()
        if row:
            return Book(id=row["id"], title=row["title"], description=row["description"], author=row["author"])
        return None  # Om ingen bok hittas

    def close(self):
        """Stänger databasanslutningen."""
        self.conn.close()