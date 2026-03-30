from src.models import Category, Product, load_categories_from_json
import json
import tempfile
import os


def test_product_creation():
    product = Product("Тест", "Описание", 10.0, 1)
    assert product.name == "Тест"
    assert product.price == 10.0


def test_category_creation():
    product = Product("Тест", "Описание", 10.0, 1)
    category = Category("Тестовая", "Описание", [product])
    assert len(category._get_products_list()) == 1


def test_category_class_counters():
    # Сбрасываем сразу, чтобы тест был независимым
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("A", "O", 1.0, 1)
    p2 = Product("B", "O", 2.0, 2)

    c1 = Category("C1", "desc", [p1])
    c2 = Category("C2", "desc", [p2, p1])

    assert Category.category_count == 2
    assert Category.product_count == 3

    # доступ из экземпляра
    assert c1.category_count == 2
    assert c2.product_count == 3


def test_load_categories_from_json():
    """Тест загрузки категорий из JSON файла"""
    # Создаем временный JSON файл с тестовыми данными
    test_data = [
        {
            "name": "Тестовая категория",
            "description": "Описание тестовой категории",
            "products": [
                {
                    "name": "Товар 1",
                    "description": "Описание товара 1",
                    "price": 100.50,
                    "quantity": 5
                },
                {
                    "name": "Товар 2",
                    "description": "Описание товара 2",
                    "price": 200.75,
                    "quantity": 3
                }
            ]
        },
        {
            "name": "Вторая категория",
            "description": "Описание второй категории",
            "products": [
                {
                    "name": "Товар 3",
                    "description": "Описание товара 3",
                    "price": 50.25,
                    "quantity": 10
                }
            ]
        }
    ]

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_file_path = f.name

    try:
        # Сбрасываем счетчики перед загрузкой
        Category.category_count = 0
        Category.product_count = 0

        # Загружаем категории
        categories = load_categories_from_json(temp_file_path)

        # Проверяем количество загруженных категорий
        assert len(categories) == 2

        # Проверяем первую категорию
        category1 = categories[0]
        assert category1.name == "Тестовая категория"
        assert category1.description == "Описание тестовой категории"
        assert len(category1._get_products_list()) == 2

        # Проверяем товары первой категории
        product1 = category1._get_products_list()[0]
        assert product1.name == "Товар 1"
        assert product1.description == "Описание товара 1"
        assert product1.price == 100.50
        assert product1.quantity == 5

        product2 = category1._get_products_list()[1]
        assert product2.name == "Товар 2"
        assert product2.description == "Описание товара 2"
        assert product2.price == 200.75
        assert product2.quantity == 3

        # Проверяем вторую категорию
        category2 = categories[1]
        assert category2.name == "Вторая категория"
        assert len(category2._get_products_list()) == 1

        # Проверяем счетчики класса
        assert Category.category_count == 2
        assert Category.product_count == 3

    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)


def test_load_categories_from_json_file_not_found():
    """Тест обработки отсутствующего файла"""
    try:
        load_categories_from_json("non_existent_file.json")
        assert False, "Должно было быть исключение FileNotFoundError"
    except FileNotFoundError:
        pass  # Ожидаемое исключение


def test_load_categories_from_json_invalid_json():
    """Тест обработки невалидного JSON"""
    # Создаем временный файл с невалидным JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        f.write('{"invalid": json content}')  # Невалидный JSON
        temp_file_path = f.name

    try:
        load_categories_from_json(temp_file_path)
        assert False, "Должно было быть исключение json.JSONDecodeError"
    except json.JSONDecodeError:
        pass  # Ожидаемое исключение
    finally:
        os.unlink(temp_file_path)


# Новые тесты для функциональности инкапсуляции

def test_category_private_products_attribute():
    """Тест того, что атрибут товаров является приватным"""
    product = Product("Тест", "Описание", 10.0, 1)
    category = Category("Тестовая", "Описание", [product])
    
    # Проверяем, что прямой доступ к __products невозможен
    try:
        _ = category.__products
        assert False, "Должен быть AttributeError при доступе к приватному атрибуту"
    except AttributeError:
        pass  # Ожидаемое поведение


def test_category_add_product():
    """Тест метода add_product"""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0
    
    product1 = Product("Товар1", "Описание1", 100.0, 5)
    category = Category("Тест", "Описание", [product1])
    
    initial_count = Category.product_count
    initial_products_count = len(category._get_products_list())
    
    product2 = Product("Товар2", "Описание2", 200.0, 3)
    category.add_product(product2)
    
    # Проверяем, что товар добавлен
    assert len(category._get_products_list()) == initial_products_count + 1
    assert Category.product_count == initial_count + 1
    assert product2 in category._get_products_list()


def test_category_products_info_property():
    """Тест геттера products"""
    product1 = Product("Товар1", "Описание1", 100.0, 5)
    product2 = Product("Товар2", "Описание2", 200.0, 3)
    category = Category("Тест", "Описание", [product1, product2])
    
    info = category.products
    
    # Проверяем формат вывода
    assert "Товар1, 100.0 руб. Остаток: 5 шт." in info
    assert "Товар2, 200.0 руб. Остаток: 3 шт." in info
    
    # Проверяем случай с пустым списком товаров
    empty_category = Category("Пустая", "Описание", [])
    assert empty_category.products == "Товары отсутствуют"


