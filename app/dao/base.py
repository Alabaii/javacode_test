from datetime import datetime
from uuid import UUID
from fastapi import HTTPException,status
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
# from app.logger import logger

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, id: str):
        try:
            # Пытаемся преобразовать строку в UUID
            uuid_obj = UUID(id)
        except ValueError:
            # Если UUID некорректен, возвращаем ошибку 400
            logger.error(f"Некорректный UUID: {id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Некорректный UUID: {id}"
            )

        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.id == uuid_obj))
            entity = result.scalar_one_or_none()
            
            if entity is None:
                logger.error(f"Объект с id={id} не найден в таблице {cls.model.__tablename__}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Объект с id={id} не найден"
                )
            
            return entity
    
