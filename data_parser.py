import json
import os
import math

from config import list_headers, products_headers, json_data, query
import requests



def get_data():

    #Параметры
    offset = 0


    #Создаем папку data, если отсутствует
    if not os.path.exists('data'):
        os.mkdir('data')

    session = requests.Session()
    response = session.post('https://dshop.kznexpress.ru/', headers=list_headers, json=json_data(query, offset)).json()

    #Число товаров
    total_items = response.get('data').get('makeSearch').get('total')
    
    if total_items is None:
        return 'No items'
    
    pages_count = math.ceil(total_items / 48) #Вычисляем число страниц

    products_id = []     #Список id товаров
    #Получаем id товаров
    for i in range(pages_count):
        offset = i * 48

        response = session.post('https://dshop.kznexpress.ru/', headers=list_headers, json=json_data(query, offset)).json()
        products = response.get('data').get('makeSearch').get('items')
        for product in products:
            products_id.append(product.get('catalogCard').get('productId'))
    
    #with open('.\data\id.json', 'w', encoding='utf-8') as file:
    #    json.dump(products_id, file, indent=4, ensure_ascii=False)


    num = 1 #Порядковый номер заказа
    data = [] #Список с необходимыми полями товаров

    #Получаем с сайта нужные поля
    for id in products_id:
        response = session.get(f'https://api.kazanexpress.ru/api/v2/product/{id}', headers=products_headers).json()
        title = response.get('payload').get('data').get('title')
        seller = response.get('payload').get('data').get('seller').get('title')
        rating = response.get('payload').get('data').get('rating')
        orders = response.get('payload').get('data').get('rOrdersAmount')

        data.append(['', seller, title, num, rating, orders])
        num += 1

    products_info = {
        'query': query,
        'data' : data
        }

    #with open('.\data\data.json', 'w', encoding='utf-8') as file:
    #    json.dump(products_info, file, indent=4, ensure_ascii=False)
    
    return products_info

if __name__ == '__main__':
    get_data()