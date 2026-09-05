import os
import sqlite3
from datetime import datetime

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "phoen.db")

class SQLiteMockDB:
    def __init__(self, db_path=None):
        self.db_path = db_path or DEFAULT_DB_PATH
        self._memory = {}

    def _init_memory(self):
        # We populate _memory manually for tests to pass
        pass # The old seed.py will call db.insert() to populate it

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # Helper mapping functions
    def _map_user(self, row):
        return {
            "id": row["id"],
            "email": row["email"],
            "password": row["password"],
            "role": row["role"],
            "name": row["name"],
            "tier": row["tier"]
        }

    def _map_product(self, row):
        return {
            "id": row["product_id"],
            "name": row["product_name"],
            "category": row["category_id"], # simplistic mapping
            "base_price": float(row["base_price"]),
            "unit": row["unit"],
            "tax_percent": float(row["tax_rate"]),
            "description": row["description"],
            "is_recurring": bool(row["is_recurring"])
        }

    def _map_customer(self, row):
        return {
            "id": row["customer_id"],
            "name": row["company_name"],
            "tier": row["customer_tier"],
            "role": "customer"
        }

    def _map_quotation(self, row, conn):
        # Fetch lines
        cur = conn.cursor()
        cur.execute("SELECT * FROM quotation_lines WHERE quotation_id = ?", (row["quotation_id"],))
        lines_rows = cur.fetchall()
        lines = []
        for l in lines_rows:
            product_id = l["product_variant_id"] or l["service_id"] or l["subscription_plan_id"] or "Unknown"
            lines.append({
                "id": l["line_id"],
                "product_id": product_id,
                "qty": int(l["quantity"]),
                "unit_price": float(l["unit_price"]),
                "unitPrice": float(l["unit_price"]),
                "discount": float(l["discount_percent"]),
                "discount_percent": float(l["discount_percent"]),
                "is_recurring": False # simplistic
            })

        row_dict = dict(row)
        return {
            "id": row_dict["quotation_id"],
            "customer_id": row_dict["customer_id"],
            "sales_rep_id": row_dict.get("created_by", "rep_marcus"), # Map correctly if needed
            "status": row_dict.get("status", "DRAFT"),
            "title": row_dict["notes"] if row_dict["notes"] else "Quotation",
            "amount": float(row_dict.get("grand_total", 0.0)),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "lines": lines
        }

    def get(self, collection: str, record_id: str):
        if collection in self._memory and record_id in self._memory[collection]:
            return self._memory[collection][record_id]

        conn = self._get_conn()
        cur = conn.cursor()
        
        try:
            if collection == "users":
                cur.execute("SELECT * FROM users WHERE id = ?", (record_id,))
                row = cur.fetchone()
                return self._map_user(row) if row else None
            elif collection == "products":
                cur.execute("SELECT * FROM products WHERE product_id = ?", (record_id,))
                row = cur.fetchone()
                return self._map_product(row) if row else None
            elif collection == "quotations":
                cur.execute("SELECT * FROM quotations WHERE quotation_id = ?", (record_id,))
                row = cur.fetchone()
                return self._map_quotation(row, conn) if row else None
            elif collection == "customers":
                cur.execute("SELECT * FROM customers WHERE customer_id = ?", (record_id,))
                row = cur.fetchone()
                return self._map_customer(row) if row else None
            
            # Fallback for others that might not exist in SQLite schema yet
            return None
        finally:
            conn.close()

    def list(self, collection: str):
        results = []
        if collection in self._memory:
            results.extend(list(self._memory[collection].values()))

        conn = self._get_conn()
        cur = conn.cursor()
        
        try:
            if collection == "users":
                cur.execute("SELECT * FROM users")
                for row in cur.fetchall():
                    # Avoid duplicates if mock data is injected to both
                    mapped = self._map_user(row)
                    if mapped["id"] not in [r["id"] for r in results]:
                        results.append(mapped)
            elif collection == "products":
                cur.execute("SELECT * FROM products")
                for row in cur.fetchall():
                    results.append(self._map_product(row))
            elif collection == "quotations":
                cur.execute("SELECT * FROM quotations")
                for row in cur.fetchall():
                    results.append(self._map_quotation(row, conn))
            elif collection == "customers":
                cur.execute("SELECT * FROM customers")
                for row in cur.fetchall():
                    results.append(self._map_customer(row))
            
            return results
        finally:
            conn.close()

    def insert(self, collection: str, record_id: str, data: dict):
        if collection not in self._memory:
            self._memory[collection] = {}
        self._memory[collection][record_id] = data
        return data

    def update(self, collection: str, record_id: str, data: dict):
        if collection in self._memory and record_id in self._memory[collection]:
            self._memory[collection][record_id].update(data)
            return self._memory[collection][record_id]
        return data

    def delete(self, collection: str, record_id: str):
        if collection in self._memory and record_id in self._memory[collection]:
            del self._memory[collection][record_id]
            return True
        return False

db = SQLiteMockDB()
