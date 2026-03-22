from src.models import Category, Product

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
for product in category.products:
    print(f"- {product.name}: {product.price} руб. (в наличии: {product.quantity})")
