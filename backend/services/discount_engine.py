from models.base import db
from models.sales import Quotation
from models.products import DiscountTier, CategoryDiscountCeiling

def calculate_blended_risk_score(quotation: Quotation) -> float:
    # Get Customer Tier (assuming customer object has a tier, we'll mock it for now)
    # Since customer is just an ID in the mock, we can fetch their tier
    customer = db.get("users", quotation.customer_id) # Let's assume customer is in users table
    if not customer:
        return 0.0
    
    # Mock lookup for customer tier ceiling. Let's assume customer has a 'tier' field
    customer_tier = customer.get("tier", "Bronze")
    
    # Find matching discount tier
    all_discount_tiers = db.list("discount_tiers")
    tier_ceiling = 0.0
    for dt in all_discount_tiers:
        if dt.get("customer_tier") == customer_tier:
            tier_ceiling = dt.get("max_discount_percent", 0.0)
            break

    total_overage = 0.0
    
    for line in quotation.lines:
        product = db.get("products", line.product_id)
        if not product:
            continue
            
        category = product.get("category")
        
        # Find category ceiling
        all_category_ceilings = db.list("category_discount_ceilings")
        category_ceiling = 100.0 # Default high
        for cc in all_category_ceilings:
            if cc.get("category") == category:
                category_ceiling = cc.get("max_discount_percent", 100.0)
                break
                
        # The stricter of the two
        allowed_discount = min(tier_ceiling, category_ceiling)
        
        # Given discount
        given_discount = line.discount_percent
        
        # Compute overage (floor 0)
        overage = max(0.0, given_discount - allowed_discount)
        
        # Accumulate (could weight by line amount, but PRD says "sum into a flag")
        total_overage += overage
        
    return total_overage
