""" File to define endpoints for setup the application
"""

from core.models import (
    ToolingType,
    RequestType,
    ProductType,
    Client,
    DateCF,
    DateBP,
)
from datetime import date
from core.database import SessionLocal


toolingTypes = [
    {"desc": "Ferramental de estampo"},
    {"desc": "Molde de injeção plástica"},
    {"desc": "Molde de injeção de alumínio"},
]

requestTypes = [
    {"desc": "ICT"},
    {"desc": "RPP"},
    {"desc": "TLM"},
]

productTypes = [
    {"desc": "Gallery injection", "cost_center": "AA"},
    {"desc": "Product Area  Ignition", "cost_center": "BB"},
    {"desc": "Product Area Fuel Supply Module", "cost_center": "CC"},
]

clients = [
    {"name": "Volkswagen"},
    {"name": "Fiat"},
    {"name": "Hyundai"},
]

dateCFs = [
    {"desc": "03", "date_exp": date(2024, 3, 30)},
    {"desc": "05", "date_exp": date(2024, 5, 30)},
    {"desc": "07", "date_exp": date(2024, 7, 30)},
]

dateBPs = [
    {"desc": "24", "date_exp": date(2024, 3, 30)},
    {"desc": "25", "date_exp": date(2025, 9, 22)},
]


def add_toolingTypes():
    db = SessionLocal()
    for item in toolingTypes:
        print(item["desc"] + "\t\t added")
        obj = ToolingType(desc=item["desc"])
        db.add(obj)
    db.commit()
    db.refresh(obj)


def add_requestTypes():
    db = SessionLocal()
    for item in requestTypes:
        print(item["desc"] + "\t\t added")
        obj = RequestType(desc=item["desc"])
        db.add(obj)
    db.commit()
    db.refresh(obj)


def add_productTypes():
    db = SessionLocal()
    for item in productTypes:
        print(item["desc"] + "\t\t added")
        obj = ProductType(
            desc=item["desc"],
            cost_center=item["cost_center"],
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)


def add_clients():
    db = SessionLocal()
    for item in clients:
        print(item["name"] + "\t\t added")
        obj = Client(
            name=item["name"],
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)


def add_dateCFs():
    db = SessionLocal()
    for item in dateCFs:
        print(item["desc"] + "\t\t added")
        obj = DateCF(
            desc=item["desc"],
            date_exp=item["date_exp"],
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)


def add_dateBPs():
    db = SessionLocal()
    for item in dateBPs:
        print(item["desc"] + "\t\t added")
        obj = DateBP(
            desc=item["desc"],
            date_exp=item["date_exp"],
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)


if __name__ == "__main__":
    add_toolingTypes()
    add_productTypes()
    add_requestTypes()
    add_clients()
    add_dateCFs()
    add_dateBPs()
