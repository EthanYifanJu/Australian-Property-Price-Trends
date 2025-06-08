from flask import Flask, render_template, request
from retrieve import DataProcessor

app = Flask(__name__)

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
        dp.fetch_data(measure, property_type, region, start_period, end_period)
        df = dp.process_data()
        graph_html = dp.visualise_data(df)

    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
