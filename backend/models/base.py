# Mock Database Engine for the Wireframe
# Holds in-memory dictionaries for our collections

class MockDB:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.variants = {}
        self.price_lists = {}
        self.discount_tiers = {}
        self.category_discount_ceilings = {}
        self.approval_chain_rules = {}
        self.quotations = {}
        self.quotation_lines = {}
        self.approval_events = {}
        self.warehouses = {}
        self.stock_levels = {}
        self.fulfillment_splits = {}
        self.backorder_records = {}
        self.subscription_plans = {}
        self.billing_schedules = {}
        self.invoices = {}
        self.upsell_rules = {}
        self.audit_logs = {}

    def insert(self, collection: str, record_id: str, data: dict):
        getattr(self, collection)[record_id] = data
        return data

    def get(self, collection: str, record_id: str):
        return getattr(self, collection).get(record_id)

    def list(self, collection: str):
        return list(getattr(self, collection).values())

    def update(self, collection: str, record_id: str, data: dict):
        col = getattr(self, collection)
        if record_id in col:
            col[record_id].update(data)
            return col[record_id]
        return None

    def delete(self, collection: str, record_id: str):
        col = getattr(self, collection)
        if record_id in col:
            del col[record_id]
            return True
        return False

# Global instance for the app
db = MockDB()
