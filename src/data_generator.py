"""
ResilioChain — Phase 1: Synthetic Data Generator
Simulates 365 days of a warehouse with realistic demand patterns.
"""

import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
np.random.seed(42)

# ─────────────────────────────────────────────
# 1. PRODUCT CATALOGUE
# ─────────────────────────────────────────────
PRODUCTS = [
    {"product_id": "P001", "name": "Wireless Headphones",  "category": "Electronics", "unit_cost": 45.00, "unit_price": 89.99,  "base_demand": 22},
    {"product_id": "P002", "name": "Yoga Mat",             "category": "Fitness",     "unit_cost": 12.00, "unit_price": 29.99,  "base_demand": 18},
    {"product_id": "P003", "name": "Stainless Water Bottle","category": "Kitchen",    "unit_cost": 8.00,  "unit_price": 19.99,  "base_demand": 30},
    {"product_id": "P004", "name": "Bluetooth Speaker",    "category": "Electronics", "unit_cost": 30.00, "unit_price": 59.99,  "base_demand": 15},
    {"product_id": "P005", "name": "Winter Jacket",        "category": "Apparel",     "unit_cost": 55.00, "unit_price": 129.99, "base_demand": 10},
]

# ─────────────────────────────────────────────
# 2. SUPPLIER TABLE
# ─────────────────────────────────────────────
SUPPLIERS = [
    {"supplier_id": "S001", "name": "AsiaTech Imports",   "lead_time_days": 14, "reliability": 0.92},
    {"supplier_id": "S002", "name": "EuroGoods Ltd",      "lead_time_days": 7,  "reliability": 0.97},
    {"supplier_id": "S003", "name": "LocalFast Supply Co","lead_time_days": 3,  "reliability": 0.99},
]

# Map products to suppliers
PRODUCT_SUPPLIER_MAP = {
    "P001": "S001", "P002": "S002",
    "P003": "S003", "P004": "S001", "P005": "S002",
}


def add_seasonality(base_demand: int, date: datetime) -> float:
    """
    Realistic demand multiplier based on:
    - Day of week (weekend boost)
    - Month (Dec holiday spike, Jan slump, summer)
    """
    dow_factor = 1.3 if date.weekday() >= 5 else 1.0      # weekend bump
    
    month = date.month
    monthly_factors = {
        1: 0.75,  # Jan slump (post-holiday)
        2: 0.85,
        3: 0.95,
        4: 1.00,
        5: 1.05,
        6: 1.15,  # Summer rise
        7: 1.20,
        8: 1.15,
        9: 1.00,
        10: 1.05,
        11: 1.30, # Black Friday / pre-holiday
        12: 1.60, # Christmas spike
    }
    month_factor = monthly_factors.get(month, 1.0)
    return base_demand * dow_factor * month_factor


def generate_transactions(start_date="2024-01-01", days=365) -> pd.DataFrame:
    """Generate daily transaction records for all products."""
    records = []
    start = datetime.strptime(start_date, "%Y-%m-%d")

    for day_offset in range(days):
        current_date = start + timedelta(days=day_offset)

        for product in PRODUCTS:
            adjusted_lambda = add_seasonality(product["base_demand"], current_date)
            # Poisson makes demand "noisy" — not flat, not fake
            units_sold = max(0, np.random.poisson(lam=adjusted_lambda))

            records.append({
                "date":        current_date.strftime("%Y-%m-%d"),
                "product_id":  product["product_id"],
                "product_name": product["name"],
                "category":    product["category"],
                "units_sold":  units_sold,
                "unit_cost":   product["unit_cost"],
                "unit_price":  product["unit_price"],
                "revenue":     round(units_sold * product["unit_price"], 2),
                "cogs":        round(units_sold * product["unit_cost"], 2),
                "gross_profit": round(units_sold * (product["unit_price"] - product["unit_cost"]), 2),
            })

    return pd.DataFrame(records)


def generate_inventory_snapshot(transactions: pd.DataFrame) -> pd.DataFrame:
    """
    Simulate running inventory levels for each product.
    Starts each product at 600 units, replenishes when below 150.
    """
    snapshots = []
    
    for product in PRODUCTS:
        pid = product["product_id"]
        supplier_id = PRODUCT_SUPPLIER_MAP[pid]
        supplier = next(s for s in SUPPLIERS if s["supplier_id"] == supplier_id)

        product_tx = transactions[transactions["product_id"] == pid].copy()
        product_tx = product_tx.sort_values("date").reset_index(drop=True)

        stock = 600
        reorder_point = 150
        order_qty = 400
        pending_order_arrival = None

        for _, row in product_tx.iterrows():
            # Check if a pending order arrived today
            if pending_order_arrival and row["date"] >= pending_order_arrival:
                stock += order_qty
                pending_order_arrival = None

            stock -= row["units_sold"]
            stock = max(0, stock)  # floor at 0

            stockout = 1 if stock == 0 else 0

            # Trigger reorder if below ROP and no pending order
            if stock <= reorder_point and pending_order_arrival is None:
                lead = supplier["lead_time_days"]
                # Add noise: sometimes ships are delayed
                if np.random.random() > supplier["reliability"]:
                    lead += np.random.randint(2, 7)
                arrival_date = (
                    datetime.strptime(row["date"], "%Y-%m-%d") + timedelta(days=lead)
                ).strftime("%Y-%m-%d")
                pending_order_arrival = arrival_date

            snapshots.append({
                "date":             row["date"],
                "product_id":       pid,
                "closing_stock":    stock,
                "stockout_flag":    stockout,
                "reorder_triggered": 1 if pending_order_arrival == row.get("date") else 0,
                "supplier_id":      supplier_id,
                "lead_time_days":   supplier["lead_time_days"],
            })

    return pd.DataFrame(snapshots)


def generate_supplier_table() -> pd.DataFrame:
    return pd.DataFrame(SUPPLIERS)


def generate_product_table() -> pd.DataFrame:
    return pd.DataFrame(PRODUCTS)


# ─────────────────────────────────────────────
# MAIN: Run and save all datasets
# ─────────────────────────────────────────────
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out, exist_ok=True)

    print("⚙️  Generating transactions...")
    tx = generate_transactions()
    tx.to_csv(f"{out}/transactions.csv", index=False)
    print(f"   ✅ transactions.csv  → {len(tx):,} rows")

    print("⚙️  Generating inventory snapshots...")
    inv = generate_inventory_snapshot(tx)
    inv.to_csv(f"{out}/inventory.csv", index=False)
    print(f"   ✅ inventory.csv     → {len(inv):,} rows")

    print("⚙️  Saving reference tables...")
    generate_supplier_table().to_csv(f"{out}/suppliers.csv", index=False)
    generate_product_table().to_csv(f"{out}/products.csv", index=False)
    print("   ✅ suppliers.csv & products.csv saved")

    print("\n📦 ResilioChain Phase 1 Complete!")
    print(f"   Total revenue simulated: ${tx['revenue'].sum():,.2f}")
    print(f"   Total stockout events:   {inv['stockout_flag'].sum()}")
    print(f"   Date range: {tx['date'].min()} → {tx['date'].max()}")
