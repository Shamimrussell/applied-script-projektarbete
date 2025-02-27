import pytest
from book_dao import BookDAO
from book import Book


class TestBookDAO:
    def setup_method(self): #Körs innan varje test-metod
        self.db_file = "test_database.db"
        self.book_dao = BookDAO(self.db_file) # Skapar en BookDao-instans med testdatabas

        self.book1 = Book("Carolinas liv", "Deckare", "Carolina")
        self.book2 = Book("Shamims liv", "Drama", "Shamim")
        self.book3 = Book("Hassans liv", "Deckare", "Hassan")

        self.book_dao.insert_book(self.book1)
        self.book_dao.insert_book(self.book2)
        self.book_dao.insert_book(self.book3)


    def teardown_method(self): #Körs efter varje test-metod
        self.book_dao.clear_table()
        self.book_dao.close()

    def test_get_all_books(self):
        books = self.book_dao.get_all_books()
        assert len(books) == 3

    def test_update_book(self):
        new_book = Book("Ilias liv", "Fantasy", "Ilias") #Skapar ny bok
        self.book_dao.insert_book(new_book) #Lägger till boken i databasen
        books = self.book_dao.get_all_books() #hämtar alla böcker på nytt
        assert len(books) == 4 #verifierar att det nu finns 4 böcker

    def test_find_by_title(self):
        new_book = Book("en ny bok namn", "Deckare", "Författaren")
        self.book_dao.insert_book(new_book)
        found_book = self.book_dao.find_by_title("en ny bok namn")  #Hämtar boken via titel
    
        assert found_book is not None
        assert found_book.description == "Deckare"




