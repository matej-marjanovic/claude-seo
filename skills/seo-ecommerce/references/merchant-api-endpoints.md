# DataForSEO Merchant API Endpoints

> Load this reference when using the seo-ecommerce skill or Merchant API commands.

## Google Shopping Endpoints

### Products Search

**Endpoint:** `merchant/google/products/task_post` (submit) → `task_get/advanced` (retrieve)

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keyword` | string | ✅ | — | Search query for products |
| `location_code` | int | — | 2840 (US) | Target location |
| `language_code` | string | — | `en` | Language |
| `depth` | int | — | 20 | Max results (up to 100) |
| `tag` | string | — | — | Custom task tag |

**Response fields:** `rank_group`, `rank_absolute`, `title`, `description`, `url`, `domain`, `price` (object with `current`, `regular`, `max_value`), `currency`, `rating` (object with `value`, `reviews_count`), `seller`, `product_id`, `data_docid`

**Cost:** $0.0024/task (standard) | $0.003/task + $0.0003/product (live)

### Sellers

**Endpoint:** `merchant/google/sellers/task_post` → `task_get/advanced`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_id` | string | ✅ | Product ID from products search |
| `location_code` | int | — | Target location |
| `language_code` | string | — | Language |

**Response fields:** `title`, `seller_name`, `url`, `price`, `condition`, `delivery_info`, `rating`

**Cost:** $0.0024/task (standard) | $0.003/task (live)

### Product Specs

**Endpoint:** `merchant/google/product_spec/task_post` → `task_get/advanced`

**Parameters:** Same as Sellers (requires `product_id`)

**Response fields:** `name`, `value`, `category`

**Cost:** $0.0024/task (standard)

### Product Reviews

**Endpoint:** `merchant/google/product_reviews/task_post` → `task_get/advanced`

**Parameters:** `product_id`, `location_code`, `language_code`, `depth`

**Response fields:** `rating`, `review_text`, `timestamp`, `author`, `title`, `helpful_count`

**Cost:** $0.0024/task (standard)

---

## Amazon Endpoints

### Products Search

**Endpoint:** `merchant/amazon/products/task_post` → `task_get/advanced`

**Parameters:** Same as Google Shopping Products

**Response fields:** Same structure as Google but with Amazon-specific fields: `asin`, `is_amazon_choice`, `is_best_seller`, `prime_delivery`

**Cost:** $0.0024/task (standard) | $0.003/task + $0.0003/product (live)

### Sellers

**Endpoint:** `merchant/amazon/sellers/task_post` → `task_get/advanced`

**Parameters:** `product_id` (Amazon ASIN), `location_code`, `language_code`

**Cost:** $0.0024/task (standard)

### Reviews

**Endpoint:** `merchant/amazon/reviews/task_post` → `task_get/advanced`

**Parameters:** `product_id` (ASIN), `location_code`, `language_code`, `depth`

**Cost:** $0.0024/task (standard)

---

## CLI Reference

```bash
# Google Shopping product search
python3 scripts/dataforseo_merchant.py products "running shoes" --marketplace google

# Amazon product search
python3 scripts/dataforseo_merchant.py products "wireless earbuds" --marketplace amazon

# Seller comparison (requires product_id from products search)
python3 scripts/dataforseo_merchant.py sellers <product_id> --marketplace google

# Product specs (Google only)
python3 scripts/dataforseo_merchant.py specs <product_id>

# Product reviews
python3 scripts/dataforseo_merchant.py reviews <product_id> --limit 20

# Raw JSON output
python3 scripts/dataforseo_merchant.py products "laptop" --json
```

---

## Cost Estimates

| Command | Standard | Live |
|---------|----------|------|
| Products (20 results) | ~$0.008 | ~$0.009 |
| Sellers | ~$0.002 | ~$0.003 |
| Specs | ~$0.002 | ~$0.003 |
| Reviews (20) | ~$0.002 | ~$0.003 |
| Full analysis (products + sellers + specs) | ~$0.012 | ~$0.015 |
