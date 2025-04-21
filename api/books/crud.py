import json

DB_FILE = 'books.json'

def load_books():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_books(books):
    with open(DB_FILE, 'w') as f:
        json.dump(books, f, indent=2)

def get_all_books():
    return load_books()

def add_book(book):
    books = load_books()
    books.append(book)
    save_books(books)

def update_book(isbn, new_data):
    books = load_books()
    for book in books:
        if book['isbn'] == isbn:
            book.update(new_data)
            break
    save_books(books)

def delete_book(isbn):
    books = load_books()
    books = [b for b in books if b['isbn'] != isbn]
    save_books(books)
