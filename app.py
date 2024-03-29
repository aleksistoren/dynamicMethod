import ast
import inspect

from flask import Flask, request, jsonify, render_template

from method_controller import MethodController
from methods import example_method, example_method2

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_method/<method_name>', methods=['GET'])
def get_method(method_name):
    method_code = MethodController.get_method_code(method_name)
    if method_code:
        return jsonify({"code": method_code})
    else:
        return jsonify({"message": "Method not found."})


@app.route('/execute_code/<method_name>', methods=['POST'])
def execute_code(method_name):
    data = request.json
    method = MethodController.get_method(method_name)
    if method:
        try:
            result = method(data['input_dict'])
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({"error": "Method not found."})


@app.route('/get_method_names', methods=['GET'])
def get_method_names():
    return jsonify(list(MethodController.methods.keys()))


@app.route('/save_method/<method_name>', methods=['POST'])
def save_method(method_name):
    data = request.json
    initial_code = data.get('code')
    code = initial_code
    if code.startswith('@MethodController.get_current_version'):
        code = code[len('@MethodController.get_current_version'):]
    if code:
        try:
            MethodController.ignore_current = True
            namespace = globals().copy()
            exec(code, namespace)
            method = namespace[method_name]
            MethodController.methods[method_name] = method, initial_code
            MethodController.ignore_current = False
            return jsonify({"message": "Method saved successfully."})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "Code not provided."})


@app.route('/get_me', methods=['GET'])
def get_me():
    return example_method({"XXX": "YYY"})


if __name__ == '__main__':
    app.run(debug=True)
