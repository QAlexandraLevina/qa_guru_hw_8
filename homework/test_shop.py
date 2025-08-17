"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("Book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(500) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(300)
        assert product.quantity == 700
        print(f"\nКоличество товара в остатке: {product.quantity}")

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError) as va_er:
            product.buy(1001)
            assert str(va_er.value) == "Товар закончился!"

class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    # Проверка добавления товара в корзину
    def test_add_product(self, product):
        cart = Cart()
        cart.add_product(product, 3)
        cart.add_product(product, 4)
        assert cart.products[product] == 7
        print(f"\nДобавили в корзину {cart.products[product]} книг!")

        rubber = Product('Rubber', 150, 'White rubber', 20)
        cart.add_product(rubber, 2)
        assert cart.products[rubber] == 2
        print(f"\nДобавили в корзину {cart.products[rubber]} ластика!")

    # Проверка удаления товара из корзины без передачи количества
    def test_remove_product_without_quantity(self, product):
        cart = Cart()
        cart.add_product(product, 20)
        cart.remove_product(product)
        assert product not in cart.products
        print("\nВы не указали количество товаров для удаления!")

    # Проверка удаления несуществующего товара из корзины
    def test_remove_not_added_product(self, product):
        cart = Cart()
        assert product not in cart.products
        with pytest.raises(KeyError) as ky_er:
            cart.remove_product(product)
        assert str(ky_er.value) == "'Товара нет в корзине!'"
        print("\nВы не выбрали товар для удаления!")

    # Проверка удаления одного товара из корзины
    def test_remove_one_product(self, product):
        cart = Cart()
        cart.add_product(product, 10)
        add_quantity_product = cart.products[product]
        cart.remove_product(product, 1)
        removed_product = add_quantity_product - cart.products[product]
        assert cart.products[product] == 9
        print(f"\nУ Вас было {add_quantity_product} товаров в корзине.\n"
              f"Вы удалили {removed_product} позицию товара из корзины!\n"
              f"У Вас осталось {cart.products[product]} товаров в корзине.")

    # Проверка удаления всех товаров из корзины
    def test_remove_all_products(self, product):
        cart = Cart()
        cart.add_product(product, 9)
        add_quantity_product = cart.products[product]
        remove_quantity_products = add_quantity_product
        cart.remove_product(product, 9)
        assert product not in cart.products
        assert len(cart.products) == 0
        print(f"\nУ Вас было {add_quantity_product} товаров в корзине.\n"
              f"Вы удалили {remove_quantity_products} товаров из корзины.\n"
              f"У вас осталось {len(cart.products)} товаров в корзине.\n"
              f"Корзина пуста!")

    # Проверка удаления большего кол-ва товаров, чем есть в корзине
    def test_remove_product_move_quantity(self, product):
        cart = Cart()
        cart.add_product(product, 11)
        cart.remove_product(product, 20)
        assert product not in cart.products
        print("\nВы удалили все товары из корзины!")

    # Проверка очистки корзины (Проверка того, что словарь пустой - False)
    def test_clear_cart(self, product):
        cart = Cart()
        cart.add_product(product, 10)
        cart.clear()
        assert not cart.products
        print(f"\nКорзина пуста!")

    # Проверка вычисления общей стоимости всех товаров в корзине
    def test_get_total_price(self, product):
        cart = Cart()
        cart.add_product(product, 5)
        notebook = Product("Notebook", 130, "Squared paper", 25)
        cart.add_product(notebook, 2)
        assert cart.get_total_price() == 760
        print(f"\nОбщая стоимость всех товаров в корзине: {cart.get_total_price()}!")

    # Проверка покупки товара
    def test_buy_product(self, product):
        ruler = Product("Ruler", 30, "Ruler for drawing", 100)
        cart = Cart()
        primary_product_quantity = product.quantity
        primary_ruler_quantity = ruler.quantity
        cart.add_product(ruler, 7)
        cart.add_product(product, 10)
        assert sum(cart.products.values()) == 17
        assert len(cart.products) == 2
        print(f"\nВы положили в корзину {len(cart.products)} товара: {ruler.name} и {product.name}.\nВ общем количестве - {sum(cart.products.values())} штук.")
        cart.buy()
        product_taken = primary_product_quantity - product.quantity
        ruler_taken = primary_ruler_quantity - ruler.quantity
        assert product.quantity == 990
        print(f"Вы купили {product_taken} книг. На складе осталось {product.quantity} книг.")
        assert ruler.quantity == 93
        print(f"Вы купили {ruler_taken} линеек. На складе осталось {ruler.quantity} линейки.")
        assert len(cart.products) == 0
        print(f"В корзине осталось {len(cart.products)} товаров.")

    # Проверка покупки товара при недостаточном количестве на складе
    def test_buy_product_with_insufficient_quantity(self, product):
        cart = Cart()
        pencil = Product("Pencil", 100, "Black pencil", 100)
        cart.add_product(product, 1001)
        cart.add_product(pencil, 101)
        with pytest.raises(ValueError) as va_er:
            cart.buy()
            assert str(va_er.value) == "Товар закончился!"
        assert product.quantity == 1000
        assert pencil.quantity == 100
        assert len(cart.products) == 2
        print("\nВы не можете приобрести товаров больше, чем есть на складе!")