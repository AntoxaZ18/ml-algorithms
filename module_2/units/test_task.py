import pytest
from module_2.units.task_1 import BooksCollector


@pytest.fixture
def collector() -> BooksCollector:
    return BooksCollector()

@pytest.mark.parametrize("book", [
    ("Book1"),  
    ("Book2"),  
])
def test_add_new_book(collector, book):
    """
    Проверяет добавление новой книги.
    """
    collector.add_new_book(book)
    assert book in collector.books_genre
    assert collector.books_genre[book] is None

    # Проверка исключения при передаче невалидного типа
    with pytest.raises(ValueError, match="book must be a string"):
        collector.add_new_book(123)


def test_set_book_genre(collector):
    """
    Проверяет установку жанра для книги.
    """
    collector.add_new_book("Book1")
    collector.set_book_genre("Book1", "Fantasy")
    assert collector.books_genre["Book1"] == "Fantasy"

    # Проверка исключения при передаче невалидных типов
    with pytest.raises(ValueError, match="book and genre must be a string"):
        collector.set_book_genre(123, "Fantasy")

    with pytest.raises(ValueError, match="book and genre must be a string"):
        collector.set_book_genre("Book1", 456)


def test_get_book_genre(collector):
    """
    Проверяет получение жанра для книги.
    """
    collector.add_new_book("Book1")
    collector.set_book_genre("Book1", "Fantasy")
    assert collector.get_book_genre("Book1") == "Fantasy"

    # Проверка исключения при отсутствии книги
    with pytest.raises(ValueError, match="no book found"):
        collector.get_book_genre("NonexistentBook")
def test_get_books_with_specific_genre(collector):
    """
    Проверяет получение книг определенного жанра.
    """
    collector.add_new_book("Book1")
    collector.add_new_book("Book2")
    collector.set_book_genre("Book1", "Fantasy")
    collector.set_book_genre("Book2", "Fantasy")

    result = collector.get_books_with_specific_genre("Fantasy")
    assert result == ["Book1", "Book2"]

    # Проверка пустого списка при отсутствии книг заданного жанра
    result = collector.get_books_with_specific_genre("Mystery")
    assert result == []


def test_get_books_for_children(collector):
    """
    Проверяет получение книг для детей.
    """
    collector.genre_age_ratings = ["Horror", "Thriller"]  
    collector.add_new_book("Book1")
    collector.add_new_book("Book2")
    collector.set_book_genre("Book1", "Fantasy")
    collector.set_book_genre("Book2", "Horror")

    result = collector.get_books_for_children()
    assert result == ["Book1"] 

def test_add_book_to_favorites(collector):
    """
    Проверяет добавление книги в избранное.
    """
    collector.add_new_book("Book1")
    collector.add_book_to_favorites("Book1")
    assert "Book1" in collector._favorites

    collector.add_book_to_favorites("Book1")
    assert collector._favorites.count("Book1") == 1

def test_delete_book_from_favourites(collector):
    """
    Проверяет удаление книги из избранного.
    """
    collector.add_new_book("Book1")
    collector.add_book_to_favorites("Book1")
    collector.delete_book_from_favourites("Book1")
    assert "Book1" not in collector._favorites

    # Проверка, что ничего не ломается при попытке удалить несуществующую книгу
    collector.delete_book_from_favourites("NonexistentBook")
    assert collector._favorites == []

# Тестирование метода get_list_of_favourites_books
def test_get_list_of_favourites_books(collector):
    """
    Проверяет получение списка избранных книг.
    """
    collector.add_new_book("Book1")
    collector.add_new_book("Book2")
    collector.add_book_to_favorites("Book1")
    collector.add_book_to_favorites("Book2")

    result = collector.get_list_of_favourites_books()
    assert result == ["Book1", "Book2"]

    # Удаление одной книги и проверка результата
    collector.delete_book_from_favourites("Book1")
    result = collector.get_list_of_favourites_books()
    assert result == ["Book2"]
