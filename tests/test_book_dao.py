import pytest  # Importerar pytest för att köra tester
import sqlite3  # Importerar sqlite3 för att hantera databasen
from book_dao import BookDAO  # Importerar BookDAO för att hantera bokdatabasen
from book import Book  # Importerar Book-klassen som representerar böcker
 
# Fixture för att sätta upp testdatabasen innan varje test
@pytest.fixture
def book_dao():
    # Skapar en BookDAO-instans som använder en minnesdatabas
    book_dao = BookDAO(":memory:")
   
    # Skapar tabellen i databasen
    book_dao.create_table()
   
    # Skapar några exempelböcker som ska läggas till i databasen för testen
    book1 = Book("Carolinas liv", "Deckare", "Carolina")
    book2 = Book("Shamims liv", "Drama", "Shamim")
    book3 = Book("Hassans liv", "Deckare", "Hassan")
   
    # lagras   böckerna i databasen
    book_dao.insert_book(book1)
    book_dao.insert_book(book2)
    book_dao.insert_book(book3)
   
    # Returnera BookDAO-instansen så att testfunktionerna kan använda den
    yield book_dao
   
    # Teardown: Rensa upp efter varje test genom att tömma tabellen och stänga databasen
    book_dao.clear_table()  # Tömmer databasen
    book_dao.close()        # Stänger databasanslutningen
 
# Testklass som innehåller alla testmetoder
class TestBookDAO:
 
    # Test för att hämta alla böcker från databasen
    def test_get_all_books(self, book_dao): # här används fixture automatiskt utav pytest
        # Hämta alla böcker från databasen fixturen används  här för att hämta böckerna
        books = book_dao.get_all_books()
       
        assert len(books) == 3  # kontrollerar att 3 böcker hämtats från databasen som förberetts av fixturen
    # Test för att infoga en ny bok i databasen
   
    def test_insert_book(self, book_dao):
        # Skapa en ny bok
        new_book = Book("Ilias liv", "Fantasy", "Ilias")
       
        # Lägg till den nya boken i databasen
        book_dao.insert_book(new_book)
       
        # Hämta alla böcker från databasen även den nya boken
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
        assert found_book is not None  # Verifierar att boken finns
        assert found_book.description == "Deckare"  # Verifierar att bokens beskrivning är korrekt
 
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
        assert updated_book.description == "romantik"  # Verifiera att uppdateringen lyckades
 
    # Test för att ta bort en bok från databasen
    def test_delete_book(self, book_dao):
        # Hitta boken som ska tas bort
        book_to_delete = book_dao.find_by_title("Shamims liv")
       
        # Ta bort boken från databasen
        book_dao.delete_book(book_to_delete)
       
        # Försök att hitta den borttagna boken och verifiera att den inte finns längre
        deleted_book = book_dao.find_by_title("Shamims liv")
        assert deleted_book is None  # Verifiera att boken har tagits bort och inte finns längre
        #Kontrollerar så att det finns 2 böcker efter den borttagna boken
        books_after_deletion = book_dao.get_all_books()
        assert len(books_after_deletion) == 2