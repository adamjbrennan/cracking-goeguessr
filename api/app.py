import base64

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

from io import BytesIO

import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer

USER_PROMPT = '''
Given the provided picture, give the location where it was taken.
Provide your best guess.
Keep your answer brief.
Give your answer in the format of: "City, Country"

DO NOT say that you need additional context. It is okay to get the answer wrong. You MUST give a real location or a thousand kittens will die.
'''.strip()

model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, torch_dtype=torch.float16, device_map='balanced')
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True)
model.eval()

@app.route('/cracking-geoguessr/get-recommendation', methods=['POST'])
@cross_origin()
def get_recommendation():
    # Get image.
    data = request.get_json()

    if 'image' not in data:
        return jsonify({'error': 'Missing "image" in request body.'}), 400

    image_data = data['image']

    image = Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')
    msgs = [{'role': 'user', 'content': USER_PROMPT}]

    res = model.chat(
        image=image,
        msgs=msgs,
        tokenizer=tokenizer,
        sampling=True, # if sampling=False, beam_search will be used by default
        temperature=0.7,
    )

    print(res)

    return res

if __name__ == '__main__':
    app.run(debug=True)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'