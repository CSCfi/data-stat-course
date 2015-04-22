from flask import Flask, redirect
from flask.ext import restful
import json

app = Flask(__name__)
api = restful.Api(app)
results = dict(json.load(file("../datasets/lotto-2000.json")))


@app.route("/")
def index():
    return redirect("/api/", code=302)


class Base(restful.Resource):
    def get(self):
        return {
            '/api/round/<round>': {
                'description': 'Query Lotto results by *round*',
                'param_min': 520,
                'param_max': 1303
            }
        }


class Lotto(restful.Resource):
    def get(self, round):
        try:
            return {'status': 'ok', 'result': results[round]}
        except:
            return {'status': 'error', 'result': []}


api.add_resource(Base, '/api/')
api.add_resource(Lotto, '/api/round/<round>')

if __name__ == '__main__':
    app.run(debug=True)
