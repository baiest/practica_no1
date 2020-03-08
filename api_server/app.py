import json
from flask import Flask
from flask import request, jsonify
from strategies import alg_first_fit

app = Flask(__name__)

@app.route("/")
def hello_world():
    return 'Helloadadadkalhdkll!!'

algorithms = {'firstfit':alg_first_fit, 'nextfit':None,
			  'bestfit':None, 'worstfit':None }
response = {}


@app.route('/api/v1/status', methods=['GET'])
def get_status():
   global response
   return jsonify(response)

@app.route('/api/v1/mem', methods=['POST'])
def sched_process():
	if not request.json:
		return {"error": "Invalid data"}, 400
	data = request.json

	algorithm = data['algorithm'] if (data['algorithm'] in algorithms) else 'firstfit'
	algorithm = algorithms.get(algorithm)
	data = algorithm(data)

	response = data
	return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)
