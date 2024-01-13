from flask_jwt_extended import JWTManager, jwt_required
from flask import Flask
from flask_cors import CORS
from auth_users import(
    login, logout, create_user, get_users,
    get_user, update_user, delete_user
)

from goods import(
    create_merchandise, get_goods, get_merchandise,
    update_merchandise, delete_merchandise
)

from goods_entries import(
    create_entry, get_entries, get_entry,
    update_entry, delete_entry
)

from goods_exits import(
    create_exit, get_exits, get_exit,
    update_exit, delete_exit
)

# Configurações do Flask

app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY'] = '9rhQbiX!1!MdORAbbAfP3ke0S4yTPLPJquKlpeejky-9Fpl3X0M2zggaRys4dR0r'
jwt = JWTManager(app)


### Rotas da API para o CRUD de Usuários e Login

@app.route('/api/v1/login', methods=['POST'])
def login_route():
    return login()

@app.route('/api/v1/logout', methods=['POST'])
def logout_route():
    return logout()

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
def create_merchandise_route():
    return create_merchandise()

@app.route('/api/v1/goods', methods=['GET'])
@jwt_required()
def get_goods_route():
    return get_goods()

@app.route('/api/v1/goods/<int:id>', methods=['GET'])
@jwt_required()
def get_merchandise_route(id):
    return get_merchandise(id)

@app.route('/api/v1/goods/<int:id>', methods=['PUT'])
@jwt_required()
def update_merchandise_route(id):
    return update_merchandise(id)

@app.route('/api/v1/goods/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_merchandise_route(id):
    return delete_merchandise(id)


### Rotas da API para o CRUD de Entradas de Mercadorias

@app.route('/api/v1/goods_entries', methods=['POST'])
@jwt_required()
def create_entry_route():
    return create_entry()

@app.route('/api/v1/goods_entries', methods=['GET'])
@jwt_required()
def get_entries_route():
    return get_entries()

@app.route('/api/v1/goods_entries/<int:id>', methods=['GET'])
@jwt_required()
def get_entry_route(id):
    return get_entry(id)

@app.route('/api/v1/goods_entries/<int:id>', methods=['PUT'])
@jwt_required()
def update_entry_route(id):
    return update_entry(id)

@app.route('/api/v1/goods_entries/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_entry_route(id):
    return delete_entry(id)


### Rotas da API para o CRUD de Saídas de Mercadorias

@app.route('/api/v1/goods_exits', methods=['POST'])
@jwt_required()
def create_exit_route():
    return create_exit()

@app.route('/api/v1/goods_exits', methods=['GET'])
@jwt_required()
def get_exits_route():
    return get_exits()

@app.route('/api/v1/goods_exits/<int:id>', methods=['GET'])
@jwt_required()
def get_exit_route(id):
    return get_exit(id)

@app.route('/api/v1/goods_exits/<int:id>', methods=['PUT'])
@jwt_required()
def update_exit_route(id):
    return update_exit(id)

@app.route('/api/v1/goods_exits/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_exit_route(id):
    return delete_exit(id)


# Inicia o servidor

if __name__ == '__main__':
    app.run(
        debug=True,
        port=81
    )
