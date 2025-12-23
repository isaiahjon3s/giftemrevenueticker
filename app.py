from flask import Flask, render_template


app = Flask(__name__)

# Pre-generate ALL revenue data with exponential growth (fixed values that never change)
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Generate labels for 6 years (enough for 60 base + 10 additional months)
ALL_LABELS = ['Start']
for y in range(1, 7):
    for m in MONTHS:
        ALL_LABELS.append(f"{m} Y{y}")

# Generate growth values with natural variation - FIXED and never recalculated
# Base exponential trend with realistic month-to-month fluctuations
import random
random.seed(42)  # Fixed seed so values are consistent across restarts

BASE_GROWTH = 1.055  # Base 5.5% monthly growth
ALL_VALUES = [0]  # Start at 0
current_value = 0

for i in range(1, 71):  # Generate 70 months of data
    # Base exponential growth with seasonal and random variation
    base_increase = current_value * (BASE_GROWTH - 1) + 45000
    
    # Add seasonal patterns (Q4 tends to be stronger, Q1 slower)
    month_in_year = (i - 1) % 12
    if month_in_year in [9, 10, 11]:  # Oct, Nov, Dec - holiday boost
        seasonal = 1.15 + random.uniform(0, 0.1)
    elif month_in_year in [0, 1]:  # Jan, Feb - post-holiday dip
        seasonal = 0.85 + random.uniform(0, 0.1)
    elif month_in_year in [5, 6]:  # Jun, Jul - summer slowdown
        seasonal = 0.92 + random.uniform(0, 0.08)
    else:
        seasonal = 1.0 + random.uniform(-0.05, 0.1)
    
    # Apply variation but ensure we always grow overall
    increase = max(base_increase * seasonal, 20000)
    current_value = int(current_value + increase)
    ALL_VALUES.append(current_value)

def get_revenue_data(additional_months):
    """Get revenue data showing 60 + additional_months of data.
    Historical values are always the same - only new months are added."""
    num_points = 61 + additional_months  # 60 months + 'Start' + additional
    chart_labels = ALL_LABELS[:num_points]
    chart_values = ALL_VALUES[:num_points]
    
    # Calculate daily revenue from the most recent month's growth
    monthly_growth = chart_values[-1] - chart_values[-2] if len(chart_values) > 1 else 0
    daily_revenue = monthly_growth // 30
    
    return {
        'total_revenue': chart_values[-1],
        'daily_revenue': daily_revenue,
        'chart_labels': chart_labels,
        'chart_values': chart_values
    }

@app.route('/', defaults={'num': None})
@app.route('/<num>')
def dynamic_index(num):
    try:
        months = int(num)
    except (TypeError, ValueError):
        months = 0
    return render_template("index.html", **get_revenue_data(months))
    
if __name__ == '__main__':
    app.run(debug=True)
