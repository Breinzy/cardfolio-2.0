-- Sample product data for Cardfolio 2.0 Master Catalog
-- Pokemon and Magic: The Gathering cards for testing

-- Pokemon Base Set Cards
INSERT INTO products (name, game, set_name, card_number, rarity, category, variant, market_price, low_price, high_price, description) VALUES
('Charizard', 'Pokemon', 'Base Set', '4/102', 'Holo Rare', 'Pokemon', 'Holo', 5000.00, 3000.00, 8000.00, 'Iconic fire-type starter Pokemon from the original Base Set'),
('Blastoise', 'Pokemon', 'Base Set', '2/102', 'Holo Rare', 'Pokemon', 'Holo', 1500.00, 1000.00, 2500.00, 'Water-type starter Pokemon from the original Base Set'),
('Venusaur', 'Pokemon', 'Base Set', '15/102', 'Holo Rare', 'Pokemon', 'Holo', 800.00, 600.00, 1200.00, 'Grass-type starter Pokemon from the original Base Set'),
('Pikachu', 'Pokemon', 'Base Set', '58/102', 'Common', 'Pokemon', 'Yellow Cheeks', 300.00, 200.00, 500.00, 'Electric mouse Pokemon, the series mascot'),
('Machamp', 'Pokemon', 'Base Set', '8/102', 'Holo Rare', 'Pokemon', '1st Edition', 400.00, 300.00, 600.00, 'Fighting-type Pokemon with incredible strength'),
('Alakazam', 'Pokemon', 'Base Set', '1/102', 'Holo Rare', 'Pokemon', 'Holo', 600.00, 400.00, 900.00, 'Psychic-type Pokemon with telekinetic powers'),
('Chansey', 'Pokemon', 'Base Set', '3/102', 'Holo Rare', 'Pokemon', 'Holo', 350.00, 250.00, 500.00, 'Normal-type Pokemon known for its healing abilities'),
('Clefairy', 'Pokemon', 'Base Set', '5/102', 'Holo Rare', 'Pokemon', 'Holo', 400.00, 300.00, 600.00, 'Fairy-type Pokemon with mystical powers'),
('Gyarados', 'Pokemon', 'Base Set', '6/102', 'Holo Rare', 'Pokemon', 'Holo', 450.00, 350.00, 650.00, 'Water/Flying-type Pokemon evolved from Magikarp'),
('Hitmonchan', 'Pokemon', 'Base Set', '7/102', 'Holo Rare', 'Pokemon', 'Holo', 300.00, 200.00, 450.00, 'Fighting-type Pokemon known for its punching attacks');

-- Magic: The Gathering Alpha/Beta Cards
INSERT INTO products (name, game, set_name, card_number, rarity, category, variant, market_price, low_price, high_price, description) VALUES
('Black Lotus', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 500000.00, 300000.00, 800000.00, 'The most iconic and expensive Magic card ever printed'),
('Ancestral Recall', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 50000.00, 30000.00, 80000.00, 'One of the Power Nine cards, allows drawing 3 cards'),
('Time Walk', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 25000.00, 15000.00, 40000.00, 'Power Nine card that grants an extra turn'),
('Mox Sapphire', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 35000.00, 20000.00, 55000.00, 'Power Nine mana artifact providing blue mana'),
('Mox Ruby', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 25000.00, 15000.00, 40000.00, 'Power Nine mana artifact providing red mana'),
('Mox Pearl', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 20000.00, 12000.00, 35000.00, 'Power Nine mana artifact providing white mana'),
('Mox Emerald', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 25000.00, 15000.00, 40000.00, 'Power Nine mana artifact providing green mana'),
('Mox Jet', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 30000.00, 18000.00, 45000.00, 'Power Nine mana artifact providing black mana'),
('Timetwister', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 15000.00, 10000.00, 25000.00, 'Power Nine card that resets hands and graveyards'),
('Shivan Dragon', 'Magic: The Gathering', 'Alpha', NULL, 'Rare', 'Magic', 'Alpha', 2500.00, 1500.00, 4000.00, 'Iconic red dragon creature from the early days of Magic');

-- Modern Pokemon Cards
INSERT INTO products (name, game, set_name, card_number, rarity, category, variant, market_price, low_price, high_price, description) VALUES
('Charizard VMAX', 'Pokemon', 'Champion''s Path', '074/073', 'Secret Rare', 'Pokemon', 'Rainbow Rare', 400.00, 300.00, 600.00, 'Popular VMAX card from Champion''s Path'),
('Pikachu VMAX', 'Pokemon', 'Vivid Voltage', '188/185', 'Secret Rare', 'Pokemon', 'Rainbow Rare', 150.00, 100.00, 250.00, 'Electric-type VMAX card'),
('Umbreon VMAX', 'Pokemon', 'Evolving Skies', '215/203', 'Secret Rare', 'Pokemon', 'Alternate Art', 200.00, 150.00, 350.00, 'Dark-type VMAX with alternate artwork'),
('Rayquaza VMAX', 'Pokemon', 'Evolving Skies', '218/203', 'Secret Rare', 'Pokemon', 'Alternate Art', 300.00, 200.00, 500.00, 'Dragon-type VMAX with stunning artwork'),
('Mew VMAX', 'Pokemon', 'Fusion Strike', '269/264', 'Secret Rare', 'Pokemon', 'Rainbow Rare', 180.00, 120.00, 280.00, 'Psychic-type VMAX from Fusion Strike');

-- Now insert product aliases for better search
INSERT INTO product_aliases (product_id, alias, alias_type, search_weight) 
SELECT p.id, 'Zard', 'nickname', 10
FROM products p WHERE p.name = 'Charizard' AND p.set_name = 'Base Set';

INSERT INTO product_aliases (product_id, alias, alias_type, search_weight) 
SELECT p.id, 'Lotus', 'abbreviation', 10
FROM products p WHERE p.name = 'Black Lotus';

INSERT INTO product_aliases (product_id, alias, alias_type, search_weight) 
SELECT p.id, 'Recall', 'abbreviation', 8
FROM products p WHERE p.name = 'Ancestral Recall';

INSERT INTO product_aliases (product_id, alias, alias_type, search_weight) 
SELECT p.id, 'Pika', 'nickname', 7
FROM products p WHERE p.name = 'Pikachu' AND p.set_name = 'Base Set';

INSERT INTO product_aliases (product_id, alias, alias_type, search_weight) 
SELECT p.id, 'Blast', 'nickname', 6
FROM products p WHERE p.name = 'Blastoise';

INSERT INTO product_aliases (product_id, alias, alias_type, search_weight) 
SELECT p.id, 'Venu', 'nickname', 6
FROM products p WHERE p.name = 'Venusaur';

INSERT INTO product_aliases (product_id, alias, alias_type, search_weight) 
SELECT p.id, 'Shivan', 'abbreviation', 5
FROM products p WHERE p.name = 'Shivan Dragon';

INSERT INTO product_aliases (product_id, alias, alias_type, search_weight) 
SELECT p.id, 'Champion Path Zard', 'nickname', 9
FROM products p WHERE p.name = 'Charizard VMAX' AND p.set_name = 'Champion''s Path';

INSERT INTO product_aliases (product_id, alias, alias_type, search_weight) 
SELECT p.id, 'Rainbow Pika', 'nickname', 8
FROM products p WHERE p.name = 'Pikachu VMAX'; 