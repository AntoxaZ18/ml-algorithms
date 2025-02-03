class BooksCollector:

    def __init__(self):
        self.books_genre = dict()
        self._favorites = []
        self.genre = []
        self.genre_age_ratings = []

    def add_new_book(self, book: str):
        if not isinstance(book, str):
            raise ValueError('book must be a string')
        self.books_genre[book] = None

    def set_book_genre(self, book: str, genre: str):
        if not isinstance(book, str) or not isinstance(genre, str):
            raise ValueError('book and genre must be a string')
            
        self.books_genre[book] = genre

    def get_book_genre(self, book: str):
        if book not in self.books_genre:
            raise ValueError('no book found')
        return self.books_genre.get(book)
    
    def get_books_with_specific_genre(self, genre):
        return [book for book, genre_ in self.books_genre.items() if genre_ == genre]
    
    def get_books_for_children(self):
        return [book for book, genre_ in self.books_genre.items() if genre_ not in self.genre_age_ratings]
    

    def add_book_to_favorites(self, book):
        if book not in self._favorites:
            self._favorites.append(book)

    def delete_book_from_favourites(self, book):
        if book in self._favorites:
            self._favorites.remove(book)

    def get_list_of_favourites_books(self):
        return self._favorites



