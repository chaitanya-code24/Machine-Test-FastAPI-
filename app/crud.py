"""Database CRUD helpers."""

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app import models, schemas


def get_pagination_offset(page: int, limit: int) -> int:
    return (page - 1) * limit


def get_categories(db: Session, page: int = 1, limit: int = 10) -> list[models.Category]:
    offset = get_pagination_offset(page, limit)
    statement = (
        select(models.Category)
        .order_by(models.Category.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def get_category(db: Session, category_id: int) -> models.Category | None:
    return db.get(models.Category, category_id)


def get_category_by_name(db: Session, name: str) -> models.Category | None:
    statement = select(models.Category).where(models.Category.name == name)
    return db.scalar(statement)


def create_category(
    db: Session,
    category: schemas.CategoryCreate,
) -> models.Category:
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session,
    db_category: models.Category,
    category: schemas.CategoryUpdate,
) -> models.Category:
    category_data = category.model_dump(exclude_unset=True)
    for field, value in category_data.items():
        setattr(db_category, field, value)

    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, db_category: models.Category) -> None:
    db.delete(db_category)
    db.commit()


def get_products(db: Session, page: int = 1, limit: int = 10) -> list[models.Product]:
    offset = get_pagination_offset(page, limit)
    statement = (
        select(models.Product)
        .options(joinedload(models.Product.category))
        .order_by(models.Product.id)
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


def get_product(db: Session, product_id: int) -> models.Product | None:
    statement = (
        select(models.Product)
        .options(joinedload(models.Product.category))
        .where(models.Product.id == product_id)
    )
    return db.scalar(statement)


def create_product(
    db: Session,
    product: schemas.ProductCreate,
) -> models.Product:
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return get_product(db, db_product.id) or db_product


def update_product(
    db: Session,
    db_product: models.Product,
    product: schemas.ProductUpdate,
) -> models.Product:
    product_data = product.model_dump(exclude_unset=True)
    for field, value in product_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return get_product(db, db_product.id) or db_product


def delete_product(db: Session, db_product: models.Product) -> None:
    db.delete(db_product)
    db.commit()
