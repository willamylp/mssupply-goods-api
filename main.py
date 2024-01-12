import mysql.connector
from flask import Flask, make_response, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


DATABASE = mysql.connector.connect(
    host="localhost",
    user="MainUser",
    password="MainPassword",
    database="mssupply_goods_api"
)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JWT_SECRET_KEY'] = '9rhQbiX!1!MdORAbbAfP3ke0S4yTPLPJquKlpeejky-9Fpl3X0M2zggaRys4dR0r'
jwt = JWTManager(app)



# Verifica se o usuário é administador
def user_is_admin(user_id):
    cursor = DATABASE.cursor()
    cursor.execute(f"SELECT id, is_admin FROM users WHERE username = '{user_id}'")
    is_admin = cursor.fetchone()
    cursor.close()

    return is_admin

    
@app.route('/api/v1/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if(not username or not password):
        return jsonify({
            "msg": "Faltam dados para concluir o login"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cursor.fetchone()
    cursor.close()

    if user is None:
        return jsonify({
            "msg": "Credenciais inválidas"
        }), 401

    access_token = create_access_token(identity=username)

    return make_response(
        jsonify(
            messagem='Login realizado com sucesso',
            access_token=access_token
        ), 200
    )

@app.route('/api/v1/users', methods=['POST'])
@jwt_required()
def create_user():
    user = request.json
    
    if(not user):
        return jsonify({
            "msg": "Faltam dados para concluir o cadastro"
        }), 401
    
    cursor = DATABASE.cursor()
    cursor.execute(
        f"SELECT * FROM users WHERE username = '{user['username']}' OR email = '{user['email']}'"
    )
    user_is_exists = cursor.fetchone()
    
    if user_is_exists is not None:
        return jsonify({
            "msg": "Usuário já cadastrado!"
        }), 401
    
    cursor.execute(
        f"INSERT INTO users (name, email, username, password) VALUES ('{user['name']}', '{user['email']}', '{user['username']}', '{user['password']}')"
    )

    DATABASE.commit()
    cursor.close()

    return jsonify({
        "msg": "Usuário criado com sucesso!"
    }), 201

@app.route('/api/v1/users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    if is_admin[1] == 0:
        return jsonify({
            "msg": "Você não tem permissão para acessar esta rota"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(f"SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    users_list = []

    for user in users:
        users_list.append({
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "username": user[3],
            "is_admin": user[5]
        })

    return make_response(
        jsonify(
            msg='Lista de usuários',
            users=users_list
        )
    )

@app.route('/api/v1/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    # Verifica se o usuário é administador ou se o id do usuário é o mesmo do token
    if(is_admin[0] != id) and (is_admin[1] == 0):
        return jsonify({
            "msg": "Você não tem permissão para acessar esta rota"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {id}")
    user = cursor.fetchone()
    cursor.close()

    return make_response(
        jsonify(
            msg='Lista de usuários',
            user= {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "username": user[3],
                "is_admin": user[5]
            }
        )
    )

@app.route('/api/v1/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    # Verifica se o usuário é administador ou se o id do usuário é o mesmo do token
    if(is_admin[0] != id) and (is_admin[1] == 0):
        return jsonify({
            "msg": "Você não tem permissão para acessar esta rota"
        }), 401

    user = request.json

    if(not user):
        return jsonify({
            "msg": "Faltam dados para concluir o cadastro"
        }), 401

    cursor = DATABASE.cursor()

    # Verifica se o usuário é administador e se o campo is_admin foi enviado
    if((is_admin[1] == 1) and ('is_admin' in user.keys())):
        cursor.execute(
            f"UPDATE users SET name='{user['name']}', email='{user['email']}', username='{user['username']}', password='{user['password']}', is_admin={user['is_admin']} WHERE id = {id}"
        )
        
    else:
        cursor.execute(
            f"UPDATE users SET name='{user['name']}', email='{user['email']}', username='{user['username']}', password='{user['password']}' WHERE id = {id}"
        )
    
    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            msg='Usuário atualizado com sucesso',
        )
    )


@app.route('/api/v1/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    # Verifica se o usuário é administador
    if is_admin[1] == 0:
        return jsonify({
            "msg": "Você não tem permissão para acessar esta rota"
        }), 401
    
    if is_admin[0] == id:
        return jsonify({
            "msg": "Você não pode deletar seu próprio usuário"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {id}")
    DATABASE.commit()
    cursor.close()

    return jsonify({
        "msg": "Usuário deletado com sucesso!"
    }), 201

if __name__ == '__main__':
    app.run()