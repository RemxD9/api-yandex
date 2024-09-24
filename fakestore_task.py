import requests


# REST API Fake Store - https://fakestoreapi.com/
#
# Самостоятельно:
# 1 Вывести продукты, цена которых <20
# 2 Вывести все категории
# 3 Вывести все продукты с категорией  "jewelery"
# 4 Вывести всех пользователей
# 5 Добавить пользователя со своим именем.

class Request:
    def __init__(self):
        self.url = None
        self.answer = None
        self.result = []

    def add(self, other):
        self.result.append(other)

    def add_data(self, url):
        self.url = url
        return self.url

    def processing(self, url: str):
        self.add_data(url)
        self.answer = requests.get(url).json()
        return self

    def prices_less_than_20(self):
        for item in self.answer:
            if float(item['price']) <= 20.0:
                self.add({f"Название: {item['title']}": f'Цена: {item["price"]}'})
        return self

    def jewelery_format(self):
        for item in self.answer:
            self.add(f'Название: {item["title"]}, Категория: {item["category"]}')
        return self.result

    def sort_by_price(self):
        self.result.sort(key=lambda x: float(list(x.values())[0].replace('Цена:', '')), reverse=True)
        return self.result

    def users_format(self):
        for user in self.answer:
            self.add(user['username'])
        return self.result

    def add_user(self, user_json):
        url = 'https://fakestoreapi.com/users'
        response = requests.post(url, json=user_json).text
        self.add(response)
        return self.result

    def clear(self):
        self.answer = None
        self.result = []


if __name__ == '__main__':
    request = Request()
    products_less_than_20 = request.processing('https://fakestoreapi.com/products/').prices_less_than_20().sort_by_price()
    print(products_less_than_20)  # 1
    request.clear()
    categories = request.processing('https://fakestoreapi.com/products/categories').answer
    print(categories)  # 2
    request.clear()
    jewelery = request.processing('https://fakestoreapi.com/products/category/jewelery').jewelery_format()
    print(jewelery)  # 3
    request.clear()
    users = request.processing('https://fakestoreapi.com/users').users_format()
    print(users)  # 4
    request.clear()
    user_data = {
        "email": "Rem@gmail.com",
        "username": "RemxD",
        "password": "m38rmF$",
        "name": {
            "firstname": "Rem",
            "lastname": "xD"
        },
        "address": {
            "city": "kilcoole",
            "street": "7835 new road",
            "number": 5,
            "zipcode": "12926-3874",
            "geolocation": {
                "lat": "-37.3159",
                "long": "81.1496"
            }
        },
        "phone": "1-570-236-7673"
    }
    new_user = request.add_user(user_data)
    # Вернет только id (либо 1, либо 11. Т.к скорее всего там есть некое ограничение на добавление пользователя с
    # одинаковыми данными), может ошибка на стороне API
    print(new_user)  # 5
