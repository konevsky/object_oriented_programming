from src.models import Category, Product


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
