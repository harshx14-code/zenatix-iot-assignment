from flask import Flask, jsonify
import csv

app = Flask(__name__)

def get_last_temperature():
    try:
        with open('temperature_data.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                last_row = rows[-1]
                return {'temperature': last_row[0], 'timestamp': last_row[1]}
            else:
                return {'error': 'No data available'}
    except FileNotFoundError:
        return {'error': 'Temperature data file not found'}

@app.route('/temperature', methods=['GET'])
def latest_temperature():
    last_temp = get_last_temperature()
    return jsonify(last_temp)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Temperature Server. Use /temperature to get the latest temperature."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)