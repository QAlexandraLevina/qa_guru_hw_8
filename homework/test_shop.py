"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


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
        print(f"Количество товара в остатке: {product.quantity}")

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

        chips = Product('Chips', 150, 'Crab-flavored chips', 20)
        cart.add_product(chips, 2)
        assert cart.products[chips] == 2

    # Проверка удаления товара из корзины без передачи количества
    def test_remove_product_without_quantity(self, product):
        cart = Cart()
        cart.add_product(product, 20)
        cart.remove_product(product)
        assert product not in cart.products

    # Проверка удаления несуществующего товара из корзины
    def test_remove_not_added_product(self, product):
        cart = Cart()
        assert product not in cart.products
        with pytest.raises(KeyError) as ky_er:
            cart.remove_product(product)
        assert str(ky_er.value) == "'Товара нет в корзине!'"

    # Проверка удаления одного товара из корзины
    def test_remove_one_product(self, product):
        cart = Cart()
        cart.add_product(product, 10)
        cart.remove_product(product, 1)
        assert cart.products[product] == 9

    # Проверка удаления всех товаров из корзины
    def test_remove_all_products(self, product):
        cart = Cart()
        cart.add_product(product, 9)
        cart.remove_product(product, 9)
        assert product not in cart.products

    # Проверка удаления большего кол-ва товаров, чем есть в корзине
    def test_remove_product_move_quantity(self, product):
        cart = Cart()
        cart.add_product(product, 11)
        cart.remove_product(product, 20)
        assert product not in cart.products

    # Проверка очистки корзины
    def test_clear_cart(self, product):
        cart = Cart()
        cart.add_product(product, 10)
        cart.clear()
        assert product not in cart