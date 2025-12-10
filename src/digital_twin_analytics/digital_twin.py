"""
Simple Digital Twin

Simulates store inventory operations with demand and stockout tracking.
"""

import pandas as pd
from typing import Optional
from dataclasses import dataclass


@dataclass
class SimulationResult:
    """Result from digital twin simulation."""
    store_data: pd.DataFrame


class SimpleDigitalTwin:
    """
    Simple digital twin for store inventory simulation.
    
    Simulates daily operations: demand, sales, stockouts, and fill rates.
    """
    
    def __init__(self, store_data: pd.DataFrame):
        """
        Initialize with store data.
        
        Expected columns:
        - store_name: Store identifier
        - date: Date of record
        - inventory_ProductA, inventory_ProductB, inventory_ProductC: Stock levels
        - demand_ProductA, demand_ProductB, demand_ProductC: Daily demand
        """
        self.store_data = store_data.copy()
        self.products = ['ProductA', 'ProductB', 'ProductC']
    
    @classmethod
    def from_csv(cls, csv_path: str) -> "SimpleDigitalTwin":
        """Load data from CSV file."""
        df = pd.read_csv(csv_path, parse_dates=['date'])
        return cls(df)
    
    def simulate_day(self, date: pd.Timestamp, 
                    demand_multiplier: float = 1.0,
                    reorder_point: float = 60.0) -> pd.DataFrame:
        """
        Simulate a single day's operations.
        
        Args:
            date: Date to simulate
            demand_multiplier: Multiplier for demand (1.0 = normal, 1.5 = 50% increase)
            reorder_point: Stock level that triggers reorder
        
        Returns:
            DataFrame with simulation results for that day
        """
        day_data = self.store_data[self.store_data['date'] == date].copy()
        
        if len(day_data) == 0:
            return pd.DataFrame()
        
        results = []
        
        for _, row in day_data.iterrows():
            store_name = row['store_name']
            result = {
                'store_name': store_name,
                'date': date
            }
            
            for product in self.products:
                inv_col = f'inventory_{product}'
                dem_col = f'demand_{product}'
                
                if inv_col not in row or dem_col not in row:
                    continue
                
                inventory = row[inv_col]
                demand = row[dem_col] * demand_multiplier
                
                # Calculate sales (can't sell more than available)
                sales = min(inventory, demand)
                
                # Stockout occurs if demand > inventory
                stockout = 1 if inventory < demand else 0
                
                # Fill rate = sales / demand
                fill_rate = sales / demand if demand > 0 else 1.0
                
                # Reorder flag
                reorder = 1 if inventory < reorder_point else 0
                
                result[f'sales_{product}'] = sales
                result[f'stockout_{product}'] = stockout
                result[f'fill_rate_{product}'] = fill_rate
                result[f'reorder_{product}'] = reorder
            
            results.append(result)
        
        return pd.DataFrame(results)
    
    def run_simulation(self, 
                      demand_multiplier: float = 1.0,
                      reorder_point: float = 60.0) -> SimulationResult:
        """
        Run simulation for all dates in the dataset.
        
        Args:
            demand_multiplier: Multiplier for demand
            reorder_point: Stock level that triggers reorder
        
        Returns:
            SimulationResult with store_data DataFrame
        """
        all_results = []
        dates = sorted(self.store_data['date'].unique())
        
        for date in dates:
            day_results = self.simulate_day(date, demand_multiplier, reorder_point)
            if len(day_results) > 0:
                all_results.append(day_results)
        
        if all_results:
            combined = pd.concat(all_results, ignore_index=True)
            return SimulationResult(store_data=combined)
        else:
            return SimulationResult(store_data=pd.DataFrame())

