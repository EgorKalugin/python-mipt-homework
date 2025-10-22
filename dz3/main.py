from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from _typeshed import ConvertibleToFloat, ConvertibleToInt


class Product:
    def __init__(
        self: Self, name: Any, price: ConvertibleToFloat, stock: ConvertibleToInt
    ) -> None:
        self.name = str(name)
        price = float(price)
        if price < 0:
            raise ValueError("Price cant be negative.")
        self.price = price

        stock = int(stock)
        if stock < 0:
            raise ValueError("Stock cant be negative.")
        self.stock = int(stock)

    def update_stock(self, quantity: ConvertibleToInt) -> None:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Qantity cant be negative.")
        self.stock = quantity


class Order:
    def __init__(self) -> None:
        self.products: dict[Product, int] = {}

    def add_product(self, product: Product, quantity: ConvertibleToInt) -> None:
        quantity = int(quantity)
        if product.stock < quantity:
            raise ValueError("Quantity cant be more then product stock.")
        self.products[product] = quantity

    def calculate_total(self) -> float:
        total = 0.0
        for product, quantity in self.products.items():
            total += quantity * product.price
        return total

    def remove_order(self, product: Product, quantity: ConvertibleToInt) -> int:
        quantity = int(quantity)
        current_quantity = self.products[product]
        new_quantity = current_quantity - quantity

        if new_quantity <= 0:
            del self.products[product]
        else:
            self.products[product] = new_quantity

        return min(current_quantity, quantity)

    def return_product(self, product: Product, quantity: ConvertibleToInt) -> None:
        product.update_stock(self.remove_order(product, quantity))


class Store:
    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def list_products(self):
        for product in self.products:
            print(f"{product.name}: price: {product.price}, stock: {product.stock}")

    def create_order(self) -> Order:
        return Order()


if __name__ == "__main__":
    # Создаем магазин
    store = Store()

    # Создаем товары
    product1 = Product("Ноутбук", 1000, 5)
    product2 = Product("Смартфон", 500, 10)

    # Добавляем товары в магазин
    store.add_product(product1)
    store.add_product(product2)

    # Список всех товаров
    store.list_products()

    # Создаем заказ
    order = store.create_order()

    # Добавляем товары в заказ
    order.add_product(product1, 2)
    order.add_product(product2, 3)

    # Выводим общую стоимость заказа
    total = order.calculate_total()
    print(f"Общая стоимость заказа: {total}")

    # Проверяем остатки на складе после заказа
    store.list_products()
