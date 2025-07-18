-- Cardfolio 2.0 Master Catalog Schema
-- Stage 1: Products and Product Aliases

-- Products table: Core product information
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    game VARCHAR(100) NOT NULL,
    set_name VARCHAR(255),
    card_number VARCHAR(50),
    rarity VARCHAR(50),
    condition VARCHAR(50) DEFAULT 'NM',
    variant VARCHAR(100), -- e.g., "Holo", "1st Edition", "Shadowless"
    category VARCHAR(100) NOT NULL, -- e.g., "Pokemon", "Magic", "Sports"
    subcategory VARCHAR(100), -- e.g., "Base Set", "Unlimited"
    release_date DATE,
    image_url TEXT,
    description TEXT,
    market_price DECIMAL(10, 2),
    low_price DECIMAL(10, 2),
    high_price DECIMAL(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Product aliases table: For fast search optimization
CREATE TABLE product_aliases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    alias VARCHAR(255) NOT NULL,
    alias_type VARCHAR(50) NOT NULL, -- e.g., "name", "abbreviation", "nickname", "misspelling"
    search_weight INTEGER DEFAULT 1, -- Higher weight = more relevant
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for optimal search performance (<10ms target)
CREATE INDEX idx_products_name ON products USING gin(to_tsvector('english', name));
CREATE INDEX idx_products_game ON products(game);
CREATE INDEX idx_products_set_name ON products(set_name);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_card_number ON products(card_number);
CREATE INDEX idx_products_created_at ON products(created_at);

-- Alias search indexes (critical for <10ms performance)
CREATE INDEX idx_product_aliases_alias ON product_aliases USING gin(to_tsvector('english', alias));
CREATE INDEX idx_product_aliases_product_id ON product_aliases(product_id);
CREATE INDEX idx_product_aliases_alias_type ON product_aliases(alias_type);
CREATE INDEX idx_product_aliases_search_weight ON product_aliases(search_weight DESC);

-- Composite index for common search patterns
CREATE INDEX idx_products_game_set_name ON products(game, set_name);
CREATE INDEX idx_products_category_game ON products(category, game);

-- Full-text search index combining product name and aliases
CREATE INDEX idx_products_full_text ON products USING gin(
    to_tsvector('english', name || ' ' || COALESCE(set_name, '') || ' ' || COALESCE(variant, ''))
);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON products 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE products IS 'Core product catalog for cards and collectibles';
COMMENT ON TABLE product_aliases IS 'Alternative names and search terms for products';
COMMENT ON COLUMN products.variant IS 'Card variant like Holo, 1st Edition, Shadowless';
COMMENT ON COLUMN product_aliases.search_weight IS 'Higher weight = more relevant in search results';
COMMENT ON COLUMN product_aliases.alias_type IS 'Type of alias: name, abbreviation, nickname, misspelling'; 