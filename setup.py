""" File to define endpoints for setup the application
"""

from core.models import ToolingType, RequestType, ProductType, Client, DateCF, Tooling
from sqlalchemy.orm import Session
from datetime import date
from core.database import SessionLocal


toolingTypes = [
    {"desc": "Ferramental de estampo"},
    {"desc": "Molde de injeção plástica"},
    {"desc": "Molde de injeção de alumínio"},
]

requestTypes = [
    {"desc": "ICT"},
    {"desc": "RRP"},
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

toolings = [
    {
        "project": "string",
        "client": {
            "name": "Volkswagen",
        },
        "part_number": "12211823996",
        "RBSNO": "2441122404",
        "price": 33474.6,
        "product": {
            "desc": "Gallery injection",
            "cost_center": "AA",
        },
        "tooling_t": {
            "desc": "Ferramental de estampo",
        },
        "date_request": date(2024, 10, 21),
        "date_sop": date(2025, 2, 15),
    },
    {
        "project": "string",
        "client": {
            "name": "Fiat",
        },
        "part_number": "228139132207",
        "RBSNO": "160145192122",
        "price": 61918.52,
        "product": {
            "desc": "New Product",
            "cost_center": "DD",
        },
        "tooling_t": {
            "desc": "Molde de injeção de alumínio",
        },
        "date_request": date(2024, 4, 3),
        "date_sop": date(2024, 12, 28),
    }
]


def add_toolingTypes():
    db = SessionLocal()
    for item in toolingTypes:
        obj = ToolingType(desc=item["desc"])
        db.add(obj)
    db.commit()
    db.refresh(obj)


def add_requestTypes():
    db = SessionLocal()
    for item in requestTypes:
        obj = RequestType(desc=item["desc"])
        db.add(obj)
    db.commit()
    db.refresh(obj)


def add_productTypes():
    db = SessionLocal()
    for item in productTypes:
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
        obj = Client(
            name=item["name"],
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)


def add_dateCFs():
    db = SessionLocal()
    for item in dateCFs:
        obj = DateCF(
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
