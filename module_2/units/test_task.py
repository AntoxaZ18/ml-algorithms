import pytest
from module_2.units.task_1 import BooksCollector

def test_add():
    collector = BooksCollector()

    with pytest.raises(ValueError):
        collector.add_new_book(8)
    
    collector.add_new_book('Отель Перекресток')

    assert collector.books_genre == {'Отель Перекресток': None}


def test_add_genre():
    collector = BooksCollector()

    with pytest.raises(ValueError):
        collector.set_book_genre(8, 'фантастика')

    with pytest.raises(ValueError):
        collector.set_book_genre('Отель Перекресток', 98)

    collector.set_book_genre('Отель Перекресток', 'фантастика')

    assert collector.books_genre == {'Отель Перекресток': 'фантастика'}
    

def test_get_book_genre():

    collector = BooksCollector()

    collector.set_book_genre('Отель Перекресток', 'фантастика')
    collector.set_book_genre('Пятьдесят на пятьдесят', 'Драма')
    collector.set_book_genre('Дракона не предлагать!', 'фантастика')
    collector.set_book_genre('Тайна мертвого ректора. Книга 1', 'Детектив')
    collector.set_book_genre('Высшая Каста', 'фантастика')

    assert collector.get_book_genre('Отель Перекресток') == 'фантастика'

    with pytest.raises(ValueError):
        collector.get_book_genre('Двадцать два')


    