def test_product_new_product_class_method():
    """Тест класс-метода new_product"""
    product_dict = {
        "name": "Товар из словаря",
        "description": "Описание из словаря",
        "price": 150.0,
        "quantity": 7
    }
    
    product = Product.new_product(product_dict)
    
    assert product.name == "Товар из словаря"
    assert product.description == "Описание из словаря"
    assert product.price == 150.0
    assert product.quantity == 7


def test_product_new_product_with_duplicates():
    """Тест класс-метода new_product с дубликатами"""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0
    
    # Создаем существующий товар
    existing_product = Product("Существующий товар", "Старое описание", 100.0, 5)
    existing_products = [existing_product]
    
    # Создаем новый товар с таким же именем
    duplicate_dict = {
        "name": "Существующий товар",  # Такое же имя
        "description": "Новое описание",
        "price": 150.0,  # Более высокая цена
        "quantity": 3
    }
    
    result_product = Product.new_product(duplicate_dict, existing_products)
    
    # Должен вернуться существующий товар с обновленными данными
    assert result_product is existing_product
    assert result_product.quantity == 8  # 5 + 3
    assert result_product.price == 150.0  # Более высокая цена
    assert result_product.description == "Новое описание"


def test_product_new_product_with_lower_price():
    """Тест класс-метода new_product с более низкой ценой"""
    existing_product = Product("Товар", "Описание", 200.0, 5)
    existing_products = [existing_product]
    
    duplicate_dict = {
        "name": "Товар",
        "description": "Описание",
        "price": 150.0,  # Более низкая цена
        "quantity": 3
    }
    
    result_product = Product.new_product(duplicate_dict, existing_products)
    
    # Цена должна остаться высокой
    assert result_product.price == 200.0
    assert result_product.quantity == 8


def test_product_price_getter():
    """Тест геттера цены"""
    product = Product("Товар", "Описание", 100.0, 5)
    assert product.price == 100.0


def test_product_price_setter_valid():
    """Тест сеттера цены с валидным значением"""
    product = Product("Товар", "Описание", 100.0, 5)
    product.price = 150.0
    assert product.price == 150.0


def test_product_price_setter_negative():
    """Тест сеттера цены с отрицательным значением"""
    product = Product("Товар", "Описание", 100.0, 5)
    original_price = product.price
    
    # Пытаемся установить отрицательную цену
    product.price = -50.0
    
    # Цена не должна измениться
    assert product.price == original_price


def test_product_price_setter_zero():
    """Тест сеттера цены с нулевым значением"""
    product = Product("Товар", "Описание", 100.0, 5)
    original_price = product.price
    
    # Пытаемся установить нулевую цену
    product.price = 0.0
    
    # Цена не должна измениться
    assert product.price == original_price


# Новые тесты для функциональности __str__ и __add__

def test_product_str_method():
    """Тест метода __str__ для Product"""
    product = Product("Ноутбук", "Игровой ноутбук", 999.99, 5)
    result = str(product)
    
    expected = "Ноутбук, 999.99 руб. Остаток: 5 шт."
    assert result == expected


def test_category_str_method():
    """Тест метода __str__ для Category"""
    product1 = Product("Товар1", "Описание1", 100.0, 5)
    product2 = Product("Товар2", "Описание2", 200.0, 3)
    category = Category("Электроника", "Товары для компьютеров", [product1, product2])
    
    result = str(category)
    expected = "Электроника, количество продуктов: 8 шт."
    assert result == expected


def test_category_str_method_empty():
    """Тест метода __str__ для пустой Category"""
    category = Category("Пустая категория", "Описание", [])
    
    result = str(category)
    expected = "Пустая категория, количество продуктов: 0 шт."
    assert result == expected


def test_product_add_method():
    """Тест метода __add__ для Product"""
    product1 = Product("Товар1", "Описание1", 100.0, 10)  # 100 * 10 = 1000
    product2 = Product("Товар2", "Описание2", 200.0, 2)   # 200 * 2 = 400
    
    result = product1 + product2
    expected = 1000 + 400  # 1400
    
    assert result == expected


def test_product_add_method_zero_quantity():
    """Тест метода __add__ с нулевым количеством"""
    product1 = Product("Товар1", "Описание1", 100.0, 10)  # 100 * 10 = 1000
    product2 = Product("Товар2", "Описание2", 200.0, 0)   # 200 * 0 = 0
    
    result = product1 + product2
    expected = 1000 + 0  # 1000
    
    assert result == expected


def test_product_add_method_with_non_product():
    """Тест метода __add__ с не-Product объектом"""
    product = Product("Товар", "Описание", 100.0, 5)
    
    try:
        result = product + "не продукт"
        assert False, "Должно было быть исключение TypeError"
    except TypeError as e:
        assert "Можно складывать только объекты класса Product" in str(e)


def test_product_add_method_with_none():
    """Тест метода __add__ с None"""
    product = Product("Товар", "Описание", 100.0, 5)
    
    try:
        result = product + None
        assert False, "Должно было быть исключение TypeError"
    except TypeError as e:
        assert "Можно складывать только объекты класса Product" in str(e)
