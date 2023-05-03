from dotenv import load_dotenv
import requests
import json
import os
from flask import Flask, render_template, request

load_dotenv()

api_key = os.environ.get('API_KEY')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q')

    response = requests.post('https://stablediffusionapi.com/api/v3/text2img', json={
        "key": api_key,
        "prompt": query,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "guidance_scale": 7.5,
    })

    if response.status_code == 200:
        results = json.loads(response.content)
        image_urls = results['output']
        images = []
        for url in image_urls:
            images.append(url)
        return render_template('results.html', images=images)
    else:
        return 'Error en la solicitud de búsqueda.'

if __name__ == '__main__':
    app.run(debug=True)