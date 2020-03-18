from datetime import datetime, date, timedelta
import Week12_own_assignment as facade
#!flask/bin/python
from flask import Flask, jsonify, abort, request


# start_date = date(2006, 1, 1)
# end_date = date(2006, 1, 2)
# print(facade.get_specific_crime_data_as_dict(start_date, end_date))

app = Flask(__name__)

@app.route('/api/crimes', methods=['GET'])
def get_crimes():
    try :
        start_date_string = request.args.get('start-date')
        start_date = datetime.strptime(start_date_string, '%Y-%m-%d').date()
        end_date_string = request.args.get('end-date')
        end_date = datetime.strptime(end_date_string, '%Y-%m-%d').date()
        crimedata = facade.get_specific_crime_data_as_dict(start_date, end_date)
        return jsonify({'crimes_in_period': crimedata["Amount_of_crimes_in_period"]})
    except :
        return jsonify({"message": "Failed to get data. Please make sure you provide the correct parameters"})


@app.route('/api/crimes', methods=['POST'])
def get_burglaries():
    if not request.json or not 'key' in request.json:
        abort(400)
    key = {
        'key': request.json['key'],
    }
    if not (key["key"] == "secret"):
        abort(400)
    data = facade.get_total_amount_of_burglaries()
    return jsonify({"Total_amount_of_burglaries": data}), 200

if __name__ == '__main__':
    app.run(debug=True)
