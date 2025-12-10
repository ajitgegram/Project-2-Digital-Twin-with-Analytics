"""
Test Digital Twin Analytics

This script tests all four types of analytics for digital twin simulation:
1. Descriptive Analytics
2. Diagnostic Analytics
3. Predictive Analytics
4. Prescriptive Analytics
"""

import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from digital_twin_analytics import SimpleDigitalTwin, DigitalTwinAnalytics


def generate_sample_data(output_path: str = "data/sample_store_data.csv"):
    """
    Generate sample store data for testing.
    
    Creates a simple dataset with:
    - 3 stores
    - 30 days of data
    - 3 products (ProductA, ProductB, ProductC)
    """
    stores = ['Store1', 'Store2', 'Store3']
    products = ['ProductA', 'ProductB', 'ProductC']
    
    # Create date range
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(30)]
    
    data = []
    for date in dates:
        for store in stores:
            row = {
                'store_name': store,
                'date': date
            }
            
            # Generate inventory and demand for each product
            for product in products:
                # Vary inventory and demand by store and day
                base_inv = 100 if store == 'Store1' else 80 if store == 'Store2' else 60
                base_demand = 20 if store == 'Store1' else 25 if store == 'Store2' else 30
                
                # Add some variation
                day_factor = (date.day % 10) / 10
                inventory = int(base_inv * (1 - day_factor * 0.3))
                demand = int(base_demand * (1 + day_factor * 0.2))
                
                row[f'inventory_{product}'] = max(0, inventory)
                row[f'demand_{product}'] = max(1, demand)
            
            data.append(row)
    
    df = pd.DataFrame(data)
    
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"✓ Generated sample data: {output_path}")
    print(f"  - {len(df)} records")
    print(f"  - {len(stores)} stores")
    print(f"  - {len(dates)} days")
    
    return df


def test_analytics():
    """Test all four analytics types."""
    
    print("="*70)
    print("DIGITAL TWIN ANALYTICS TEST")
    print("="*70)
    
    # Step 1: Generate or load data
    data_path = "data/sample_store_data.csv"
    if not os.path.exists(data_path):
        print("\n📊 Generating sample data...")
        generate_sample_data(data_path)
    else:
        print(f"\n📊 Loading data from {data_path}...")
    
    # Step 2: Load data into Digital Twin
    print("\n🔧 Initializing Digital Twin...")
    twin = SimpleDigitalTwin.from_csv(data_path)
    print(f"  ✓ Loaded {len(twin.store_data)} records")
    
    # Step 3: Run simulation - Normal Demand
    print("\n⚙️  Running simulation (Normal Demand)...")
    print("  Parameters:")
    print("    - Demand multiplier: 1.0 (normal)")
    print("    - Reorder point: 60 units")
    
    result = twin.run_simulation(demand_multiplier=1.0, reorder_point=60.0)
    print(f"  ✓ Simulation complete: {len(result.store_data)} results")
    
    # Step 4: Apply Analytics
    print("\n📈 Applying Analytics...")
    analytics = DigitalTwinAnalytics(result.store_data)
    
    # 4.1 Descriptive Analytics
    analytics.descriptive()
    
    # 4.2 Diagnostic Analytics
    analytics.diagnostic()
    
    # 4.3 Predictive Analytics
    analytics.predictive()
    
    # 4.4 Prescriptive Analytics
    analytics.prescriptive(threshold=0.1)
    
    print("\n" + "="*70)
    print("✓ All analytics tests completed successfully!")
    print("="*70)
    
    # Step 5: Test with increased demand
    print("\n" + "="*70)
    print("TESTING WITH INCREASED DEMAND (50% increase)")
    print("="*70)
    
    print("\n⚙️  Running simulation with 50% demand increase...")
    result2 = twin.run_simulation(demand_multiplier=1.5, reorder_point=60.0)
    analytics2 = DigitalTwinAnalytics(result2.store_data)
    
    print("\n📊 Descriptive Analytics (High Demand Scenario):")
    analytics2.descriptive()
    
    print("\n💡 Prescriptive Analytics (High Demand Scenario):")
    analytics2.prescriptive(threshold=0.15)
    
    # Comparison
    print("\n" + "="*70)
    print("COMPARISON: NORMAL vs HIGH DEMAND")
    print("="*70)
    
    stockout_cols = [c for c in result.store_data.columns if c.startswith('stockout_')]
    stockout_cols2 = [c for c in result2.store_data.columns if c.startswith('stockout_')]
    
    normal_stockouts = result.store_data[stockout_cols].sum().sum() if stockout_cols else 0
    high_stockouts = result2.store_data[stockout_cols2].sum().sum() if stockout_cols2 else 0
    
    print(f"\n📊 Normal Demand Scenario:")
    print(f"  Total Stockout Days: {normal_stockouts}")
    
    print(f"\n📊 High Demand Scenario (50% increase):")
    print(f"  Total Stockout Days: {high_stockouts}")
    
    if high_stockouts > normal_stockouts:
        increase = ((high_stockouts - normal_stockouts) / normal_stockouts * 100) if normal_stockouts > 0 else 0
        print(f"\n  ⚠️  Stockouts increased by {increase:.1f}%")
        print("  → Recommendation: Increase reorder points or safety stock")
    
    print("\n" + "="*70)
    print("✓ All tests completed!")
    print("="*70)


if __name__ == "__main__":
    test_analytics()

