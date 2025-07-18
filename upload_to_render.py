import pandas as pd
from sqlalchemy import create_engine, text

# PostgreSQL database URL from Render
db_url = "postgresql://ecommerce_deke_user:dvx8GWrmHDCnjkCD4j0QMqUdX68CNew9@dpg-d1sd7gbipnbc73dv6ti0-a.oregon-postgres.render.com/ecommerce_deke"

# Connect to the database
engine = create_engine(db_url)

# ✅ Drop all existing tables
with engine.connect() as conn:
    conn.execute(text("""
        DO $$ DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
            END LOOP;
        END $$;
    """))
    print("🗑️ All existing tables dropped from PostgreSQL.")

# 📁 CSV file paths
tables = {
    "orders": "data/orders.csv",
    "order_items": "data/order_items.csv",
    "products": "data/products.csv",
    "order_item_refunds": "data/order_item_refunds.csv",
    "website_pageviews": "data/website_pageviews.csv",
    "w_sessions": "data/w_sessions.csv"
}

# 🔄 Upload each CSV file to the database
for table_name, file_path in tables.items():
    print(f"📥 Loading {file_path}...")
    df = pd.read_csv(file_path)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"✅ Uploaded '{table_name}' to PostgreSQL.")

print("🎉 All tables uploaded successfully!")
