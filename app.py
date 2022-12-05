from flask import Flask, jsonify

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

import pandas as pd
from Preprocessing import preprocess 

app,json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API Deployment'),
        'Version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API Binar Quiz')
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "header": [],
    'specs': [
        {
            "endpoint": 'dokumentasi',
            "route" :'/docs.json'
        }
    ],
    "statistic_url_path": "flasgger_statistic",
    "swagger_ui": True,
    "specs_route": "/dokumentasi"
}
swagger = Swagger(app,template=swagger_template,config=swagger_config)

@swag_from("template/text_processing.yml", methods=['POST'])
@app.route('text-preprocessing', methods=['POST'])
def text_preprocessing():
    text_=request.form.get('text')

    df = pd.DataFrame([{'text': text_}])
    print (df)

    df_clean = preprocess(df,'text')
    print(df_clean)

    json_response = {
        'status_code': 200, 
        'data': df_clean['clean'][0]
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
    app.run()