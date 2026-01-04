# Project 2: Digital Twin with Analytics

This project demonstrates **Digital Twin Simulation** with **Four Types of Analytics**.

## Overview

Simulates multi-store, multi-product inventory operations using a digital twin approach and provides comprehensive analytics to understand, diagnose, predict, and optimize store performance.

## Features

- **Multi-Store Simulation:**
  - Multiple stores (Store1, Store2, Store3)
  - Multiple products (ProductA, ProductB, ProductC)
  - Date-based simulation

- **Scenario Testing:**
  - Normal demand scenarios
  - High demand scenarios (stress testing)
  - Configurable reorder points

- **Four Types of Analytics:**
  1. **Descriptive Analytics** - What happened?
  2. **Diagnostic Analytics** - Why did it happen?
  3. **Predictive Analytics** - What will happen?
  4. **Prescriptive Analytics** - What should we do?

## Project Structure

```
Project2_Digital_Twin_Analytics/
├── src/
│   └── digital_twin_analytics/
│       ├── __init__.py
│       ├── digital_twin.py      # Digital twin simulation engine
│       └── analytics.py          # Analytics engine
├── data/
│   └── sample_store_data.csv     # Sample data (auto-generated)
├── test_digital_twin_analytics.py   # Test script
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run the Test

```bash
python test_digital_twin_analytics.py
```

This will:
1. Generate sample store data (if not exists)
2. Run simulation with normal demand
3. Apply all 4 analytics types
4. Test with increased demand (50% increase)
5. Compare scenarios

### Use in Your Code

```python
from digital_twin_analytics import SimpleDigitalTwin, DigitalTwinAnalytics

# Load data
twin = SimpleDigitalTwin.from_csv("data/sample_store_data.csv")

# Run simulation
result = twin.run_simulation(demand_multiplier=1.0, reorder_point=60.0)

# Apply analytics
analytics = DigitalTwinAnalytics(result.store_data)
analytics.descriptive()    # What happened?
analytics.diagnostic()      # Why did it happen?
analytics.predictive()       # What will happen?
analytics.prescriptive()    # What should we do?
```

## Data Format

The CSV file should have the following columns:
- `store_name`: Store identifier
- `date`: Date of record
- `inventory_ProductA`, `inventory_ProductB`, `inventory_ProductC`: Stock levels
- `demand_ProductA`, `demand_ProductB`, `demand_ProductC`: Daily demand

## Analytics Output

### 1. Descriptive Analytics
- Total stockout days
- Average stockouts per day
- Average fill rate
- Total sales
- Top stores by stockouts
- Stockouts by product

### 2. Diagnostic Analytics
- Days with most stockouts
- Store performance analysis
- Product performance analysis
- Root cause identification

### 3. Predictive Analytics
- High-risk store identification
- Trend analysis (increasing/decreasing/stable)
- Overall stockout risk assessment
- Future stockout predictions

### 4. Prescriptive Analytics
- Store-specific recommendations
- Product-specific recommendations
- Reorder point suggestions
- Demand forecasting improvements
- Safety stock recommendations

## Example Output

```
============================================================
DESCRIPTIVE ANALYTICS - What Happened?
============================================================

Total Stockout Days: 36
Average Stockouts per Day: 0.40
Average Fill Rate: 98.71%
Total Sales: 5400.00 units

Top 5 Stores by Stockouts:
  Store3: 36 stockout days
  Store1: 0 stockout days
  Store2: 0 stockout days
...
```

## Simulation Parameters

- `demand_multiplier`: Multiplier for demand (1.0 = normal, 1.5 = 50% increase)
- `reorder_point`: Stock level that triggers reorder flag

## Scenario Testing

### Normal Demand
```python
result = twin.run_simulation(demand_multiplier=1.0, reorder_point=60.0)
```

### High Demand (Stress Test)
```python
result = twin.run_simulation(demand_multiplier=1.5, reorder_point=60.0)
```

### Different Reorder Points
```python
result = twin.run_simulation(demand_multiplier=1.0, reorder_point=80.0)
```

## Notes

- This is a **deterministic** simulation (no randomness)
- Results are reproducible with same parameters
- Analytics work with any digital twin simulation results DataFrame
- Sample data is automatically generated if not provided

