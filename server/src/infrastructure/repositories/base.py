from typing import Any, List, Tuple, Type, Union

from domain.types import ID_Type, T_Model
from infrastructure.db.orm import BaseModel
from pydantic import BaseModel as BaseEntity
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.common.exceptions.db import DataToORMSerializationException, DBException, DuplicatedKeyError


class BaseRepository:
    _model: BaseModel = BaseModel
    _entity: Type[T_Model] = BaseEntity

    def upsert(self, session: Session, data: T_Model) -> T_Model:
        model_data = self._schema_to_model(data, self._model)
        try:
            model_data = session.merge(model_data)
            session.commit()
            return self._entity.from_orm(model_data)
        except IntegrityError:
            session.rollback()
            raise DuplicatedKeyError(data.dict())
        except Exception as e:
            session.rollback()
            raise DBException(self._model, e) from e

    def get_by_id(self, session: Session, id: ID_Type) -> Union[T_Model, None]:
        try:
            model = session.query(self._model).filter_by(id=id).first()
            if model is None:
                return model
        except Exception as e:
            raise DBException(self._model, e) from e
        return self._entity.from_orm(model)

    def delete_by_id(self, session: Session, id: ID_Type) -> None:
        try:
            session.query(self._model).filter_by(id=id).delete()
        except Exception as e:
            raise DBException(self._model, e) from e

    def get_with_pagination(
        self, session: Session, page: int, size: int, query_filters: Any = None
    ) -> Tuple[int, List[BaseModel]]:
        if query_filters is not None:
            query = session.query(self._model).filter(query_filters)
        else:
            query = session.query(self._model)
        total = query.count()
        if total == 0:
            return 0, []
        result = query.limit(size).offset((page - 1) * size).all()
        return total, [self._model_to_schema(r) for r in result]

    def _get_by_filters(self, session: Session, filters: dict, mode: str = "all") -> List[T_Model]:
        if mode not in ["all", "first"]:
            raise ValueError("mode should be all or first")
        try:
            if mode == "all":
                return session.query(self._model).filter_by(**filters).all()
            elif mode == "first":
                return session.query(self._model).filter_by(**filters).first()
        except Exception as e:
            raise DBException(self._model, e) from e

    def _schema_to_model(self, data: T_Model, model: BaseModel) -> BaseModel:
        try:
            model_data = model(**data.dict())
        except ValueError as e:
            raise DataToORMSerializationException(f"Unable to serialize {self._model=} from {data=}") from e
        return model_data

    def _model_to_schema(self, model_data: BaseModel) -> T_Model:
        return self._entity.from_orm(model_data)