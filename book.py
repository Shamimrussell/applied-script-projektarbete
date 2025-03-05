class Book:
    def __init__(self, title, description, author, id=None):
        #id är optional 
        #det ska inte skickas med när man skapar nya böcker som ej finns i databasen
        self.id = id
        self.title = title
        self.description = description
        self.author = author

    def __str__(self):
        return f"Book(id={self.id}, title='{self.title}', description='{self.description}', author='{self.author}')"