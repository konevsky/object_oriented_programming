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
        self._price = price  # Приватный атрибут цены
        self.quantity = quantity

    @property
    def price(self) -> float:
        """
        Возвращает цену товара.
        
        Returns:
            Цена товара
        """
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Устанавливает цену товара с проверкой на отрицательные значения.
        
        Args:
            value: Новая цена товара
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self._price = value

    @classmethod
    def new_product(cls, product_dict: dict, existing_products: List['Product'] = None) -> 'Product':
        """
        Создает объект Product из словаря с параметрами.
        Если товар с таким же именем уже существует в existing_products,
        то объединяет количество и выбирает более высокую цены.
        
        Args:
            product_dict: Словарь с параметрами товара.
                         Ожидаемые ключи: 'name', 'description', 'price', 'quantity'
            existing_products: Список существующих товаров для проверки дубликатов
        
        Returns:
            Созданный или обновленный объект класса Product
        """
        new_product = cls(
            name=product_dict['name'],
            description=product_dict['description'],
            price=0,  # Временное значение
            quantity=int(product_dict['quantity'])
        )
        # Устанавливаем цену через сеттер для проверки
        new_product.price = float(product_dict['price'])
        
        # Проверяем наличие дубликатов, если передан список существующих товаров
        if existing_products:
            for existing_product in existing_products:
                if existing_product.name.lower() == new_product.name.lower():
                    # Объединяем количество
                    existing_product.quantity += new_product.quantity
                    # Выбираем более высокую цену
                    if new_product.price > existing_product.price:
                        existing_product.price = new_product.price
                    # Обновляем описание, если новое не пустое
                    if new_product.description and new_product.description.strip():
                        existing_product.description = new_product.description
                    return existing_product
        
        return new_product


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
