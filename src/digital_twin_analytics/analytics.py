"""
Digital Twin Analytics

Provides four types of analytics for digital twin simulation data:
1. Descriptive - What happened?
2. Diagnostic - Why did it happen?
3. Predictive - What will happen?
4. Prescriptive - What should we do?
"""

import pandas as pd


class DigitalTwinAnalytics:
    """Analytics for digital twin simulation data."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with digital twin simulation DataFrame.
        
        Expected columns: store_name, date, sales_*, stockout_*, fill_rate_*
        """
        self.df = data.copy()
    
    def descriptive(self) -> None:
        """Descriptive Analytics: What happened?"""
        print("\n" + "="*60)
        print("DESCRIPTIVE ANALYTICS - What Happened?")
        print("="*60)
        
        # Get stockout and fill rate columns
        stockout_cols = [c for c in self.df.columns if c.startswith('stockout_')]
        fill_rate_cols = [c for c in self.df.columns if c.startswith('fill_rate_')]
        sales_cols = [c for c in self.df.columns if c.startswith('sales_')]
        
        # Calculate total stockouts
        if stockout_cols:
            total_stockouts = self.df[stockout_cols].sum().sum()
            avg_per_day = self.df[stockout_cols].sum(axis=1).mean()
            print(f"\n Total Stockout Days: {total_stockouts}")
            print(f" Average Stockouts per Day: {avg_per_day:.2f}")
        
        # Calculate average fill rate
        if fill_rate_cols:
            avg_fill_rate = self.df[fill_rate_cols].mean().mean()
            print(f" Average Fill Rate: {avg_fill_rate:.2%}")
        
        # Calculate total sales
        if sales_cols:
            total_sales = self.df[sales_cols].sum().sum()
            print(f" Total Sales: {total_sales:.2f} units")
        
        # Top stores by stockouts
        if stockout_cols and 'store_name' in self.df.columns:
            print("\n Top 5 Stores by Stockouts:")
            store_totals = self.df.groupby('store_name')[stockout_cols].sum().sum(axis=1)
            top_stores = store_totals.sort_values(ascending=False).head()
            for store, count in top_stores.items():
                print(f"  {store}: {count} stockout days")
        
        # Product-level summary
        if stockout_cols:
            print("\n Stockouts by Product:")
            for col in stockout_cols:
                product = col.replace('stockout_', '')
                product_stockouts = self.df[col].sum()
                print(f"  {product}: {product_stockouts} stockout days")
    
    def diagnostic(self) -> None:
        """Diagnostic Analytics: Why did it happen?"""
        print("\n" + "="*60)
        print("DIAGNOSTIC ANALYTICS - Why Did It Happen?")
        print("="*60)
        
        stockout_cols = [c for c in self.df.columns if c.startswith('stockout_')]
        
        if not stockout_cols or 'date' not in self.df.columns:
            print("\n No date-based data available for analysis")
            return
        
        # Find days with most stockouts
        daily_stockouts = self.df.groupby('date')[stockout_cols].sum().sum(axis=1)
        worst_days = daily_stockouts.sort_values(ascending=False).head(5)
        
        print("\n Days with Most Stockouts:")
        for date, count in worst_days.items():
            print(f"  {date}: {count} stockouts")
        
        # Store-level analysis
        if 'store_name' in self.df.columns:
            print("\n Store Performance Analysis:")
            store_stockouts = self.df.groupby('store_name')[stockout_cols].sum().sum(axis=1)
            worst_store = store_stockouts.idxmax()
            worst_count = store_stockouts.max()
            print(f"  Worst performing store: {worst_store} ({worst_count} stockout days)")
            
            if len(store_stockouts) > 1:
                best_store = store_stockouts.idxmin()
                best_count = store_stockouts.min()
                print(f"  Best performing store: {best_store} ({best_count} stockout days)")
        
        # Product-level analysis
        print("\n Product Performance Analysis:")
        for col in stockout_cols:
            product = col.replace('stockout_', '')
            product_stockouts = self.df[col].sum()
            if 'store_name' in self.df.columns:
                worst_store_for_product = self.df.groupby('store_name')[col].sum().idxmax()
                worst_count_for_product = self.df.groupby('store_name')[col].sum().max()
                print(f"  {product}: {product_stockouts} total stockouts")
                print(f"    Worst store: {worst_store_for_product} ({worst_count_for_product} stockouts)")
    
    def predictive(self) -> None:
        """Predictive Analytics: What will happen?"""
        print("\n" + "="*60)
        print("PREDICTIVE ANALYTICS - What Will Happen?")
        print("="*60)
        
        stockout_cols = [c for c in self.df.columns if c.startswith('stockout_')]
        fill_rate_cols = [c for c in self.df.columns if c.startswith('fill_rate_')]
        
        if not stockout_cols:
            print("\n Insufficient data for predictions")
            return
        
        # Analyze each product
        for col in stockout_cols:
            product = col.replace('stockout_', '')
            
            if 'store_name' in self.df.columns:
                # Group by store and check trend
                store_stockouts = self.df.groupby('store_name')[col].sum()
                avg_stockouts = store_stockouts.mean()
                high_risk_stores = store_stockouts[store_stockouts > avg_stockouts]
                
                if len(high_risk_stores) > 0:
                    print(f"\n {product}: High-risk stores (above average stockouts):")
                    for store, count in high_risk_stores.items():
                        print(f"  - {store}: {count} stockouts (likely to continue)")
                else:
                    print(f"\n {product}: Stockout patterns are stable across all stores")
            else:
                # Simple trend: compare first half vs second half
                mid_point = len(self.df) // 2
                first_half = self.df[col].iloc[:mid_point].sum()
                second_half = self.df[col].iloc[mid_point:].sum()
                
                if second_half > first_half * 1.2:
                    print(f"\n {product}: Stockouts are increasing (trend: {first_half} → {second_half})")
                elif first_half > second_half * 1.2:
                    print(f"\n {product}: Stockouts are decreasing (trend: {first_half} → {second_half})")
                else:
                    print(f"\n {product}: Stockout trend is stable")
        
        # Overall prediction
        if 'store_name' in self.df.columns:
            total_stockouts = self.df[stockout_cols].sum().sum()
            num_stores = self.df['store_name'].nunique()
            num_days = self.df['date'].nunique()
            avg_stockouts_per_store_per_day = total_stockouts / (num_stores * num_days)
            
            print(f"\n Overall Prediction:")
            print(f"  Average stockouts per store per day: {avg_stockouts_per_store_per_day:.2f}")
            if avg_stockouts_per_store_per_day > 0.3:
                print("  → High stockout risk - immediate action recommended")
            elif avg_stockouts_per_store_per_day > 0.1:
                print("  → Moderate stockout risk - monitor closely")
            else:
                print("  → Low stockout risk - current policy appears adequate")
    
    def prescriptive(self, threshold: float = 0.1) -> None:
        """Prescriptive Analytics: What should we do?"""
        print("\n" + "="*60)
        print("PRESCRIPTIVE ANALYTICS - What Should We Do?")
        print("="*60)
        
        # Get only actual stockout columns (not lagged ones)
        stockout_cols = [c for c in self.df.columns 
                        if c.startswith('stockout_') and not c.endswith('_lag1')]
        
        if not stockout_cols:
            print("\n No stockout data available")
            return
        
        if 'store_name' not in self.df.columns:
            print("\n Store-level recommendations require store_name column")
            return
        
        # Calculate stockout rate per store per product
        store_performance = self.df.groupby('store_name')[stockout_cols].mean()
        
        print("\n Store Recommendations:")
        
        for col in stockout_cols:
            product = col.replace('stockout_', '')
            problem_stores = store_performance[store_performance[col] > threshold]
            
            if len(problem_stores) > 0:
                print(f"\n  Product: {product}")
                print(f" Stores needing attention (stockout rate > {threshold:.0%}):")
                for store, rate in problem_stores[col].items():
                    print(f"    - {store}: {rate:.2%} stockout rate")
                    print(f"      → Increase reorder point for {product}")
                    print(f"      → Review demand forecasting for {store}")
                    print(f"      → Consider increasing safety stock")
            else:
                print(f"\n  Product: {product}")
                print(f"  ✓ All stores performing well")
        
        # Overall recommendations
        overall_stockout_rate = self.df[stockout_cols].mean().mean()
        if overall_stockout_rate > threshold:
            print(f"\n Overall Recommendation:")
            print(f"  System-wide stockout rate ({overall_stockout_rate:.2%}) exceeds threshold")
            print(f"  → Review inventory policies across all stores")
            print(f"  → Consider increasing base stock levels")
            print(f"  → Implement demand forecasting improvements")

