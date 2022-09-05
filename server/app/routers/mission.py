from typing import Union
from fastapi import APIRouter, Depends, Query, status, HTTPException
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..schemas.mission import BaseMissionSchema, MissionDeletion, MissionSchema
from ..schemas.base import Page, Params
from ..dependencies import get_db
from ..models.metadata import MissionDetails
from ..internal.logging import get_logger
from ..constants import DEFAULT_PAGE_LEN
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination

logger = get_logger(__name__)
router = APIRouter(
    prefix="/mission",
    tags=["mission"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=MissionSchema, status_code=status.HTTP_201_CREATED)
async def add_mission(mission: BaseMissionSchema, db: Session = Depends(get_db)):
    try:
        mission_db = MissionDetails(**mission.dict())
        db.add(mission_db)
        db.commit()
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The following mission already exists: {mission.mission_alias}",
        )
    except Exception as err:
        logger.exception("Exception detected!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
    return MissionSchema.from_orm(mission_db)


@router.patch(
    "/<mission_id>", response_model=MissionSchema, status_code=status.HTTP_200_OK
)
async def update_mission(
    mission_id: int, mission_to_update: BaseMissionSchema, db: Session = Depends(get_db)
):
    stored_mission = db.query(MissionDetails).filter_by(mission_id=mission_id).first()
    if stored_mission:
        try:
            stored_mission_model = MissionSchema.from_orm(stored_mission)
            update_data = mission_to_update.dict(exclude_unset=True)
            updated_mission = stored_mission_model.copy(update=update_data)
            db.query(MissionDetails).filter_by(mission_id=mission_id).update(
                update_data
            )
            db.commit()
            return updated_mission.to_json()
        except Exception as e:
            logger.exception(f"Exception detected: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The following mission does not exists: {stored_mission.mission_alias}",
        )


@router.get("", response_model=Page[MissionSchema], status_code=status.HTTP_200_OK)
async def retrieve_mission(
    mission_alias: Union[str, None] = Query(default=None),
    page: Union[int, None] = Query(default=1),
    size: Union[int, None] = Query(default=DEFAULT_PAGE_LEN),
    db: Session = Depends(get_db),
):
    if mission_alias is not None:
        missions = db.query(MissionDetails).filter_by(mission_alias=mission_alias)
    else:
        missions = db.query(MissionDetails)
    return paginate(missions, Params(page=page, size=size, path="/mission"))


@router.delete(
    "/<mission_id>", response_model=MissionDeletion, status_code=status.HTTP_200_OK
)
async def delete_mission(
    mission_id: Union[str, None] = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        mission = db.query(MissionDetails).filter_by(mission_id=mission_id)
        if mission is None:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The following mission does not exists, ID -> {mission_id}",
            )
        mission.delete()
        db.commit()
    except Exception as e:
        logger.exception(f"Exception detected: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return MissionDeletion(msg="Deleted", mission_id=mission_id).to_json()


add_pagination(router)
