from typing import List
import json


class ProductIterator:
    """
    Вспомогательный класс для итерации по товарам категории.
    """
    
    def __init__(self, category: 'Category'):
        """
        Инициализирует итератор для категории.
        
        Args:
            category: Объект категории для итерации
        """
        self._products = category._get_products_list()
        self._index = 0
    
    def __iter__(self) -> 'ProductIterator':
        """
        Возвращает итератор.
        
        Returns:
            Сам себя
        """
        return self
    
    def __next__(self) -> 'Product':
        """
        Возвращает следующий товар в итерации.
        
        Returns:
            Следующий товар категории
            
        Raises:
            StopIteration: Когда товары закончились
        """
        if self._index >= len(self._products):
            raise StopIteration
        
        product = self._products[self._index]
        self._index += 1
        return product


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
        Устанавливает цену товара с проверкой на отрицательные значения
        и подтверждением при понижении цены.
        
        Args:
            value: Новая цена товара
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        
        # Проверяем, понижается ли цена
        if hasattr(self, '_price') and value < self._price:
            confirmation = input(f"Цена понижается с {self._price} до {value}. Подтвердите (y/n): ")
            if confirmation.lower() != 'y':
                print("Действие отменено")
                return
        
        self._price = value

    def __str__(self) -> str:
        """
        Возвращает строковое представление продукта.
        
        Returns:
            Строка в формате "Название продукта, 80 руб. Остаток: 15 шт."
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        """
        Возвращает общую стоимость товаров на складе для двух продуктов.
        
        Args:
            other: Другой объект Product для сложения
            
        Returns:
            Общая стоимость товаров (цена × количество для обоих продуктов)
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")
        
        total_self = self.price * self.quantity
        total_other = other.price * other.quantity
        return total_self + total_other

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
    def products(self) -> str:
        """
        Возвращает список товаров в виде отформатированных строк.
        
        Returns:
            Строка с информацией о товарах в формате:
            "Название продукта, 80 руб. Остаток: 15 шт."
        """
        if not self.__products:
            return "Товары отсутствуют"
        
        # Используем __str__ для каждого продукта
        product_strings = [str(product) for product in self.__products]
        return "\n".join(product_strings) + "\n"  # Добавляем \n в конце по шаблону

    def _get_products_list(self) -> List[Product]:
        """
        Внутренний метод для получения списка товаров (для тестов).
        
        Returns:
            Список товаров категории
        """
        return self.__products

    def get_iterator(self) -> ProductIterator:
        """
        Возвращает итератор по товарам категории.
        
        Returns:
            Объект ProductIterator для перебора товаров
        """
        return ProductIterator(self)

    def __str__(self) -> str:
        """
        Возвращает строковое представление категории.
        
        Returns:
            Строка в формате "Название категории, количество продуктов: 200 шт."
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


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
