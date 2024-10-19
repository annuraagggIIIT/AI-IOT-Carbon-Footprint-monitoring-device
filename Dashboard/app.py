from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

# Function to read data from gas.json
def read_data():
    with open('esp32/gas.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(read_data())

if __name__ == '__main__':
    app.run(debug=True, port=3000)
