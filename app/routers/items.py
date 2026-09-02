from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Item

# Inline Pydantic Schemas (previously in schemas.py)
class ItemBase(BaseModel):
    title: str = Field(..., example="Build a FastAPI service")
    description: Optional[str] = Field(None, example="Clean architecture with Pydantic")
    completed: bool = False

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return None