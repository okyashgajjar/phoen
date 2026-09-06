# Project Rules & Guidelines for DealFlow360

## Database & Data Integrity Rules
1. **Always work on the PostgreSQL database**:
   - Do not rely on ad-hoc or synthetic in-memory databases when PostgreSQL is configured.
   - Use the official database schema and models defined in `database/models.py`.
2. **Never create fake or synthetic data**:
   - Do not generate invented, mock, or fake customer/transaction records.
   - Always connect to, query, and mutate actual records from the database.
   - Maintain referential integrity across customer accounts, quotations, quotation lines, users, and audit logs.
