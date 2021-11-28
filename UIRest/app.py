from flask.json import JSONEncoder

import numpy as np

import api

strategyApi= api.StrategyRunnerAPI()

# from config import ma, app, Base
# from config import sa


class ALGOEncoder(JSONEncoder):
    def default(self, obj):
        # print("type(obj), obj")
        # print(type(obj),obj)
        # if isinstance(obj, np.ndarray):
        #     return obj.tolist()
        # el
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8');

        return JSONEncoder.default(self, obj)

# @app.before_first_request
# def create_tables():
#     # sa.create_all()
#     # Base.metadata.drop_all(sa.engine)
#     Base.metadata.create_all(sa.engine)
#     # test.testceate()
#     # entities.init_db()



if __name__ == '__main__':
    # sa.init_app(app)
    # ma.init_app(app)
    app.json_encoder = ALGOEncoder
    print(app.json_encoder)
    app.run(host="0.0.0.0",port=5000, debug=True)

