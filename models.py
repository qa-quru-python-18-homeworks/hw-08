class Product:
    """
    Класс продукта
    """

    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, requested_quantity) -> bool:
        """
        Метод проверки количества продуктов на складе.
        Возвращает True, если количество продуктов больше или равно запрашиваемому
        и False в обратном случае
        """
        if requested_quantity < 0:
            raise ValueError(f"Запрашиваемое количество ({requested_quantity}) не может быть отрицательным")
        return self.quantity >= requested_quantity

    def buy(self, requested_quantity):
        """
        Метод покупки. Вычитает запрашиваемое количество продуктов из общего количества.
        Если запрашиваемое количество продуктов больше общего, то выбрасывает исключение ValueError
        """
        if self.check_quantity(requested_quantity):
            self.quantity -= requested_quantity
        else:
            raise ValueError(
                f"Запрашиваемое количество ({requested_quantity}) больше, чем есть в наличии ({self.quantity})"
            )

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if buy_count <= 0:
            raise ValueError(
                f"Добавляемое количество товара ({buy_count}) не может быть меньше или равно нулю"
            )

        # Если продукта нет в корзине, то при получении его количества вернется 0
        self.products[product] = self.products.get(product, 0) + buy_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        # Проверка наличия продукта в корзине
        if product not in self.products:
            raise ValueError(f"Продукт ({product.name}) отсутствует в корзине")

        # Проверка, что если remove_count указан, он не отрицательный
        if remove_count is not None and remove_count <= 0:
            raise ValueError(f"Удаляемое количество ({remove_count}) не может быть меньше или равно нулю")

        current_count = self.products[product]
        # Если не указан remove_count или его значение больше или равно текущему количеству, удаляем всю позицию
        if remove_count is None or remove_count >= current_count:
            self.products.pop(product)
        else:
            self.products[product] = current_count - remove_count

    def clear(self):
        """
        Метод очистки корзины
        """
        self.products.clear()

    def get_total_price(self) -> float:
        """
        Метод расчета общей стоимости всех продуктов в корзине
        Возвращает общую стоимость
        """
        return sum(
            product.price * quantity for product, quantity in self.products.items()
        )

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        if len(self.products) == 0:
            raise ValueError("Корзина пуста")

        for product, requested_quantity in list(self.products.items()):
            # Если товара не хватает, то в buy будет ValueError
            product.buy(requested_quantity)
        self.clear()  # Очищаем всю корзину после покупки
