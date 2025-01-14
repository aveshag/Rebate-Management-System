import logging

from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound

from src.db.db_session_manager import DBSessionManager

logger = logging.getLogger(__name__)


class GenericDAO:
    def __init__(self, model):
        self.db = DBSessionManager()
        self.model = model

    async def get_all(self):
        """
        Retrieve all rows for the model.
        """
        try:
            async with self.db.get_session_context() as session:
                result = await session.execute(select(self.model))
                session.expunge_all()
                return result.scalars().all()
        except Exception as e:
            logger.error(f"Error retrieving all records: {e}")
            raise e

    async def get_by_column_value(self, column_name, value):
        """
        Retrieve a single row by any column's value.
        :param column_name: The name of the column to filter by.
        :param value: The value of the column to search for.
        """
        try:
            async with self.db.get_session_context() as session:
                column = getattr(self.model, column_name)
                result = await session.execute(
                    select(self.model).where(column == value))
                session.expunge_all()
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error retrieving a record: {e}")
            raise e

    async def create(self, data):
        """
        Insert a new row into the database.
        :param data: A dictionary of model columns and their values.
        """
        try:
            async with self.db.get_session_context() as session:
                new_record = self.model(**data)
                session.add(new_record)
        except Exception as e:
            logger.error(f"Error creating record: {e}")
            raise e

    async def update(self, id_, data):
        """
        Update an existing record by its primary key.
        :param id_: The primary key of the record to update.
        :param data: A dictionary of model columns and their new values.
        """
        try:
            async with self.db.get_session_context() as session:
                record = await session.get(self.model, id_)
                if not record:
                    raise NoResultFound(f"No record found for ID: {id_}")

                for key, value in data.items():
                    setattr(record, key, value)

                session.commit()
                session.expunge_all()
                return record
        except Exception as e:
            logger.error(f"Error updating record: {e}")

    async def update_by_column(self, column_name, column_value, data):
        """
        Update an existing record by any column's value.
        :param column_name: The name of the column to filter by.
        :param column_value: The value of the column to find the record.
        :param data: A dictionary of model columns and their new values.
        """
        try:
            async with self.db.get_session_context() as session:
                column = getattr(self.model, column_name)
                result = await session.execute(
                    select(self.model).where(column == column_value))
                record = result.scalar_one_or_none()

                if not record:
                    raise NoResultFound(
                        f"No record found for {column_name} = {column_value}")

                for key, value in data.items():
                    setattr(record, key, value)
                session.commit()
                session.expunge_all()
                return record
        except Exception as e:
            logger.error(f"Error updating record: {e}")
            raise e

    async def delete(self, id_):
        """
        Delete an existing record by its primary key without checking for its existence.
        :param id_: The primary key of the record to delete.
        """
        try:
            async with self.db.get_session_context() as session:
                # Attempt to delete directly
                await session.execute(
                    self.model.__table__.delete().where(
                        self.model.__table__.c.id == id_)
                )
                await session.commit()
                return True
        except Exception as e:
            logger.error(
                f"Error deleting record with ID: {id_}: {e}")
            return False
