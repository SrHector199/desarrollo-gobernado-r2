from __future__ import annotations


def split_expense(amount_cents: int, people: int) -> list[int]:
    if type(amount_cents) is not int or amount_cents < 0:
        raise ValueError("amount_cents debe ser un entero no negativo")
    if type(people) is not int or people <= 0:
        raise ValueError("people debe ser un entero mayor que cero")

    base, remainder = divmod(amount_cents, people)
    return [base + 1] * remainder + [base] * (people - remainder)
