from flask import Flask
from flask_ngrok import run_with_ngrok
from flask import request
from flasgger import Swagger
import json

app = Flask(__name__)
swagger = Swagger(app, template_file='./swag.yaml')
run_with_ngrok(app)

books = [{'name': 'Сильмариллион', 'author': 'Джон Ронал Руэл Толкин'},
         {'name': 'Чужой Завет', 'author': 'Алан Дин Фостер'}, 
         {'name': 'Цветы для Элджернона', 'author': 'Дэниел Киз'}]

@app.route('/')
def hello_world():
    return 'Hello, World!'
  
@app.route('/books')
def get_books():
  return json.dumps(books)

@app.route('/book/<string:name>')
def get_book(name):
  for elem in books:
    if name in elem['name']:
      return json.dumps(elem)
  return {"message": "Book not found"}, 404

@app.route('/book', methods=['POST'])
def add_book():
  book = {'name': request.json.get('name'), 'author': request.json.get('author')}
  books.append(book)
  return json.dumps(book)
  
app.run()
