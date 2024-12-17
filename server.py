from flask import Flask, request, jsonify
from gcms import GCMS
from object import Color

app = Flask(__name__)
gcms = GCMS()

@app.route('/add_bin', methods=['POST'])
def add_bin():
    data = request.json
    bin_id = data['bin_id']
    capacity = data['capacity']
    gcms.add_bin(bin_id, capacity)
    return jsonify({"message": "Bin added successfully", "bin_id": bin_id})

@app.route('/add_object', methods=['POST'])
def add_object():
    data = request.json
    object_id = data['object_id']
    size = data['size']
    color = Color[data['color']]
    try:
        gcms.add_object(object_id, size, color)
        return jsonify({"message": "Object added successfully", "object_id": object_id})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/bin_info/<int:bin_id>', methods=['GET'])
def bin_info(bin_id):
    info = gcms.bin_info(bin_id)
    if info:
        return jsonify({"remaining_capacity": info[0], "objects": info[1]})
    else:
        return jsonify({"error": "Bin not found"})

@app.route('/object_info/<int:object_id>', methods=['GET'])
def object_info(object_id):
    parent_id = gcms.object_info(object_id)
    if parent_id is not None:
        return jsonify({"object_id": object_id, "bin_id": parent_id})
    else:
        return jsonify({"error": "Object not found"})

if __name__ == '__main__':
    app.run(debug=True)
