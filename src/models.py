from typing import List
import json
from abc import ABC, abstractmethod


class ZeroQuantityError(Exception):
    """
    Custom exception for products with zero quantity.
    """
    pass


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.
    Определяет общую функциональность, которая должна быть у каждого продукта.
    """

    @abstractmethod
    def __str__(self) -> str:
        """
        Возвращает строковое представление продукта.

        Returns:
            Строка с информацией о продукте
        """
        pass

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        """
        Возвращает общую стоимость товаров на складе для двух продуктов.

        Args:
            other: Другой объект продукта для сложения

        Returns:
            Общая стоимость товаров
        """
        pass


class CreationMixin:
    """
    Миксин для логирования создания объектов.
    Печатает информацию о создании объекта в консоль.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализирует объект и логирует его создание.
        """
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: {args}")
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        """
        Возвращает представление объекта для отладки.

        Returns:
            Строка с именем класса и параметрами
        """
        class_name = self.__class__.__name__
        attrs = []
        for key, value in self.__dict__.items():
            attrs.append(f"{key}={repr(value)}")
        return f"{class_name}({', '.join(attrs)})"


class BaseEntity(ABC):
    """
    Абстрактный базовый класс для сущностей с общими свойствами.
    """

    @abstractmethod
    def __str__(self) -> str:
        """
        Возвращает строковое представление сущности.

        Returns:
            Строка с информацией о сущности
        """
        pass


class Order(BaseEntity):
    """
    Класс для представления заказа.
    """

    def __init__(self, product: BaseProduct, quantity: int):
        """
        Инициализирует заказ.

        Args:
            product: Товар, который был куплен
            quantity: Количество купленного товара
        """
        if not isinstance(product, BaseProduct):
            raise TypeError("Товар должен быть наследником BaseProduct")

        if quantity <= 0:
            raise ValueError("Количество товара должно быть положительным")

        if quantity > product.quantity:
            raise ValueError(f"Недостаточно товара на складе. Доступно: {product.quantity}, запрошено: {quantity}")

        self.product = product
        self.quantity = quantity
        self.total_cost = product.price * quantity

        # Уменьшаем количество товара на складе
        product.quantity -= quantity

    def __str__(self) -> str:
        """
        Возвращает строковое представление заказа.

        Returns:
            Строка с информацией о заказе
        """
        return (
            f"Заказ: {self.product.name}, количество: {self.quantity} шт., итоговая стоимость: {self.total_cost} руб."
        )

    def __repr__(self) -> str:
        """
        Возвращает представление заказа для отладки.

        Returns:
            Строка с параметрами заказа
        """
        return f"Order(product={repr(self.product)}, quantity={self.quantity}, total_cost={self.total_cost})"


class ProductIterator:
    """
    Вспомогательный класс для итерации по товарам категории.
    """

    def __init__(self, category: "Category"):
        """
        Инициализирует итератор для категории.

        Args:
            category: Объект категории для итерации
        """
        self._products = category._get_products_list()
        self._index = 0

    def __iter__(self) -> "ProductIterator":
        """
        Возвращает итератор.

        Returns:
            Сам себя
        """
        return self

    def __next__(self) -> "Product":
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


class Product(CreationMixin, BaseProduct):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        
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
        if hasattr(self, "_price") and value < self._price:
            confirmation = input(f"Цена понижается с {self._price} до {value}. Подтвердите (y/n): ")
            if confirmation.lower() != "y":
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

    def __add__(self, other: "Product") -> float:
        """
        Возвращает общую стоимость товаров на складе для двух продуктов.

        Args:
            other: Другой объект Product для сложения

        Returns:
            Общая стоимость товаров (цена × количество для обоих продуктов)

        Raises:
            TypeError: если типы объектов не совпадают
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        # Проверяем, что объекты принадлежат одному и тому же классу
        if type(self) is not type(other):
            raise TypeError(f"Нельзя складывать товары разных классов: {type(self).__name__} и {type(other).__name__}")

        total_self = self.price * self.quantity
        total_other = other.price * other.quantity
        return total_self + total_other

    @classmethod
    def new_product(cls, product_dict: dict, existing_products: List["Product"] = None) -> "Product":
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
            name=product_dict["name"],
            description=product_dict["description"],
            price=0,  # Временное значение
            quantity=int(product_dict["quantity"]),
        )
        # Устанавливаем цену через сеттер для проверки
        new_product.price = float(product_dict["price"])

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


class Category(BaseEntity):
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
        Добавляет товар в категорию с проверкой типа.

        Args:
            product: Объект класса Product или его наследников для добавления

        Raises:
            TypeError: если переданный объект не является Product или его наследником
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

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

    def get_average_price(self) -> float:
        """
        Вычисляет среднюю цену всех товаров в категории.

        Returns:
            Средняя цена товаров или 0, если товаров нет
        """
        try:
            if not self.__products:
                return 0.0
            
            total_price = sum(product.price for product in self.__products)
            average_price = total_price / len(self.__products)
            return average_price
        except ZeroDivisionError:
            return 0.0

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

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for category_data in data:
        products = []
        for product_data in category_data["products"]:
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=float(product_data["price"]),
                quantity=int(product_data["quantity"]),
            )
            products.append(product)

        category = Category(name=category_data["name"], description=category_data["description"], products=products)
        categories.append(category)

    return categories


class Smartphone(Product):
    """
    Класс для представления смартфонов, наследник от Product.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
    ):
        """
        Инициализирует смартфон с дополнительными атрибутами.

        Args:
            name: Название смартфона
            description: Описание смартфона
            price: Цена смартфона
            quantity: Количество на складе
            efficiency: Производительность
            model: Модель
            memory: Объем встроенной памяти в ГБ
            color: Цвет
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """
    Класс для представления газонной травы, наследник от Product.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        """
        Инициализирует газонную траву с дополнительными атрибутами.

        Args:
            name: Название травы
            description: Описание травы
            price: Цена травы
            quantity: Количество на складе
            country: Страна-производитель
            germination_period: Срок прорастания
            color: Цвет
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
