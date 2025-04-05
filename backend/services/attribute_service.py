from fastapi import HTTPException, status
from models import Attribute
from repositories import AttributeRepository
from schemas.gensin_schema import CreateAttributeSchema


class AttributeService:
    def __init__(self, attribute_repository: AttributeRepository) -> None:
        self._attribute_repo = attribute_repository

    def is_duplicate_attribute(
        self,
        attribute: str,
    ) -> bool:
        is_duplicated = self._attribute_repo.is_duplicate_attribute(name=attribute)
        print("OK_10")
        if is_duplicated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return is_duplicated

    def get_attribute_all(self, skip: int = 0, limit: int = 100) -> list[Attribute]:
        return self._attribute_repo.get_all_attributes(skip=skip, limit=limit)

    def get_attribute_by_id(self, gensin_name: str) -> Attribute:
        return self._attribute_repo.get_attribute_id(attribute_name=gensin_name)

    def create_attribute(self, attribute: CreateAttributeSchema):
        print(attribute.dict())
        new_attribute = Attribute(attribute_name=attribute.attribute_name)
        return self._attribute_repo.create(new_attribute)
