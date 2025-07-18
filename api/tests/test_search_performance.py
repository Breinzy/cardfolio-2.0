"""Performance tests for product search functionality."""

import asyncio
import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select

from ..app.database import get_async_session
from ..app.main import app
from ..app.models import Product, ProductAlias


@pytest.mark.asyncio
async def test_alias_search_performance():
    """Test that alias search meets the <10ms requirement."""
    # This test requires the database to be running with seed data

    async def get_session():
        async for session in get_async_session():
            return session

    session = await get_session()

    # Test queries that should be fast
    test_queries = [
        "Zard",  # Charizard nickname
        "Lotus",  # Black Lotus abbreviation
        "Pika",  # Pikachu nickname
        "Recall",  # Ancestral Recall abbreviation
        "Blast",  # Blastoise nickname
        "Shivan",  # Shivan Dragon abbreviation
    ]

    for query in test_queries:
        # Time the alias search query
        start_time = time.perf_counter()

        # Search aliases with subquery (same logic as in the API)
        alias_subquery = select(ProductAlias.product_id).where(
            func.to_tsvector("english", ProductAlias.alias).match(query),
        )

        # Get products matching the aliases
        products_query = select(Product).where(Product.id.in_(alias_subquery))
        result = await session.execute(products_query)
        products = result.scalars().all()

        end_time = time.perf_counter()
        query_time_ms = (end_time - start_time) * 1000

        print(f"Query '{query}': {query_time_ms:.2f}ms, found {len(products)} products")

        # Assert that the query takes less than 10ms
        assert (
            query_time_ms < 10.0
        ), f"Query '{query}' took {query_time_ms:.2f}ms, exceeding 10ms limit"

        # Assert that we found at least one product for known aliases
        assert len(products) > 0, f"No products found for alias '{query}'"

    await session.close()


@pytest.mark.asyncio
async def test_full_text_search_performance():
    """Test that full-text search on product names is fast."""

    async def get_session():
        async for session in get_async_session():
            return session

    session = await get_session()

    # Test queries for product names
    test_queries = [
        "Charizard",
        "Black Lotus",
        "Pikachu",
        "Magic",
        "Pokemon",
        "Alpha",
        "Base Set",
    ]

    for query in test_queries:
        # Time the full-text search query
        start_time = time.perf_counter()

        # Full-text search on product fields
        products_query = select(Product).where(
            func.to_tsvector(
                "english",
                func.coalesce(Product.name, "")
                + " "
                + func.coalesce(Product.set_name, "")
                + " "
                + func.coalesce(Product.variant, ""),
            ).match(query),
        )

        result = await session.execute(products_query)
        products = result.scalars().all()

        end_time = time.perf_counter()
        query_time_ms = (end_time - start_time) * 1000

        print(
            f"Full-text query '{query}': {query_time_ms:.2f}ms, found {len(products)} products"
        )

        # Assert that the query takes less than 10ms
        assert (
            query_time_ms < 10.0
        ), f"Full-text query '{query}' took {query_time_ms:.2f}ms, exceeding 10ms limit"

    await session.close()


def test_api_search_performance():
    """Test API search endpoint performance."""
    client = TestClient(app)

    # Test queries via API
    test_queries = [
        "Zard",
        "Lotus",
        "Pika",
        "Charizard",
        "Pokemon",
    ]

    for query in test_queries:
        # Time the API request
        start_time = time.perf_counter()

        response = client.get(f"/api/v1/products/search?q={query}")

        end_time = time.perf_counter()
        query_time_ms = (end_time - start_time) * 1000

        print(
            f"API query '{query}': {query_time_ms:.2f}ms, status: {response.status_code}"
        )

        # Assert successful response
        assert response.status_code == 200

        # Parse response
        data = response.json()
        assert "products" in data
        assert "total" in data

        # The API might be slower due to overhead, so we'll use a more lenient limit
        # But it should still be reasonably fast
        assert (
            query_time_ms < 50.0
        ), f"API query '{query}' took {query_time_ms:.2f}ms, too slow"


@pytest.mark.asyncio
async def test_search_with_filters_performance():
    """Test search with filters performance."""

    async def get_session():
        async for session in get_async_session():
            return session

    session = await get_session()

    # Test filtered searches
    test_cases = [
        ("Charizard", "Pokemon", None),
        ("Lotus", "Magic: The Gathering", None),
        ("Holo", "Pokemon", "Base Set"),
        ("Rare", "Magic: The Gathering", "Alpha"),
    ]

    for query, game, set_name in test_cases:
        start_time = time.perf_counter()

        # Build filtered query
        products_query = select(Product).where(
            func.to_tsvector(
                "english",
                func.coalesce(Product.name, "")
                + " "
                + func.coalesce(Product.set_name, "")
                + " "
                + func.coalesce(Product.variant, ""),
            ).match(query),
        )

        if game:
            products_query = products_query.where(Product.game.ilike(f"%{game}%"))
        if set_name:
            products_query = products_query.where(
                Product.set_name.ilike(f"%{set_name}%")
            )

        result = await session.execute(products_query)
        products = result.scalars().all()

        end_time = time.perf_counter()
        query_time_ms = (end_time - start_time) * 1000

        print(
            f"Filtered query '{query}' (game={game}, set={set_name}): {query_time_ms:.2f}ms, found {len(products)} products"
        )

        # Assert performance
        assert (
            query_time_ms < 15.0
        ), f"Filtered query took {query_time_ms:.2f}ms, too slow"

    await session.close()


if __name__ == "__main__":
    """Run performance tests directly."""
    print("Running Cardfolio 2.0 Search Performance Tests")
    print("=" * 50)

    # Run async tests
    asyncio.run(test_alias_search_performance())
    asyncio.run(test_full_text_search_performance())
    asyncio.run(test_search_with_filters_performance())

    # Run API test
    test_api_search_performance()

    print("\n✅ All performance tests passed!")
    print("Alias search requirement (<10ms) met! 🚀")
