import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
import sqlalchemy

# Ensure parent directory is in path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import DATABASE_URL
from database.models import Base

# Setup DB Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_csv_files(base_dir):
    """Return dict of filename to full path for a given directory."""
    if not os.path.exists(base_dir):
        return {}
    return {f: os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.endswith('.csv')}

def clean_df(df):
    """Replace NaN and NaT with None so SQLAlchemy handles them as NULL."""
    return df.replace({np.nan: None})

def upsert_data(table, df, unique_cols, session):
    """Perform a generic UPSERT (merge) using SQLAlchemy."""
    if df.empty:
        return
        
    records = df.to_dict(orient='records')
    model_class = table
    
    seen_ids = set()
    for record in records:
        pk_val = record.get('id')
        if pk_val in seen_ids:
            continue
            
        instance = session.query(model_class).filter_by(**{col: record[col] for col in ['id']}).first()
        if instance:
            # We are doing a DO NOTHING equivalent for master data to preserve the first imported city
            if pk_val:
                seen_ids.add(pk_val)
        else:
            # Filter record to only include valid columns for this model
            valid_cols = model_class.__table__.columns.keys()
            filtered_record = {k: v for k, v in record.items() if k in valid_cols}
            try:
                with session.begin_nested():
                    new_instance = model_class(**filtered_record)
                    session.add(new_instance)
                if pk_val:
                    seen_ids.add(pk_val)
            except sqlalchemy.exc.IntegrityError:
                # Ignore duplicate uniqueness violations for master data across cities
                pass

def import_city_dataset(city_name, folder_path, session):
    print(f"--- Importing {city_name} dataset from {folder_path} ---")
    files = get_csv_files(folder_path)
    
    if not files:
        print(f"No CSVs found in {folder_path}")
        return

    # To avoid circular dependency issues, we import in the exact order
    from database import models
    
    import_order = [
        ('brands.csv', models.Brand, 'brand_id'),
        ('categories.csv', models.Category, 'category_id'),
        ('warehouses.csv', models.Warehouse, 'warehouse_id'),
        ('services.csv', models.Service, 'service_id'),
        ('subscription_plans.csv', models.SubscriptionPlan, 'plan_id'),
        ('products.csv', models.Product, 'product_id'),
        ('product_variants.csv', models.ProductVariant, 'variant_id'),
        ('product_service_rules.csv', models.ProductServiceRule, 'rule_id'),
        ('product_recommendations.csv', models.ProductRecommendation, 'recommendation_id'),
        ('customers.csv', models.Customer, 'customer_id'),
        ('discount_rules.csv', models.DiscountRule, 'discount_rule_id'),
        ('price_lists.csv', models.PriceList, 'price_list_id'),
        ('customer_price_lists.csv', models.CustomerPriceList, 'customer_price_id'),
        ('approval_chains.csv', models.ApprovalChain, 'chain_id'),
        ('quotations.csv', models.Quotation, 'quotation_id'),
        ('quotation_lines.csv', models.QuotationLine, 'line_id'),
        ('inventory.csv', models.Inventory, 'inventory_id'),
        ('negotiations.csv', models.Negotiation, 'negotiation_id'),
        ('customer_negotiations.csv', models.Negotiation, 'negotiation_id'),
        ('orders.csv', models.Order, 'order_id'),
        ('warehouse_allocations.csv', models.WarehouseAllocation, 'allocation_id'),
        ('invoices.csv', models.Invoice, 'invoice_id'),
        ('invoice_lines.csv', models.InvoiceLine, 'invoice_line_id'),
        ('subscriptions.csv', models.Subscription, 'subscription_contract_id'),
        ('deal_health.csv', models.DealHealth, 'deal_health_id'),
        ('audit_logs.csv', models.AuditLog, 'audit_id'),
    ]
    
    for filename, model, pk_col in import_order:
        if filename in files:
            print(f"Importing {filename} into {model.__tablename__}...")
            df = pd.read_csv(files[filename])
            df = clean_df(df)
            
            # Explicitly map the primary key to 'id'
            if pk_col in df.columns:
                df.rename(columns={pk_col: 'id'}, inplace=True)
                
            # Rename specifically weird columns
            df.rename(columns={
                'maximum_discount_percent': 'max_discount_percent',
                'minimum_margin_percent': 'min_margin_percent',
                'brand_name': 'name',
                'category_name': 'name',
                'warehouse_name': 'name',
                'service_name': 'name',
                'plan_name': 'name',
                'product_name': 'name',
                'variant_name': 'name',
                'brand_code': 'code',
                'warehouse_code': 'code',
                'customer_code': 'code',
                'product_code': 'code',
                'parent_category_id': 'parent_id',
                'variant_sku': 'sku',
                'plan_code': 'code',
                'service_code': 'code',
                'chain_code': 'code'
            }, inplace=True)

            
            # Convert date columns
            date_cols = ['effective_from', 'effective_to', 'quotation_date', 'valid_until', 'last_restocked_at', 
                         'next_expected_restock', 'start_date', 'next_renewal_date', 'submitted_at', 'resolved_at',
                         'order_date', 'promised_delivery_date', 'allocated_at', 'invoice_date', 'due_date',
                         'last_evaluated_at', 'timestamp', 'created_at', 'updated_at']
            
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    df[col] = df[col].apply(lambda x: x.to_pydatetime() if pd.notnull(x) else None)
            
            # Clean dataframe again to replace NaN/NaT with None
            df = clean_df(df)
            
            upsert_data(model, df, ['id'], session)
            
    session.commit()
    print(f"Finished importing {city_name}.")

def main():
    print("Starting DealFlow360 Seed Data Import...")
    
    # Create all tables
    print("Creating tables in database...")
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    try:
        # Import in order of size/complexity to resolve master data
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        import_city_dataset('Ahmedabad', os.path.join(base_dir, 'seed-data'), session)
        import_city_dataset('Bangalore', os.path.join(base_dir, 'seed-data-bangalore'), session)
        import_city_dataset('Mumbai', os.path.join(base_dir, 'seed-data-mumbai'), session)
        
        print("Import completed successfully!")
    except Exception as e:
        session.rollback()
        print(f"Import failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    main()
