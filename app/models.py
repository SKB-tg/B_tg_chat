import datetime
import pytz
from pydantic import BaseModel

from typing import Dict, List, NamedTuple, ByteString, Union, Any
import app.db as db



class TgUser(BaseModel):
	"""class TgUser"""
	id: int = 1
	codename: str = ""
	id_chat: int = 0
	first_name: str = ''
	last_name: str = ''
	is_bot: bool = False
	is_donate: bool = False

tguser = TgUser(**{'id': 0, "codename": "", "id_chat": 0, "created": "", "last_name": "", "first_name": "",
  "is_donate": False, "is_bot": False})

def add_tg_user(new_user: dict) -> TgUser:
	inserted_row_id=db.insert("tguser", {
	"codename": new_user['codename'],
	"id_chat": new_user['id_chat'],
	"created": _get_now_formatted(),
	"last_name": new_user['last_name'],
	"first_name": new_user['first_name'],
	"is_donate": new_user['is_donate'],
	"is_bot": new_user['is_bot']
	})
	d_tg_user=TgUser(id= 0, codename= "", is_donate= False, id_chat= 1, first_name= "").dict().update(new_user)
	#d_tg_user1=d_tg_user.dict(None, None,  None, False, None, include=['id', 'codename', 'id_chat', 'is_donate', 'first_name'])#.update(new_user)
	#tg_user_data = {i[0]: i[1] for i in new_user.items() if (i[0] != 'id') and (i[0] != 'username')}

	return #d_tg_user #(codename=new_user['username'], is_donate='1003', id_chat=None, first_name="first_name")


def tg_user_is_db(user_data: str) -> Union[bool, Any]:
	code = user_data#['username']
	cursor = db.get_cursor()
	try:
		cursor.execute(f"select * from tguser where codename='{code}'" )
	except Exception as e:
		print(42, e)
		return False
	result = cursor.fetchone()
	print (46, result)
	if result == None:
		return False
	tguser.id = result[0] 
	tguser.codename = result[1]
	tguser.id_chat = result[2] 
	tguser.last_name = result[4] 
	tguser.first_name = result[5] 
	tguser.is_donate = True if result[6] == 1 else False
	tguser.is_bot = True if result[7] == 1 else False
	return tguser

def update_coloms_user( id_db: int, coloms: list) -> bool:
	for i in coloms:
		col={}
		col.update(i)
	cursor = db.get_cursor()
	print(66, col)
	try:
		db.updates('tguser', id_db, col)
	except Exception as e:
		print(78, e)
		return False
	
	return True

def load_users() -> List[TgUser]:
  """Возвращает справочник категорий расходов из БД"""
  _users = db.fetchall(
      "tguser", "codename id_chat first_name is_donate".split()
  )
  return _users

# def get_user() -> List[Dict]:
#   """Возвращает справочник категорий."""
#   return _categories

def get_tguser( username: str) -> Union[bool, TgUser]:
	_users = load_users()
	for user in _users:
		if user['codename'] == username:
			codename=user['codename']
			cursor = db.get_cursor()
			try:
				cursor.execute(f"select * from tguser where codename='{codename}'" )
			except Exception as e:
				print(78, e)
				return False
			result = cursor.fetchone()
			print (107, result)
			if result == None:
				return False
			tguser.id = result[0]
			tguser.codename = result[1]
			tguser.id_chat = result[2] 
			#tguser.last_name = result[4] 
			tguser.first_name = result[5] 
			tguser.is_donate = True if result[6] == 1 else False
			#tguser.is_bot = result[7]
			print(112, tguser.is_donate)
	return tguser

def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")

def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
        print(type(file))
    return blob_data

#*********************************************************************************

def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    print("Данные из blob сохранены в: ", filename, "\n")

def get_img_product(emp_id):
	product_data = db.fetchall(
		"product", "id name description price slug".split()
	)
	for item in product_data:
		if item['id'] == emp_id:
			print("colon = ", type(item), "value = ")
			return item


class Product(NamedTuple): # таблица Товаров
	name: str #= models.CharField(max_length=50, verbose_name='Название')
	attribute: List[str]
	description: str #= models.TextField(null=True, blank=True, verbose_name='Описание')
	price: int #= models.PositiveIntegerField(verbose_name='Стоимость')
	slug: str #= models.CharField(max_length=80, verbose_name='Алиас')
	category: str

	#section #= models.ForeignKey('Section', on_delete=models.CASCADE, verbose_name='Раздел') # связь один ко многим с таблицой разделов
	#reviews #= models.ManyToManyField('Review', related_name='Product', verbose_name='Отзывы', through='ReviewProductRelation') # связь многие ко многим с таблицой Отзывов


def row_is_db(table: str, col: tuple) ->Product:
	cursor = db.get_cursor()
	try:
		cursor.execute(f"select * from {table} where {col[0]}='{col[1]}'" )
	except Exception as e:
		print("Ошибка при работе с SQLite", e)
		return None
	          
	result = cursor.fetchone()
	print (135, result)
	if result == None:
		return None
	Product.id = result[0],
	Product.name = result[1],
	Product.description = result[2],
	Product.price = result[3],
	Product.slug = result[4]
	Product.category = result[5],
	Product.attribute = result[6],
	return Product

