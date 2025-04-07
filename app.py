from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

project_data = {
    "project1": {
        "available": 10,
        "checked_out": 0,
        "users": []
    },
    "project2": {
        "available": 10,
        "checked_out": 0,
        "users": []
    }
}

@app.route('/')
def index():
    return jsonify(project_data) 

@app.get('/checkin/<project_id>/<int:qty>')
def checkIn_hardware(project_id, qty):
    if project_id not in project_data:
        return jsonify({"error": "Project ID not found"}), 404
    
    if qty <= 0:
        return jsonify({"error": "Quantity must be greater than 0"}), 400
    
    if project_data[project_id]['checked_out'] < qty:
        return jsonify({"error": "Not enough hardware checked out"}), 400
    
    project_data[project_id]['checked_out'] -= qty
    project_data[project_id]['available'] += qty

    return jsonify({"message": f"{qty} hardware checked in"}), 200

@app.get('/checkout/<project_id>/<int:qty>')
def checkOut_hardware(project_id, qty):
    if project_id not in project_data:
        return jsonify({"error": "Project ID not found"}), 404

    if qty <= 0:
        return jsonify({"error": "Quantity must be greater than 0"}), 400
    
    if project_data[project_id]['available'] < qty:
        return jsonify({"error": "Not enough hardware available"}), 400
    
    project_data[project_id]['checked_out'] += qty
    project_data[project_id]['available'] -= qty

    return jsonify({"message": f"{qty} hardware checked out"}), 200

@app.get('/join/<project_id>')
def joinProject(project_id):
    if project_id not in project_data:
        return jsonify({"error": "Project ID not found"}), 404
    
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if user_id in project_data[project_id]['users']:
        return jsonify({"error": "User in the project"}), 400
    
    project_data[project_id]['users'].append(user_id)

    return jsonify({"message": f"Joined {project_id}"}), 200

@app.get('/leave/<project_id>')
def leaveProject(project_id):

    if project_id not in project_data:
        return jsonify({"error": "Project ID not found"}), 404
    
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if user_id not in project_data[project_id]['users']:
        return jsonify({"error": "User not in the project"}), 400
    
    project_data[project_id]['users'].remove(user_id)

    return jsonify({"message": f"Left {project_id}"}), 200