import requests

def fetch_book_by_isbn(isbn):
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        authors = data.get('authors', [])
        author_names = ', '.join(a.get('name', 'Unknown') for a in authors)
        return {
            'title': data.get('title', 'Unknown'),
            'author': author_names,
            'isbn': isbn
        }
    return {'title': 'Unknown', 'author': 'Unknown', 'isbn': isbn}
