"""calculator.py
Módulo simple para demostrar pruebas unitarias.
"""
from typing import List, Optional

def add(a: float, b: float) -> float:
    return a + b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("No se puede dividir entre cero")
    return a / b

def mean(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)

def power(a: float, b) -> float:
    """Potencia a**b (b puede ser entero o float)."""
    return a ** b