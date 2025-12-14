from flask import Flask, render_template
import random



app = Flask(__name__)


@app.route('/')
def index():
    # Revenue data - update these values with your actual data/logic
    revenue_data = {
        'total_revenue': 2151248,
        'daily_revenue': 12420,
        'chart_labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
        'chart_values': [0, 50000, 150000, 350000, 650000, 1100000, 1500000, 2151656]
    }
    
    return render_template("index.html", **revenue_data)


if __name__ == '__main__':
    app.run(debug=True)
