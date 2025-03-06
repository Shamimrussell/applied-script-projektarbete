import pytest #importerar pytest för att köra tester
import sqlite3 # importerar sqlite3 för att hantera databasen
from book_dao import BookDAO
from book import Book
 
# Fixture för att sätta upp testdatabasen innan varje test
@pytest.fixture
def book_dao():
    book_dao=BookDAO(":memory:")
 
    book_dao.clear_table()
   
    # Skapar några exempelböcker som ska läggas till i databasen för teständamål
    book1 = Book("Carolinas liv", "Deckare", "Carolina")
    book2 = Book("Shamims liv", "Drama", "Shamim")
    book3 = Book("Hassans liv", "Deckare", "Hassan")
   
    # Lägg till böckerna i databasen
    book_dao.insert_book(book1)
    book_dao.insert_book(book2)
    book_dao.insert_book(book3)
   
    # Returnera BookDAO-instansen till testfunktionerna så de kan använda den
    yield book_dao
   
    # Teardown: Rensa upp efter varje test genom att tömma tabellen och stänga databasen
    book_dao.clear_table()  # Tömmer databasen (tabellen)
    book_dao.close()        # Stänger databasanslutningen
 
# Testklass som innehåller alla testmetoder
class TestBookDAO:
 
    # Test för att hämta alla böcker från databasen
    def test_get_all_books(self, book_dao):
        # Hämta alla böcker från databasen
        books = book_dao.get_all_books()
       
        # Verifiera att det finns exakt tre böcker i databasen
        assert len(books) == 3
# CARRO PRESENTERAR HIT..
    # Test för att infoga en ny bok i databasen
    def test_insert_book(self, book_dao):
        # Skapa en ny bok
        new_book = Book("Ilias liv", "Fantasy", "Ilias")
       
        # Lägg till den nya boken i databasen
        book_dao.insert_book(new_book)
       
        # Hämta alla böcker från databasen på nytt
        books = book_dao.get_all_books()
       
        # Verifiera att det nu finns fyra böcker (eftersom vi lade till en ny bok)
        assert len(books) == 4
 
    # Test för att hitta en bok via titel
    def test_find_by_title(self, book_dao):
        # Skapa och lägg till en ny bok i databasen
        new_book = Book("Maltes liv", "Deckare", "Malte")
        book_dao.insert_book(new_book)
       
        # Hitta boken genom dess titel
        found_book = book_dao.find_by_title("Maltes liv")
       
        # Verifiera att boken faktiskt hittades och att beskrivningen är korrekt
        assert found_book is not None
        assert found_book.description == "Deckare"
 
    # Test för att uppdatera en bok
    def test_update_book(self, book_dao):
        # Hitta en bok i databasen som ska uppdateras
        book_to_update = book_dao.find_by_title("Carolinas liv")
       
        # Uppdatera bokens beskrivning
        book_to_update.description = "romantik"
       
        # Uppdatera boken i databasen
        book_dao.update_book(book_to_update)
       
        # Hämta den uppdaterade boken och verifiera att beskrivningen har ändrats
        updated_book = book_dao.find_by_title("Carolinas liv")
        assert updated_book.description == "romantik"
 
    # Test för att ta bort en bok från databasen
    def test_delete_book(self, book_dao):
        # Hitta boken som ska tas bort
        book_to_delete = book_dao.find_by_title("Shamims liv")
       
        # Ta bort boken från databasen
        book_dao.delete_book(book_to_delete)
       
        # Försök att hitta den borttagna boken och verifiera att den inte finns längre
        deleted_book = book_dao.find_by_title("Shamims liv")
        assert deleted_book is None
        #Kontrollerar så att det finns 2 böcker efter den borttagna boken
        books_after_deletion = setup_database.get_all_books()
        assert len(books_after_deletion) == 2