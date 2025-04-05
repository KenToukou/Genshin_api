from core.database import Base, CreateUpdateMetaMixin, get_engine
from schemas.gensin_schema import CreateGensinSchema, UpdateGensinSchema
from sqlalchemy import Column, ForeignKey, Integer, String

# from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


# CreateUpdateMetaMixin
class Person(CreateUpdateMetaMixin, Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True)
    attribute_id = Column(Integer, ForeignKey("attributes.id"))
    attributes = relationship("Attribute", back_populates="persons")
    belong_id = Column(Integer, ForeignKey("belongs.id"))
    belongs = relationship("Belong", back_populates="persons")

    # , cascade="all, delete" : これに紐付いてる親のテーブルもろとも消し去る。

    # @hybrid_property
    # def belong(self):
    #     for _belong in self.belongs:
    #         if _belong.belong == "稲妻幕府":
    #             return _belong
    #     return None

    @classmethod
    def create(cls, chara: CreateGensinSchema) -> "Person":
        create_data = chara.dict(exclude_unset=True)
        new_chara = cls(
            **create_data,
        )
        return new_chara

    def update(self, chara: UpdateGensinSchema) -> None:
        update_data = chara.dict(exclude_unset=True)
        for key, val in update_data.items():
            setattr(self, key, val)

    def get_attribute(self):
        if self.attributes:
            return self.attributes.attribute_name

    def get_belong(self):
        if self.belongs:
            return self.belongs.belong

    def get_country(self):
        if self.belongs:
            return self.belongs.country.country_name


class Attribute(CreateUpdateMetaMixin, Base):
    __tablename__ = "attributes"
    id = Column(Integer, autoincrement=True, primary_key=True)
    attribute_name = Column(String(128), unique=True)
    persons = relationship("Person", back_populates="attributes")


class Belong(CreateUpdateMetaMixin, Base):
    __tablename__ = "belongs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    belong = Column(String(128), unique=True)
    country = relationship("Country", back_populates="belongs")
    country_id = Column(Integer, ForeignKey("countries.id"))
    persons = relationship("Person", back_populates="belongs")


class Country(CreateUpdateMetaMixin, Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String(128))
    belongs = relationship("Belong", back_populates="country")


Base.metadata.create_all(get_engine())
