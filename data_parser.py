import json
import math
import os

import requests

from config import json_data, list_headers, products_headers, query
from get_url import get_urls

def get_data(query):

    # Параметры
    offset = 0

    # Создаем папку data, если отсутствует
    if not os.path.exists('data'):
        os.mkdir('data')

    session = requests.Session()
    response = session.post(
        'https://dshop.kznexpress.ru/',
        headers=list_headers,
        json=json_data(
            query,
            offset)).json()

    # Число товаров
    total_items = response.get('data').get('makeSearch').get('total')

    if total_items is None:
        return 'No items'

    pages_count = math.ceil(total_items / 48)  # Вычисляем число страниц

    products_urls = get_urls(pages_count)

    products_id = []  # Список id товаров
    
    # Получаем id товаров
    for i in range(pages_count):
        offset = i * 48

        response = session.post(
            'https://dshop.kznexpress.ru/',
            headers=list_headers,
            json=json_data(
                query,
                offset)).json()
        products = response.get('data').get('makeSearch').get('items')
        for product in products:
            products_id.append(product.get('catalogCard').get('productId'))

    # with open('.\data\id.json', 'w', encoding='utf-8') as file:
    #    json.dump(products_id, file, indent=4, ensure_ascii=False)

    data = []  # Список с необходимыми полями товаров

    # Получаем с сайта нужные поля
    for i in range (len(products_id)):
        response = session.get(
            f'https://api.kazanexpress.ru/api/v2/product/{products_id[i]}',
            headers=products_headers).json()
        title = response.get('payload').get('data').get('title')
        seller = response.get('payload').get('data').get('seller').get('title')
        rating = response.get('payload').get('data').get('rating')
        orders = response.get('payload').get('data').get('rOrdersAmount')

        data.append([products_urls[i], seller, title, i+1, rating, orders])

    products_info = {
        'query': query,
        'data': data
    }

    return products_info


if __name__ == '__main__':
    result =  get_data(query[0])