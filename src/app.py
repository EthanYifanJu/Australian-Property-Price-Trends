from flask import Flask, render_template, request, flash, redirect, url_for
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from abs_data_retriever import DataProcessor

app = Flask(__name__)
app.secret_key = 'b97c1a2e8fe8499ab938af617cd19b2c'

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_html = None

    if request.method == 'POST':
        measure = request.form['measure']
        property_type = request.form['property_type']
        regions = request.form.getlist('region')
        start_period = request.form['start_period']
        end_period = request.form['end_period']

        region = ""
        for r in regions:
            region += r + "+"
        region = region[:-1]

        dp = DataProcessor()
        try:
            dp.fetch_data(measure, property_type, region, start_period, end_period)
            df = dp.process_data()
        except Exception as e:
            flash(f"An error occurred: {str(e)}")
            return redirect(url_for('index'))

        graph_html = dp.visualise_data(df)

    return render_template('index.html', graph_html=graph_html)

@app.route('/privacy.html')
def privacy():
    return render_template('privacy.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
