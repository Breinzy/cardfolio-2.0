#!/usr/bin/env python3
"""Load seed data into the Cardfolio database."""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.app.database import engine


async def load_seed_data() -> None:
    """Load seed data from SQL files."""
    seed_files = [
        "warehouse/ddl/00_catalog.sql",
        "warehouse/seeds/01_sample_products.sql",
    ]

    print("Loading seed data...")

    async with engine.begin() as conn:
        for seed_file in seed_files:
            file_path = project_root / seed_file
            if not file_path.exists():
                print(f"Warning: Seed file {seed_file} not found, skipping...")
                continue

            print(f"Loading {seed_file}...")

            with open(file_path, encoding="utf-8") as f:
                sql_content = f.read()

            # Split SQL content by semicolons and execute each statement
            statements = [
                stmt.strip() for stmt in sql_content.split(";") if stmt.strip()
            ]

            for statement in statements:
                if statement.strip():
                    try:
                        await conn.execute(statement)
                        print(f"  ✓ Executed statement: {statement[:50]}...")
                    except Exception as e:
                        print(f"  ✗ Error executing statement: {e}")
                        print(f"    Statement: {statement[:100]}...")
                        # Continue with other statements
                        continue

    print("Seed data loading complete!")


async def main() -> None:
    """Main function."""
    print("Cardfolio 2.0 - Seed Data Loader")
    print("=" * 40)

    # Check database connection
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://cardfolio:dev@localhost:5432/cardfolio",
    )
    print(f"Database URL: {database_url}")

    try:
        await load_seed_data()
        print("\n✅ Seed data loaded successfully!")
    except Exception as e:
        print(f"\n❌ Error loading seed data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
