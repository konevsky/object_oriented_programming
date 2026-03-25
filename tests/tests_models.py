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
    assert len(category.products) == 1


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
        assert len(category1.products) == 2

        # Проверяем товары первой категории
        product1 = category1.products[0]
        assert product1.name == "Товар 1"
        assert product1.description == "Описание товара 1"
        assert product1.price == 100.50
        assert product1.quantity == 5

        product2 = category1.products[1]
        assert product2.name == "Товар 2"
        assert product2.description == "Описание товара 2"
        assert product2.price == 200.75
        assert product2.quantity == 3

        # Проверяем вторую категорию
        category2 = categories[1]
        assert category2.name == "Вторая категория"
        assert len(category2.products) == 1

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
