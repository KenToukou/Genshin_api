import os
from datetime import datetime
from typing import Literal, Optional

import sqlalchemy
from const import env

# from core.context_vars import get_current_user
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


def get_db_url() -> Optional[str]:
    DB_URL: Optional[str] = os.getenv("DB_URL")
    print("DB_URL :", DB_URL)
    return DB_URL


class Engines(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Engines, cls).__new__(cls)
        return cls._instance


def get_engine():
    # 詳細設定のところがミスってた。
    DB_URL = get_db_url()
    new_engine = sqlalchemy.create_engine(
        DB_URL.format(user=env.user, password=env.password, gensin_db=env.db_name),
        echo=True,
    )
    return new_engine


def get_session_factory(db_type: Literal["gensin"]):
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=get_engine())
    return session_factory


Base = declarative_base()


# class SoftDeleteMixin:
#     delete_at = Column(DateTime, nullable=False)

#     def soft_delete(self, delete_at: datetime | None = None):
#         self.delete_at = delete_at or datetime.now()

#     def restore(self):
#         self.delete_at = None


class CreateUpdateMetaMixin:
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    # @staticmethod
    # def get_update_user(model, session, target):
    #     current_user = get_current_user()
    #     target.uppdate_user = (
    #         current_user if current_user != "gensin" else target.uppdate_user
    #     )

    @classmethod
    def __declare_last__(cls):
        pass
        # event.listen(cls, "before_update")
        # event.listen(cls, "before_insert")


# @event.listens_for(Session,"do_orm_execute")
# def _do_orm_execute(orm_execute_state: Any):
