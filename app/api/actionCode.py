from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.actionCode import ActionCode
from app.crud.actionCode import get_action_code, create_action_code

router = APIRouter(prefix="/action-code", tags=["action-code"])

@router.get("/{CodeID}", response_model=ActionCode)
async def get_action_code_by_id(CodeID: int, db: Session = Depends(get_db)):
    action_code = await get_action_code(db, CodeID)
    if action_code is None:
        raise HTTPException(status_code=404, detail="Action code not found")
    return action_code

@router.post("/", response_model=ActionCode)
async def create_new_action_code(action_code: ActionCode, db: Session = Depends(get_db)):
    return await create_action_code(db, action_code)