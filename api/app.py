import base64
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route('/cracking-geoguessr/get-recommendation', methods=['POST'])
@cross_origin()
def get_recommendation():
    # Get image.
    data = request.get_json()

    if 'image' not in data:
        return jsonify({'error': 'Missing "image" in request body.'}), 400

    image = data['image']
    
    # Write image to file system for debugging purposes.
    file = open('mostRecent.png', 'wb') 
    file.write(base64.b64decode((image))) 
    file.close() 

    # Use model to get suggestion here.

    # Return suggestion.
    return 'Seattle, WA'

if __name__ == '__main__':
    app.run(debug=True)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'