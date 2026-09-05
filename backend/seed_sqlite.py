import os
import sqlite3
import pandas as pd

DB_PATH = "phoen.db"
SEED_DIR = "../seed-data"

def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed old {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    print(f"Connected to {DB_PATH}")

    csv_files = [f for f in os.listdir(SEED_DIR) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        table_name = csv_file.replace('.csv', '')
        file_path = os.path.join(SEED_DIR, csv_file)
        print(f"Ingesting {csv_file} into table {table_name}...")
        df = pd.read_csv(file_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"  Inserted {len(df)} rows.")

    # We also need a Users table since seed-data might not have one (wait, let's check if it has customers/users).
    # To ensure the mock logins still work, we can inject a few base users.
    users_data = [
        {"id": "rep_marcus", "email": "marcus@phoen.io", "password": "password", "role": "sales_rep", "name": "Marcus Vance", "tier": "Gold"},
        {"id": "rep_rachel", "email": "rachel@phoen.io", "password": "password", "role": "sales_rep", "name": "Rachel Torres", "tier": "Gold"},
        {"id": "admin_1", "email": "admin@phoen.io", "password": "password", "role": "admin", "name": "Admin User", "tier": "Gold"}
    ]
    pd.DataFrame(users_data).to_sql("users", conn, if_exists='replace', index=False)
    print("Injected base users into 'users' table.")

    conn.close()
    print("Database seeding complete.")

if __name__ == "__main__":
    main()
