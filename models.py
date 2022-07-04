from typing import NamedTuple

class Product(NamedTuple):
    '''Базовый класс для продукта'''
    name: str
    serial: str
    warranty: str
    price: str

    def __repr__(self) -> str:
        return f"{self.name}#{self.serial}#{self.warranty}#{self.price}"
