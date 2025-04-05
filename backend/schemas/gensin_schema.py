# from typing import Optional

from pydantic import Field

from .base_schema import BaseModel


class Person(BaseModel):
    id: int
    name: str
    attribute_id: int
    belong_id: int


class Attribute(BaseModel):
    id: int
    attribute_name: str


class Belong(BaseModel):
    id: int
    belong: str


class Country(BaseModel):
    id: int
    country_name: str


class CreateCountrySchema(BaseModel):
    country_name: str


class CreateBelongSchema(BaseModel):
    belong: str
    country_id: int


class CreateAttributeSchema(BaseModel):
    attribute_name: str


class CreateGensinSchema(BaseModel):
    name: str = Field(..., main_length=1, max_length=128)
    attribute_id: int
    belong_id: int


class DeleteGensin(BaseModel):
    name: str


class UpdateGensinSchema(BaseModel):
    name: str | None = Field(..., main_length=1, max_length=128)


class ShowGensinSchema(BaseModel):
    name: str


class ShowAttribute(BaseModel):
    attribute_name: str


class ShowCountry(BaseModel):
    country_name: str


class ShowBelong(BaseModel):
    belong: str
    country: ShowCountry


class ShowPerson(BaseModel):
    id: int
    name: str
    attributes: ShowAttribute
    belongs: ShowBelong
