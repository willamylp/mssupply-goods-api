from flask_jwt_extended import JWTManager, jwt_required
from flask import Flask
from auth_users import(
    login, create_user, get_users,
    get_user, update_user, delete_user
)
from goods import(
    create_good, #get_goods, get_good,
    #update_good, delete_good
)
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY'] = '9rhQbiX!1!MdORAbbAfP3ke0S4yTPLPJquKlpeejky-9Fpl3X0M2zggaRys4dR0r'
jwt = JWTManager(app)


### Rotas da API para o CRUD de usuários e login

@app.route('/api/v1/login', methods=['POST'])
def login_route():
    return login()

@app.route('/api/v1/users', methods=['POST'])
@jwt_required()
def create_user_route():
    return create_user()

@app.route('/api/v1/users', methods=['GET'])
@jwt_required()
def get_users_route():
    return get_users()

@app.route('/api/v1/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user_route(id):
    return get_user(id)

@app.route('/api/v1/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user_route(id):
    return update_user(id)

@app.route('/api/v1/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user_route(id):
    return delete_user(id)


### Rotas da API para o CRUD de Mercadorias

@app.route('/api/v1/goods', methods=['POST'])
@jwt_required()
def create_good_route():
    return create_good()

# @app.route('/api/v1/goods', methods=['GET'])
# @jwt_required()
# def get_goods_route():
#     return get_goods()

# @app.route('/api/v1/goods/<int:id>', methods=['GET'])
# @jwt_required()
# def get_good_route(id):
#     return get_good(id)

# @app.route('/api/v1/goods/<int:id>', methods=['PUT'])
# @jwt_required()
# def update_good_route(id):
#     return update_good(id)

# @app.route('/api/v1/goods/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_good_route(id):
#     return delete_good(id)


if __name__ == '__main__':
    app.run()