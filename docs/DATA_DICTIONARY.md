# DealFlow360 Data Dictionary

This document details the critical tables within the DealFlow360 PostgreSQL database.

## TABLE: products
**Purpose**: Stores the abstract catalog items before they are broken down into specific hardware configurations.
| Column | Type | Nullable | Primary Key | Foreign Key | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | VARCHAR(50) | No | Yes | - | Internal unique identifier (e.g., PRD-001) |
| `brand_id` | VARCHAR(50) | No | - | `brands.id` | Brand reference |
| `category_id` | VARCHAR(50) | No | - | `categories.id` | Category classification |
| `name` | VARCHAR(255) | No | - | - | Human-readable product name |
| `base_price` | NUMERIC(18,2) | No | - | - | Reference baseline price |

## TABLE: product_variants
**Purpose**: Stores sellable, distinct SKUs.
| Column | Type | Nullable | Primary Key | Foreign Key | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | VARCHAR(50) | No | Yes | - | Internal unique identifier |
| `product_id` | VARCHAR(50) | No | - | `products.id` | Parent product reference |
| `sku` | VARCHAR(100) | No | - | - | Stock Keeping Unit (UNIQUE index) |
| `selling_price`| NUMERIC(18,2) | No | - | - | Actual selling price for this SKU |

## TABLE: inventory
**Purpose**: Tracks stock levels per warehouse.
| Column | Type | Nullable | Primary Key | Foreign Key | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | VARCHAR(50) | No | Yes | - | Internal unique identifier |
| `warehouse_id` | VARCHAR(50) | No | - | `warehouses.id` | The location of the stock |
| `variant_id` | VARCHAR(50) | No | - | `product_variants.id`| The specific SKU |
| `available_quantity`| INT | No | - | - | Stock ready to sell |
| `allocated_quantity`| INT | No | - | - | Stock assigned to an order |

## TABLE: quotations
**Purpose**: Preserves customer offers and snapshots deal status.
| Column | Type | Nullable | Primary Key | Foreign Key | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | VARCHAR(50) | No | Yes | - | Internal identifier |
| `customer_id` | VARCHAR(50) | No | - | `customers.id` | The customer receiving the quote |
| `grand_total` | NUMERIC(18,2) | No | - | - | The final calculated price |
| `status` | VARCHAR(50) | No | - | - | Enum: DRAFT, SUBMITTED, APPROVED, REJECTED |
