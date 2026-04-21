from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.actionCode import actionCode
from app.crud.actionCode import get_action_Code, create_actionCode, update_actionCode, delete_actionCode

router = APIRouter(prefix="/action-code", tags=["action-code"])

@router.get("/{CodeID}", response_model=actionCode)
async def get_action_code_by_id(CodeID: int, db: Session = Depends(get_db)):
    action_code = await get_action_Code(db, CodeID)
    if action_code is None:
        raise HTTPException(status_code=404, detail="Action code not found")
    return action_code

@router.post("/", response_model=actionCode)
async def create_new_action_code(action_code: actionCode, db: Session = Depends(get_db)):
    return await create_actionCode(db, action_code)

@router.put("/{CodeID}", response_model=actionCode)
async def update_action_code_by_id(CodeID: int, action_code: actionCode, db: Session = Depends(get_db)):
    return await update_actionCode(db, CodeID, action_code)

@router.delete("/{CodeID}")
async def delete_action_code_by_id(CodeID: int, db: Session = Depends(get_db)):
    return await delete_actionCode(db, CodeID)