def add_product(new_product: dict):
	try:
		inserted_row_id=db.insert("product", {
		"name": new_product['name'],
		"attribute": new_product['attribute'],
		"description": new_product['description'],
		"price": new_product['price'],
		"category": new_product['category'],
		"slug": new_product['slug']
		})
	except Exception as e:
		print("Ошибка при работе с SQLite", e)
	product_data = {i[0]: i[1] for i in new_product.items()}
	return Product(name=new_product['name'], attribute=new_product['attribute'], description=new_product['description'], price=new_product['price'], slug=new_product['slug'] , category=new_product['category'])#codename=None, id_chat=None, tg_user_data =tg_user_data)

	class Meta: # как будут отображаться в админке
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'

	class ProductPhoto(NamedTuple):
		"""docstring for product_photo"""
		image: bytes
		url: str

		# def __init__(self, arg):
		# 	super(ProductPhoto, self).__init__()
		# 	self.arg = arg
	def __str__(self): # для красивого вывода
	  return self.name


def add_img_product(photo: dict ) -> bool:
	filename_img = photo['url']
	blob_data_img = convert_to_binary_data(filename_img)
	inserted_row_img=db.insert_blob("product", ("id", 1), ("image", blob_data_img))
	print('lol',  inserted_row_img)
	return True


class Order(NamedTuple): # таблица Заказов
	id_n: int   # = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Автор') # связь один ко многим с Пользователем
	product: List[str]   # = models.ManyToManyField('Product', related_name='Order', verbose_name='Товары', through='OrderProductRelation') # связь многие ко многим с таблицой Товаров
	total: int   # = models.PositiveIntegerField(verbose_name='Общая стоимость заказа')
	user_id: int
	order_user_data: List[dict]
	complete: bool   # = models.BooleanField(default=False, verbose_name='Завершен')

	class Meta: # как будут отображаться в админке
	  verbose_name = 'Заказ'
	  verbose_name_plural = 'Заказы'

	def add_order_db(new_order: dict):
		inserted_row_id=db.insert("order", {
		"product": new_order['username'],
		"id_n": new_order['id'],
		"created": _get_now_formatted(),
		"total": new_order['last_name'],
		"count": new_order['first_name'],
		"user_id": new_order['first_name'],
		"order_user_data": new_order['photo_url'],
		"complete": new_order['is_bot']
		})
		db.close_ses()
		tg_user_data = {i[0]: i[1] for i in new_user.items() if (i[0] != 'id') and (i[0] != 'username')}

		return TgUser(codename=None, id_chat=None, tg_user_data =tg_user_data)


# class OrderProductRelation(models.Model): # промежуточная таблица заказ - товар
#     order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ') # связь один ко многим с таблицой Заказов
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар') # связь один ко многим с таблицой Товаров
#     amount = models.PositiveIntegerField(verbose_name='Количество')
#     total = models.PositiveIntegerField(verbose_name='Сумма')

#     class Meta: # как будут отображаться в админке
#         verbose_name = 'Заказ-Товар'
#         verbose_name_plural = 'Заказ-Товар'

#     def __str__(self): # для красивого вывода
#         return str(self.order) + ' ' + str(self.product.name)


#--------------------------------------------------------------------------
# class Message(NamedTuple):
#     """Структура распаршенного сообщения о новом расходе"""
#     amount: int
#     category_text: str


# class Expense(NamedTuple):
#     """Структура добавленного в БД нового расхода"""
#     id: Optional[int]
#     amount: int
#     category_name: str



# def add_expense(raw_message: str) -> Expense:
#     """Добавляет новое сообщение.
#     Принимает на вход текст сообщения, пришедшего в бот."""
#     parsed_message = _parse_message(raw_message)
#     category = Categories().get_category(
#         parsed_message.category_text)
#     inserted_row_id = db.insert("expense", {
#         "amount": parsed_message.amount,
#         "created": _get_now_formatted(),
#         "category_codename": category.codename,
#         "raw_text": raw_message
#     })
#     return Expense(id=None,
#                    amount=parsed_message.amount,
#                    category_name=category.name)

# class Category(NamedTuple):
#     """Структура категории"""
#     codename: str
#     name: str
#     is_base_expense: bool
#     aliases: List[str]


# class Categories:
#     def __init__(self):
#         self._categories = self._load_categories()

#     def _load_categories(self) -> List[Category]:
#         """Возвращает справочник категорий расходов из БД"""
#         categories = db.fetchall(
#             "category", "codename name is_base_expense aliases".split()
#         )
#         categories = self._fill_aliases(categories)
#         return categories

#     def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
#         """Заполняет по каждой категории aliases, то есть возможные
#         названия этой категории, которые можем писать в тексте сообщения.
#         Например, категория «кафе» может быть написана как cafe,
#         ресторан и тд."""
#         categories_result = []
#         for index, category in enumerate(categories):
#             aliases = category["aliases"].split(",")
#             aliases = list(filter(None, map(str.strip, aliases)))
#             aliases.append(category["codename"])
#             aliases.append(category["name"])
#             categories_result.append(Category(
#                 codename=category['codename'],
#                 name=category['name'],
#                 is_base_expense=category['is_base_expense'],
#                 aliases=aliases
#             ))

#         return categories_result

#     def get_all_categories(self) -> List[Dict]:
#         """Возвращает справочник категорий."""
#         return self._categories

#     def get_category(self, category_name: str) -> Category:
#         """Возвращает категорию по одному из её алиасов."""
#         finded = None
#         other_category = None
#         for category in self._categories:
#             if category.codename == "other":
#                 other_category = category
#             for alias in category.aliases:
#                 if category_name in alias:
#                     finded = category
#         if not finded:
#             finded = other_category
#         return  finded


