from sqlalchemy import Column, Integer, String, Double, ForeignKey, Date, Boolean
from core.database import Base
from sqlalchemy.orm import relationship

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
    request = relationship("RequestType", back_populates="tooling")

    # drop box: Gallery injection, Product Area  Ignition, Product Area Fuel Supply Module, ...
    product_type = Column(ForeignKey("productType.id"))
    product = relationship("ProductType", back_populates="tooling")

    # Ferramental de estampo, Molde de injeção plástica, Molde de injeção de alumínio,....
    tooling_type = Column(ForeignKey("toolingType.id"))
    tooling_t = relationship("ToolingType", back_populates="tooling")

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
    
    history = relationship("ToolingUpdates", back_populates="tooling")

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
    request = relationship("RequestType", back_populates="tooling_update")
    
    product_type = Column(ForeignKey("productType.id"))
    product = relationship("ProductType", back_populates="tooling_update")
    
    tooling_type = Column(ForeignKey("toolingType.id"))
    tooling_t = relationship("ToolingType", back_populates="tooling_update")
    
    date_input = Column(Date)
    date_request = Column(Date)
    date_sop = Column(Date)
    RBSNO = Column(String, nullable=True)
    
    tooling = relationship("Tooling", back_populates="history")


# ICT / RRP / TLM / ...
class RequestType(Base):
    __tablename__ = "requestType"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)

    tooling_update = relationship("ToolingUpdates", back_populates="request")
    tooling = relationship("Tooling", back_populates="request")

# Ferramental de estampo, Molde de injeção plástica, Molde de injeção de alumínio,....
class ToolingType(Base):
    __tablename__ = "toolingType"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)

    tooling_update = relationship("ToolingUpdates", back_populates="tooling_t")
    tooling = relationship("Tooling", back_populates="tooling_t")
    

# drop box: Gallery injection, Product Area  Ignition, Product Area Fuel Supply Module, ...
class ProductType(Base):
    __tablename__ = "productType"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String)
    cost_center = Column(String)

    tooling_update = relationship("ToolingUpdates", back_populates="product")
    tooling = relationship("Tooling", back_populates="product")
    

# Client table to prevent same client with different spellings
class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
