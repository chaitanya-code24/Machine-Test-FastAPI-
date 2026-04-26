"""Product API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=list[schemas.ProductResponse])
def list_products(
    db: Annotated[Session, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return crud.get_products(db=db, page=page, limit=limit)


@router.post(
    "",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: schemas.ProductCreate,
    db: Annotated[Session, Depends(get_db)],
):
    category = crud.get_category(db=db, category_id=product.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    return crud.create_product(db=db, product=product)


@router.get("/{id}", response_model=schemas.ProductResponse)
def get_product(
    id: int,
    db: Annotated[Session, Depends(get_db)],
):
    product = crud.get_product(db=db, product_id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.put("/{id}", response_model=schemas.ProductResponse)
def update_product(
    id: int,
    product_update: schemas.ProductUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    product = crud.get_product(db=db, product_id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    if product_update.category_id is not None:
        category = crud.get_category(db=db, category_id=product_update.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

    return crud.update_product(db=db, db_product=product, product=product_update)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    id: int,
    db: Annotated[Session, Depends(get_db)],
):
    product = crud.get_product(db=db, product_id=id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    crud.delete_product(db=db, db_product=product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
