"""Category API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("", response_model=list[schemas.CategoryResponse])
def list_categories(
    db: Annotated[Session, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return crud.get_categories(db=db, page=page, limit=limit)


@router.post(
    "",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category: schemas.CategoryCreate,
    db: Annotated[Session, Depends(get_db)],
):
    existing_category = crud.get_category_by_name(db, category.name)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists",
        )

    return crud.create_category(db=db, category=category)


@router.get("/{id}", response_model=schemas.CategoryResponse)
def get_category(
    id: int,
    db: Annotated[Session, Depends(get_db)],
):
    category = crud.get_category(db=db, category_id=id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return category


@router.put("/{id}", response_model=schemas.CategoryResponse)
def update_category(
    id: int,
    category_update: schemas.CategoryUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    category = crud.get_category(db=db, category_id=id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    if category_update.name:
        existing_category = crud.get_category_by_name(db, category_update.name)
        if existing_category and existing_category.id != id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with this name already exists",
            )

    return crud.update_category(
        db=db,
        db_category=category,
        category=category_update,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    id: int,
    db: Annotated[Session, Depends(get_db)],
):
    category = crud.get_category(db=db, category_id=id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    crud.delete_category(db=db, db_category=category)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
