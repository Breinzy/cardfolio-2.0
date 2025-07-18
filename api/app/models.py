"""SQLAlchemy models for Cardfolio 2.0."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DECIMAL, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime

from .database import Base


class Product(Base):
    """Product model representing cards and collectibles."""

    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    game: Mapped[str] = mapped_column(String(100), nullable=False)
    set_name: Mapped[str | None] = mapped_column(String(255))
    card_number: Mapped[str | None] = mapped_column(String(50))
    rarity: Mapped[str | None] = mapped_column(String(50))
    condition: Mapped[str] = mapped_column(String(50), default="NM")
    variant: Mapped[str | None] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    subcategory: Mapped[str | None] = mapped_column(String(100))
    release_date: Mapped[datetime | None] = mapped_column(DateTime)
    image_url: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    market_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2))
    low_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2))
    high_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    aliases: Mapped[list["ProductAlias"]] = relationship(
        "ProductAlias",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class ProductAlias(Base):
    """Product alias model for search optimization."""

    __tablename__ = "product_aliases"

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    product_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    alias: Mapped[str] = mapped_column(String(255), nullable=False)
    alias_type: Mapped[str] = mapped_column(String(50), nullable=False)
    search_weight: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    product: Mapped[Product] = relationship("Product", back_populates="aliases")
