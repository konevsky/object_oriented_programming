from typing import List
import json


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

    @classmethod
    def new_product(cls, product_dict: dict) -> 'Product':
        """
        Создает объект Product из словаря с параметрами.
        
        Args:
            product_dict: Словарь с параметрами товара.
                         Ожидаемые ключи: 'name', 'description', 'price', 'quantity'
        
        Returns:
            Созданный объект класса Product
        
        Raises:
            KeyError: Если отсутствуют обязательные ключи в словаре
        """
        return cls(
            name=product_dict['name'],
            description=product_dict['description'],
            price=float(product_dict['price']),
            quantity=int(product_dict['quantity'])
        )


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.__products = products

        # обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """
        Добавляет товар в категорию.
        
        Args:
            product: Объект класса Product для добавления
        """
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[Product]:
        """
        Возвращает список товаров категории (только для чтения).
        
        Returns:
            Список товаров категории
        """
        return self.__products

    @property
    def products_info(self) -> str:
        """
        Возвращает список товаров в виде отформатированных строк.
        
        Returns:
            Строка с информацией о товарах в формате:
            "Название продукта, 80 руб. Остаток: 15 шт."
        """
        if not self.__products:
            return "Товары отсутствуют"
        
        products_list = []
        for product in self.__products:
            product_info = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            products_list.append(product_info)
        
        return "\n".join(products_list)


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
        products = []
        for product_data in category_data['products']:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=float(product_data['price']),
                quantity=int(product_data['quantity'])
            )
            products.append(product)

        category = Category(
            name=category_data['name'],
            description=category_data['description'],
            products=products
        )
        categories.append(category)

    return categories
