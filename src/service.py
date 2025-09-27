import sqlite3
from typing import List
from .repository import VehicleRepository, Vehicle

class VehicleService:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.repo = VehicleRepository(conn)

    def register_vehicle(self, brand: str, model: str, year: int) -> int:
        if year < 1886:
            raise ValueError("El año debe ser 1886 o mayor")
        if not brand or not model:
            raise ValueError("Marca y modelo son obligatorios")
        return self.repo.add(brand.strip(), model.strip(), int(year))

    def inventory(self) -> List[Vehicle]:
        return self.repo.list()