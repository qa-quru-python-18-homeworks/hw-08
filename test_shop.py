import pytest

from models import Cart, Product


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    @pytest.mark.parametrize(
        "requested_quantity, expected_result",
        [(999, True), (1000, True), (1001, False)],
    )
    def test_product_check_quantity(self, product, requested_quantity, expected_result):
        assert product.check_quantity(requested_quantity) == expected_result

    def test_product_check_quantity_exception(self, product):
        with pytest.raises(ValueError):
            product.check_quantity(-1)

    def test_product_buy(self, product):
        product.buy(1000)
        assert product.quantity == 0

    @pytest.mark.parametrize(
        "requested_quantity, expected_exception",
        [(1001, ValueError), (-1, ValueError)],
    )
    def test_product_check_buy_exception(
        self, product, requested_quantity, expected_exception
    ):
        with pytest.raises(expected_exception):
            product.buy(requested_quantity)


class TestCart:
    def test_new_cart_is_empty(self):
        cart = Cart()
        assert len(cart.products) == 0

    def test_add_product(self, product):
        cart = Cart()
        cart.add_product(product, buy_count=10)
        cart.add_product(product)
        assert len(cart.products) == 1
        assert cart.products[product] == 11

    @pytest.mark.parametrize("buy_count", [-1, 0])
    def test_add_zero_or_less_product(self, product, buy_count):
        cart = Cart()
        with pytest.raises(ValueError):
            cart.add_product(product, buy_count)

    @pytest.mark.parametrize("remove_count", [1, None])
    def test_remove_all_product_from_cart(self, product, remove_count):
        cart = Cart()
        cart.add_product(product)
        cart.remove_product(product, remove_count)
        assert product not in cart.products

    def test_remove_not_all_product_from_cart(self, product):
        cart = Cart()
        cart.add_product(product, buy_count=10)
        cart.remove_product(product, remove_count=5)
        assert cart.products[product] == 5

    @pytest.mark.parametrize("remove_count", [-1, 0])
    def test_remove_zero_or_less_product_from_cart(self, product, remove_count):
        cart = Cart()
        cart.add_product(product, buy_count=10)
        with pytest.raises(ValueError):
            cart.remove_product(product, remove_count)

    def test_clear_cart(self, product):
        cart = Cart()
        cart.add_product(product)
        cart.clear()
        assert len(cart.products) == 0

    def test_total_price(self, product):
        cart = Cart()
        cart.add_product(product, buy_count=10)
        assert cart.get_total_price() == 1000

    def test_buy_all_cart(self, product):
        cart = Cart()
        cart.add_product(product, 1000)
        cart.buy()
        assert product.quantity == 0
        assert len(cart.products) == 0

    def test_buy_empty_cart(self):
        cart = Cart()
        with pytest.raises(ValueError):
            cart.buy()

    def test_buy_cart_with_more_products_than_in_stock(self, product):
        cart = Cart()
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            cart.buy()
