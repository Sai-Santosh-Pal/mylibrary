##from flask import Flask, render_template, request, redirect, url_for
##import os
##import json
##import jsonify
##import requests
##from werkzeug.utils import secure_filename
##from pyzbar.pyzbar import decode
##from PIL import Image
##
##app = Flask(__name__)
##
##UPLOAD_FOLDER = 'static/uploads'
##os.makedirs(UPLOAD_FOLDER, exist_ok=True)
##app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
##
##books = []
##
##def extract_isbn_from_image(image_path):
##    img = Image.open(image_path)
##    decoded_objects = decode(img)
##    for obj in decoded_objects:
##        return obj.data.decode('utf-8')
##    return None
##
##def get_book_data(isbn):
##    # Try Google Books API first
##    google_api = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
##    response = requests.get(google_api)
##    if response.status_code == 200:
##        data = response.json()
##        if data.get("totalItems") and data["items"]:
##            info = data["items"][0]["volumeInfo"]
##            description = info.get("description") or info.get("searchInfo", {}).get("textSnippet", "No description available.")
##            return {
##                "title": info.get("title", "Unknown"),
##                "subtitle": info.get("subtitle"),
##                "author": ", ".join(info.get("authors", ["Unknown"])),
##                "isbn": isbn,
##                "page_count": info.get("pageCount"),
##                "published": info.get("publishedDate"),
##                "language": info.get("language"),
##                "preview": info.get("previewLink"),
##                "info_link": info.get("infoLink"),
##                "thumbnail": info.get("imageLinks", {}).get("thumbnail"),
##                "description": description  # Add description (or textSnippet)
##            }
##    # Fallback to OpenLibrary if no data found
##    open_url = f"https://openlibrary.org/isbn/{isbn}.json"
##    res = requests.get(open_url)
##    if res.status_code == 200:
##        book_data = res.json()
##        return {
##            "title": book_data.get("title", "Unknown"),
##            "author": book_data.get("authors", [])[0].get("name", "") if book_data.get("authors") else "",
##            "isbn": isbn,
##            "thumbnail": f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg",
##            "description": book_data.get("description", "No description available.")  # Add description
##        }
##    return None
##
##
##@app.route('/')
##def index():
##    return render_template('index.html', books=books)
##
##@app.route('/add', methods=['POST'])
##def add_book():
##    method = request.form.get('method')
##    if method == 'manual':
##        books.append({
##            'title': request.form['title'],
##            'author': request.form['author'],
##            'isbn': request.form['isbn'],
##            'thumbnail': None
##        })
##    elif method == 'isbn':
##        isbn = request.form['isbn_only']
##        book = get_book_data(isbn)
##        if book:
##            books.append(book)
##    elif method == 'image':
##        image = request.files['image']
##        if image:
##            filename = secure_filename(image.filename)
##            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
##            image.save(path)
##            isbn = extract_isbn_from_image(path)
##            if isbn:
##                book = get_book_data(isbn)
##                if book:
##                    books.append(book)
##    return redirect(url_for('index'))
##
##@app.route('/edit', methods=['POST'])
##def edit_book():
##    data = request.get_json()
##    index = int(data['index'])
##    if 0 <= index < len(books):
##        books[index]['title'] = data['title']
##        books[index]['author'] = data['author']
##        books[index]['isbn'] = data['isbn']
##    return "Success"
##
##@app.route('/delete', methods=['POST'])
##def delete_book():
##    data = request.get_json()
##    index = int(data['index'])
##    if 0 <= index < len(books):
##        books.pop(index)
##    return "Success"
##
##if __name__ == '__main__':
##    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
import requests
from werkzeug.utils import secure_filename
# import cv2
# from pyzbar.pyzbar import decode
# from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
DATA_FILE = 'books.json'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def load_books():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_books(books):
    with open(DATA_FILE, 'w') as f:
        json.dump(books, f, indent=2)

books = load_books()

# def extract_isbn_from_image(image_path):
#     img = cv2.imread(image_path)
#     detector = cv2.QRCodeDetector()
#     retval, decoded_info, points, straight_qrcode = detector(img)
#     if retval:
#         return decoded_info[0]
#     return None

def get_book_data(isbn):
    google_api = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(google_api)
    if response.status_code == 200:
        data = response.json()
        if data.get("totalItems") and data["items"]:
            info = data["items"][0]["volumeInfo"]
            description = info.get("description") or info.get("searchInfo", {}).get("textSnippet", "No description available.")
            return {
                "title": info.get("title", "Unknown"),
                "subtitle": info.get("subtitle"),
                "author": ", ".join(info.get("authors", ["Unknown"])),
                "isbn": isbn,
                "page_count": info.get("pageCount"),
                "published": info.get("publishedDate"),
                "language": info.get("language"),
                "preview": info.get("previewLink"),
                "info_link": info.get("infoLink"),
                "thumbnail": info.get("imageLinks", {}).get("thumbnail"),
                "description": description
            }

    open_url = f"https://openlibrary.org/isbn/{isbn}.json"
    res = requests.get(open_url)
    if res.status_code == 200:
        book_data = res.json()
        return {
            "title": book_data.get("title", "Unknown"),
            "author": book_data.get("authors", [])[0].get("name", "") if book_data.get("authors") else "",
            "isbn": isbn,
            "thumbnail": f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg",
            "description": book_data.get("description", "No description available.")
        }
    return None

@app.route('/')
def index():
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    method = request.form.get('method')
    if method == 'manual':
        books.append({
            'title': request.form['title'],
            'author': request.form['author'],
            'isbn': request.form['isbn'],
            'thumbnail': None
        })
    elif method == 'isbn':
        isbn = request.form['isbn_only']
        book = get_book_data(isbn)
        if book:
            books.append(book)
    # elif method == 'image':
    #     image = request.files['image']
    #     if image:
    #         filename = secure_filename(image.filename)
    #         path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #         image.save(path)
    #         isbn = extract_isbn_from_image(path)
    #         if isbn:
    #             book = get_book_data(isbn)
    #             if book:
    #                 books.append(book)
    save_books(books)
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])
def edit_book():
    data = request.get_json()
    index = int(data['index'])
    if 0 <= index < len(books):
        books[index]['title'] = data['title']
        books[index]['author'] = data['author']
        books[index]['isbn'] = data['isbn']
        save_books(books)
    return "Success"

@app.route('/delete', methods=['POST'])
def delete_book():
    data = request.get_json()
    index = int(data['index'])
    if 0 <= index < len(books):
        books.pop(index)
        save_books(books)
    return "Success"

if __name__ == '__main__':
    app.run(debug=True)

