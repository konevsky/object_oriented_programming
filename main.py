from src.models import Category, Product, load_categories_from_json


def main():
    print("=== Демонстрация работы с классами ===\n")

    # Создание объектов вручную
    print("1. Создание объектов вручную:")
    product1 = Product(
        "Ноутбук",
        "Игровой ноутбук",
        999.99,
        5,
    )
    product2 = Product(
        "Мышь",
        "Беспроводная мышь",
        29.99,
        10,
    )

    category = Category(
        "Электроника",
        "Товары для компьютеров",
        [product1, product2],
    )

    print(f"Категория: {category.name}")
    print(f"Описание: {category.description}")
    for product in category.products:
        print(f"- {product.name}: {product.price} руб. (в наличии: {product.quantity})")

    print(f"\nВсего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print("\n" + "=" * 50 + "\n")

    # Загрузка данных из JSON файла
    print("2. Загрузка данных из JSON файла:")

    # Сбрасываем счетчики перед загрузкой из JSON
    Category.category_count = 0
    Category.product_count = 0

    try:
        categories = load_categories_from_json("data/products.json")

        for category in categories:
            print(f"\nКатегория: {category.name}")
            print(f"Описание: {category.description}")
            print(f"Товары в категории ({len(category.products)} шт.):")

            for product in category.products:
                print(f"  - {product.name}")
                print(f"    Описание: {product.description}")
                print(f"    Цена: {product.price} руб.")
                print(f"    В наличии: {product.quantity} шт.")

        print("\nИтого после загрузки из JSON:")
        print(f"Всего категорий: {Category.category_count}")
        print(f"Всего товаров: {Category.product_count}")

    except FileNotFoundError:
        print("Ошибка: Файл data/products.json не найден")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")


if __name__ == "__main__":
    main()
