"""Product API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import get_async_session
from ..models import Product, ProductAlias
from ..schemas.products import (
    Product as ProductSchema,
)
from ..schemas.products import (
    ProductCreate,
    ProductSearchResult,
    ProductUpdate,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/search", response_model=ProductSearchResult)
async def search_products(
    q: str = Query(..., min_length=1, description="Search query"),
    game: str | None = Query(None, description="Filter by game"),
    category: str | None = Query(None, description="Filter by category"),
    set_name: str | None = Query(None, description="Filter by set name"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    session: AsyncSession = Depends(get_async_session),
) -> ProductSearchResult:
    """
    Search products with optimized performance (<10ms target).

    Uses PostgreSQL full-text search with GIN indexes for fast results.
    """
    # Calculate offset for pagination
    offset = (page - 1) * per_page

    # Build base query with full-text search
    query = select(Product).options(selectinload(Product.aliases))

    # Full-text search across product name, set_name, and variant
    search_conditions = []

    # Primary search on product fields
    search_conditions.append(
        func.to_tsvector(
            "english",
            func.coalesce(Product.name, "")
            + " "
            + func.coalesce(Product.set_name, "")
            + " "
            + func.coalesce(Product.variant, ""),
        ).match(q),
    )

    # Search aliases with subquery for high performance
    alias_subquery = select(ProductAlias.product_id).where(
        func.to_tsvector("english", ProductAlias.alias).match(q),
    )
    search_conditions.append(Product.id.in_(alias_subquery))

    # Combine search conditions with OR
    query = query.where(or_(*search_conditions))

    # Apply filters
    if game:
        query = query.where(Product.game.ilike(f"%{game}%"))
    if category:
        query = query.where(Product.category.ilike(f"%{category}%"))
    if set_name:
        query = query.where(Product.set_name.ilike(f"%{set_name}%"))

    # Count total results for pagination
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await session.execute(count_query)
    total = total_result.scalar() or 0

    # Apply pagination and ordering
    query = query.order_by(Product.name).offset(offset).limit(per_page)

    # Execute search query
    result = await session.execute(query)
    products = result.scalars().all()

    # Calculate pagination info
    has_next = offset + per_page < total
    has_prev = page > 1

    return ProductSearchResult(
        products=products,
        total=total,
        page=page,
        per_page=per_page,
        has_next=has_next,
        has_prev=has_prev,
    )


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: UUID,
    session: AsyncSession = Depends(get_async_session),
) -> ProductSchema:
    """Get a specific product by ID."""
    query = (
        select(Product)
        .options(selectinload(Product.aliases))
        .where(Product.id == product_id)
    )
    result = await session.execute(query)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )

    return product


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_async_session),
) -> ProductSchema:
    """Create a new product."""
    # Create product
    product = Product(**product_data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)

    # Load with aliases
    query = (
        select(Product)
        .options(selectinload(Product.aliases))
        .where(Product.id == product.id)
    )
    result = await session.execute(query)
    product = result.scalar_one()

    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> ProductSchema:
    """Update an existing product."""
    # Find product
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )

    # Update product
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    await session.commit()
    await session.refresh(product)

    # Load with aliases
    query = (
        select(Product)
        .options(selectinload(Product.aliases))
        .where(Product.id == product_id)
    )
    result = await session.execute(query)
    product = result.scalar_one()

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Delete a product."""
    # Find product
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )

    # Delete product (aliases will be deleted automatically due to cascade)
    await session.delete(product)
    await session.commit()


@router.get("/", response_model=list[ProductSchema])
async def list_products(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    game: str | None = Query(None, description="Filter by game"),
    category: str | None = Query(None, description="Filter by category"),
    session: AsyncSession = Depends(get_async_session),
) -> list[ProductSchema]:
    """List products with pagination and filtering."""
    offset = (page - 1) * per_page

    query = select(Product).options(selectinload(Product.aliases))

    # Apply filters
    if game:
        query = query.where(Product.game.ilike(f"%{game}%"))
    if category:
        query = query.where(Product.category.ilike(f"%{category}%"))

    # Apply pagination
    query = query.order_by(Product.name).offset(offset).limit(per_page)

    result = await session.execute(query)
    products = result.scalars().all()

    return list(products)
