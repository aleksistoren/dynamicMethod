from typing import Dict

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Dummy storage for method code
methods = {
    #"example_method": "def example_method(d: Dict):\n    print('Hello, World!')\n"
    "example_method": '''def example_method(d: dict):
    res = []
    for key, val in d.items():
        res.append(f'{key}: {val}')
    
    return res''',
    "example_method2": '''def example_method(d: dict):
    res = []
    for key, val in d.items():
        res.append(f'{key} -> {val}')

    return res''',

}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_method/<method_name>', methods=['GET'])
def get_method(method_name):
    code = methods.get(method_name, "Method not found.")
    return jsonify({"code": code})


@app.route('/save_method/<method_name>', methods=['POST'])
def save_method(method_name):
    code = request.json.get('code')
    methods[method_name] = code
    return jsonify({"message": "Method saved successfully."})

@app.route('/execute_code', methods=['POST'])
def execute_code():
    data = request.json
    code = data['code'] + '\nresult = example_method(input_dict)'  # Ensure 'result' is being set
    input_dict = data['input_dict']
    try:
        local_namespace = {'input_dict': input_dict}
        exec(code, {}, local_namespace)
        result = local_namespace.get('result', 'No result returned.')
        return jsonify({'result': str(result)})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_method_names', methods=['GET'])
def get_method_names():
    return jsonify(list(methods.keys()))


if __name__ == '__main__':
    app.run(debug=True)
