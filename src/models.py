from typing import List
import json
from pathlib import Path


class Product:
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.products = products

        # обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и товары из JSON файла.
    
    Args:
        file_path: Путь к JSON файлу
        
    Returns:
        Список объектов Category с товарами
        
    Raises:
        FileNotFoundError: Если файл не найден
        json.JSONDecodeError: Если файл содержит невалидный JSON
    """
    categories = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    for category_data in data:
        # Создаем товары для категории
        products = []
        for product_data in category_data['products']:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=float(product_data['price']),
                quantity=int(product_data['quantity'])
            )
            products.append(product)
        
        # Создаем категорию с товарами
        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)
    
    return categories
