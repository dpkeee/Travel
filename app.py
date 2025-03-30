from flask import Flask, jsonify
from main import main
from flight_checker import format_flights_html

app = Flask(__name__)

@app.route('/')
def home():
    return "Flight Finder API is running"

@app.route('/api/trigger')
def trigger():
    try:
        # Call main() instead of get_flights()
        print('am here 1')
        result = main()
        print('am here 2')
        print('result in apppy is...', result)
        # Format the result as HTML
        html_content = format_flights_html(result)
        print('am here 3')
        print('html_content', html_content)
        print('am here 4')
        return jsonify({
            'success': True,
            'html': html_content
        })
        
    except Exception as e:
        print(f"Error in /api/trigger: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True) 