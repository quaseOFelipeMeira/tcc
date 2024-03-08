from sqlalchemy import Column, Integer, String, Double, ForeignKey, Date, Boolean
from core.database import Base


class Tooling(Base):
    __tablename__ = "toolings"
    id = Column(Integer, primary_key=True, index=True)

    # ==== description of the tooling ==================

    # Project name
    project = Column(String, nullable=True)  # null if RPP
    # Client if is ICT / Supplier if is RPP
    # client_supplier = Column(String, nullable=True)
    client_supplier = Column(ForeignKey("client.id"), nullable=True)
    # part_number (opcional)
    part_number = Column(String, nullable=True)  # part number for the component

    # ==================================================

    # Price in BRL
    price = Column(Double)

    # ICT / RRP / TLM / ...
    request_type = Column(ForeignKey("requestType.id"))

    # drop box: Gallery injection, Product Area  Ignition, Product Area Fuel Supply Module, ...
    product_type = Column(ForeignKey("productType.id"))

    # Ferramental de estampo, Molde de injeção plástica, Molde de injeção de alumínio,....
    tooling_type = Column(ForeignKey("toolingType.id"))

    # Current date for the request
    date_input = Column(Date)

    # Date for start the process of buying the tooling
    date_request = Column(Date)

    # Date for use this tolling
    date_sop = Column(Date)

    # Status if the request was approved: Yes - true / null - not yet / No - refused
    was_approved = Column(Boolean, nullable=True)

    # Period of the approval - "BP24" / "BP24CF02" or "CF02"
    status_description = Column(String, nullable=True)

    # ID from the user that requested the request
    requested_by = Column(String)

    # Robert Bosch Supplier Number
    RBSNO = Column(String, nullable=True)


class ToolingUpdates(Base):
    __tablename__ = "toolingUpdates"
    id = Column(Integer, primary_key=True, index=True)
    # column to identify the tooling:
    tooling_fk = Column(ForeignKey("toolings.id"))
    # info previously saved
    project = Column(String, nullable=True)  # null if RPP
    client_supplier = Column(ForeignKey("client.id"), nullable=True)
    part_number = Column(String, nullable=True)  # part number for the component
    price = Column(Double)
    request_type = Column(ForeignKey("requestType.id"))
    product_type = Column(ForeignKey("productType.id"))
    tooling_type = Column(ForeignKey("toolingType.id"))
    date_input = Column(Date)
    date_request = Column(Date)
    date_sop = Column(Date)


# ICT / RRP / TLM / ...
class RequestType(Base):
    __tablename__ = "requestType"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)


# Ferramental de estampo, Molde de injeção plástica, Molde de injeção de alumínio,....
class ToolingType(Base):
    __tablename__ = "toolingType"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)


# drop box: Gallery injection, Product Area  Ignition, Product Area Fuel Supply Module, ...
class ProductType(Base):
    __tablename__ = "productType"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)
    cost_center = Column(String)


# Client table to prevent same client with different spellings
class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
