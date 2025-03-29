from flask import Flask, jsonify
from flask_cors import CORS
from main import main as get_flight_details
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return jsonify({
        'status': 'running',
        'message': 'Flight Search API is running',
        'endpoints': {
            '/api/trigger': 'GET - Trigger flight search'
        }
    })

@app.route('/api/trigger', methods=['GET'])
def trigger_flight_search():
    try:
        # Call the main function to get flight details
        result = get_flight_details()
        print("result is...." + str(result))
        
        # Ensure result is a dictionary
        if not isinstance(result, dict):
            result = {'data': result}
            
        # Add status field
        result['status'] = 'success'
        return jsonify(result)
    except Exception as e:
        print(f"Error in trigger_flight_search: {str(e)}")
        print("Full traceback:")
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested URL was not found on the server.'
    }), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000) 