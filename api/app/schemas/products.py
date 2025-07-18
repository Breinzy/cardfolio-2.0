"""Pydantic schemas for Product and ProductAlias models."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class ProductAliasBase(BaseModel):
    """Base schema for ProductAlias."""

    alias: str = Field(
        ..., min_length=1, max_length=255, description="Alternative name or search term"
    )
    alias_type: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Type of alias (name, abbreviation, etc.)",
    )
    search_weight: int = Field(
        default=1, ge=1, le=10, description="Search relevance weight (1-10)"
    )


class ProductAliasCreate(ProductAliasBase):
    """Schema for creating a new ProductAlias."""


class ProductAliasUpdate(BaseModel):
    """Schema for updating a ProductAlias."""

    alias: str | None = Field(None, min_length=1, max_length=255)
    alias_type: str | None = Field(None, min_length=1, max_length=50)
    search_weight: int | None = Field(None, ge=1, le=10)


class ProductAlias(ProductAliasBase):
    """Schema for ProductAlias response."""

    id: UUID
    product_id: UUID
    created_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class ProductBase(BaseModel):
    """Base schema for Product."""

    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    game: str = Field(..., min_length=1, max_length=100, description="Game/franchise")
    set_name: str | None = Field(
        None, max_length=255, description="Set or collection name"
    )
    card_number: str | None = Field(None, max_length=50, description="Card number")
    rarity: str | None = Field(None, max_length=50, description="Rarity level")
    condition: str = Field(default="NM", max_length=50, description="Card condition")
    variant: str | None = Field(
        None, max_length=100, description="Variant (Holo, 1st Edition, etc.)"
    )
    category: str = Field(
        ..., min_length=1, max_length=100, description="Product category"
    )
    subcategory: str | None = Field(
        None, max_length=100, description="Product subcategory"
    )
    release_date: datetime | None = Field(None, description="Release date")
    image_url: str | None = Field(None, description="Image URL")
    description: str | None = Field(None, description="Product description")
    market_price: Decimal | None = Field(
        None, ge=0, decimal_places=2, description="Current market price"
    )
    low_price: Decimal | None = Field(
        None, ge=0, decimal_places=2, description="Historical low price"
    )
    high_price: Decimal | None = Field(
        None, ge=0, decimal_places=2, description="Historical high price"
    )


class ProductCreate(ProductBase):
    """Schema for creating a new Product."""


class ProductUpdate(BaseModel):
    """Schema for updating a Product."""

    name: str | None = Field(None, min_length=1, max_length=255)
    game: str | None = Field(None, min_length=1, max_length=100)
    set_name: str | None = Field(None, max_length=255)
    card_number: str | None = Field(None, max_length=50)
    rarity: str | None = Field(None, max_length=50)
    condition: str | None = Field(None, max_length=50)
    variant: str | None = Field(None, max_length=100)
    category: str | None = Field(None, min_length=1, max_length=100)
    subcategory: str | None = Field(None, max_length=100)
    release_date: datetime | None = Field(None)
    image_url: str | None = Field(None)
    description: str | None = Field(None)
    market_price: Decimal | None = Field(None, ge=0, decimal_places=2)
    low_price: Decimal | None = Field(None, ge=0, decimal_places=2)
    high_price: Decimal | None = Field(None, ge=0, decimal_places=2)


class Product(ProductBase):
    """Schema for Product response."""

    id: UUID
    created_at: datetime
    updated_at: datetime
    aliases: list[ProductAlias] = []

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class ProductSearchResult(BaseModel):
    """Schema for product search results."""

    products: list[Product]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool


class ProductSearchQuery(BaseModel):
    """Schema for product search query."""

    q: str = Field(..., min_length=1, description="Search query")
    game: str | None = Field(None, description="Filter by game")
    category: str | None = Field(None, description="Filter by category")
    set_name: str | None = Field(None, description="Filter by set name")
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=20, ge=1, le=100, description="Items per page")
