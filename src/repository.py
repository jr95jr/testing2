import sqlite3
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Vehicle:
    id: int
    brand: str
    model: str
    year: int

class VehicleRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self._init_schema()

    def _init_schema(self) -> None:
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL
        )
        """)
        self.conn.commit()

    def add(self, brand: str, model: str, year: int) -> int:
        cur = self.conn.execute(
            "INSERT INTO vehicles(brand, model, year) VALUES (?, ?, ?)",
            (brand, model, year),
        )
        self.conn.commit()
        return cur.lastrowid

    def get(self, vid: int) -> Optional[Vehicle]:
        cur = self.conn.execute("SELECT id, brand, model, year FROM vehicles WHERE id = ?", (vid,))
        row = cur.fetchone()
        if row:
            return Vehicle(*row)
        return None

    def list(self) -> List[Vehicle]:
        cur = self.conn.execute("SELECT id, brand, model, year FROM vehicles ORDER BY id")
        return [Vehicle(*row) for row in cur.fetchall()]