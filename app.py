from flask import Flask
from flask_ngrok import run_with_ngrok
from flask import request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, template_file='/swag.yaml')
run_with_ngrok(app)

class Book:
  name = ''
  author = ''
  def __init__(self, name, author):
    self.name = name
    self.author = author

from flask_marshmallow import Marshmallow
from marshmallow import fields
ma = Marshmallow(app)

class BookSchema(ma.Schema):
  name = fields.String()
  author = fields.String()

books = [Book('Сильмариллион', 'Джон Ронал Руэл Толкин'),
         Book('Чужой Завет', 'Алан Дин Фостер'), 
         Book('Цветы для Элджернона', 'Дэниел Киз')]

@app.route('/')
def hello_world():
    return 'Hello, World!'
  
@app.route('/books')
def get_books():
   return BookSchema(many=True).dumps(books)

@app.route('/book/<string:name>')
def get_book(name):
  for elem in books:
    if name in elem.name:
      return BookSchema().dumps(elem)
  return {"message": "Book not found"}, 404

@app.route('/book', methods=['POST'])
def add_book():
  # TODO вернуть 400 если пользователь не передал name и author (они нам необходимы)
  # {message: 'подставить нужное is required}, 400
  book = Book(request.json.get('name'), request.json.get('author'))
  books.append(book)
  return BookSchema().dumps(book)

# TODO создать метод удаления книги  methods=['DELETE'], вернуть кого удалили
# TODO создать метод изменения книги  methods=['PATCH'], вернуть результат
  
app.run()
