""" File to define endpoints for setup the application
"""

from core.models import (
    ToolingType,
    RequestType,
    ProductType,
    Client,
    DateCF,
    DateBP,
    Tooling
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
    {"desc": "03", "date_exp": date(2024, 3, 30), "bp": 1},
    {"desc": "05", "date_exp": date(2024, 5, 30), "bp": 1},
    {"desc": "07", "date_exp": date(2024, 7, 30), "bp": 1},
    {"desc": "03", "date_exp": date(2024, 3, 30), "bp": 2},
    {"desc": "05", "date_exp": date(2024, 5, 30), "bp": 2},
    {"desc": "07", "date_exp": date(2024, 7, 30), "bp": 2},
]

dateBPs = [
    {"desc": "24", "date_exp": date(2024, 3, 30)},
    {"desc": "25", "date_exp": date(2025, 9, 22)},
]

toolings = [
    {
        "project": "coldStart",
        "client_supplier": 1,
        "part_number": "511",
        "price": 10000,
        "request_type": 1,
        "product_type": 1,
        "tooling_type": 1,
        "date_input": date(2024, 3, 30),
        "date_request": date(2024, 7, 30),
        "date_sop": date(2025, 7, 30),
        "was_approved": True,
        "bp_id": 1,
        "cf_id": 1,
        "requested_by": "Douglas",
        "RBSNO": "fa44c211-7171-5a38-b874-4e9bfd34ee9e",
    }
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
        obj = DateCF(desc=item["desc"], date_exp=item["date_exp"], bp=item["bp"])
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


def add_toolings():
    db = SessionLocal()
    for item in toolings:
        print(item["project"] + "\t\t added")
        obj = Tooling(
            project=item["project"],
            client_supplier=item["client_supplier"],
            part_number=item["part_number"],
            price=item["price"],
            request_type=item["request_type"],
            product_type=item["product_type"],
            tooling_type=item["tooling_type"],
            date_input=item["date_input"],
            date_request=item["date_request"],
            date_sop=item["date_sop"],
            was_approved=item["was_approved"],
            bp_id=item["bp_id"],
            cf_id=item["cf_id"],
            requested_by=item["requested_by"],
            RBSNO=item["RBSNO"],
        )
        db.add(obj)
    db.commit()
    db.refresh(obj)


if __name__ == "__main__":
    add_toolingTypes()
    add_productTypes()
    add_requestTypes()
    add_clients()
    add_dateBPs()
    add_dateCFs()
    add_toolings()
