from flask import Flask, jsonify, abort
import pandas as pd

app = Flask(__name__)

def load_data():
    data = pd.read_csv('vacunacion_panama.csv', skiprows=4)
    return data[data['Country Name'] == 'Panama'].iloc[0].to_dict()

panama_data = load_data()

@app.route('/api/vaccination', methods=['GET'])
def get_all_data():
    return jsonify(panama_data)

@app.route('/api/vaccination/<int:year>', methods=['GET'])
def get_data_by_year(year):
    year_str = str(year)
    if year_str in panama_data:
        return jsonify({year_str: panama_data[year_str]})
    else:
        return jsonify({"error": "Año no encontrado"}), 404

@app.route('/api/vaccination/latest', methods=['GET'])
def get_latest_data():
    try:
        latest_year = max(int(year) for year in panama_data if year.isdigit() and panama_data[year] != '')
        return jsonify({str(latest_year): panama_data[str(latest_year)]})
    except ValueError:
        return jsonify({"error": "No hay datos disponibles"}), 404

@app.route('/api/vaccination/average', methods=['GET'])
def get_average():
    try:
        values = [float(value) for value in panama_data.values() if value != '' and value.replace('.', '', 1).isdigit()]
        if not values:
            raise ValueError("No hay valores válidos")
        average = sum(values) / len(values)
        return jsonify({"average": average})
    except ValueError:
        return jsonify({"error": "No se pudo calcular el promedio"}), 400

if __name__ == '__main__':
    app.run(debug=True)






















