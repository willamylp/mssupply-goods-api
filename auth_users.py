from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity
from config_db import DATABASE

# Verifica se o usuário é administador
def user_is_admin(user_id):
    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            SELECT id, is_admin 
            FROM users 
            WHERE username = '{user_id}'
        """
    )
    is_admin = cursor.fetchone()
    cursor.close()

    # Retorna o id e o valor do campo 'is_admin'
    return is_admin

# Realiza o login
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Verifica se todos os campos foram enviados
    if(not username or not password):
        return jsonify({
            "msg": "Faltam dados para concluir o login"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            SELECT * FROM users 
            WHERE username = '{username}' 
            AND password = '{password}'
        """
    )
    user = cursor.fetchone()
    cursor.close()

    # Verifica se o usuário existe
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

# Criar um novo Usuário
def create_user():
    user = request.json
    
    # Verifica se todos os campos foram enviados
    if(not user):
        return jsonify({
            "msg": "Faltam dados para concluir o cadastro"
        }), 401
    
    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            SELECT * FROM users 
            WHERE username = '{user['username']}' 
            OR email = '{user['email']}'
        """
    )
    user_is_exists = cursor.fetchone()
    
    # Verifica se o usuário já existe
    if user_is_exists is not None:
        return jsonify({
            "msg": "Usuário já cadastrado!"
        }), 401
    
    cursor.execute(
        f"""
            INSERT INTO users (name, email, username, password) 
            VALUES (
                '{user['name']}',
                '{user['email']}',
                '{user['username']}',
                '{user['password']}'
            )
        """
    )

    DATABASE.commit()
    cursor.close()

    return jsonify({
        "msg": "Usuário criado com sucesso!"
    }), 201

# Retorna todos os usuários
def get_users():
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    # Verifica se o usuário não é administador
    if is_admin[1] == 0:
        return jsonify({
            "msg": "Você não tem permissão para acessar esta rota"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(
        f"SELECT * FROM users"
    )
    users = cursor.fetchall()
    cursor.close()

    users = [{
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "username": user[3],
        "is_admin": user[5]
    } for user in users]

    return make_response(
        jsonify(
            msg='Lista de usuários',
            users=users
        )
    )

# Retorna um usuário específico
def get_user(id):
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    # Verifica se o usuário é administador ou se o id do usuário é o mesmo do token
    if(is_admin[0] != id) and (is_admin[1] == 0):
        return jsonify({
            "msg": "Você não tem permissão para acessar esta rota"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(
        f"SELECT * FROM users WHERE id = {id}"
    )
    user = cursor.fetchone()

    if user is None:
        return jsonify({
            "msg": "Usuário não encontrado"
        }), 401

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

# Atualiza um usuário
def update_user(id):
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)
    user = request.json

    # Verifica se o usuário é administador ou se o id do usuário é o mesmo do token
    if(is_admin[0] != id) and (is_admin[1] == 0):
        return jsonify({
            "msg": "Você não tem permissão para acessar esta rota"
        }), 401

    if(not user):
        return jsonify({
            "msg": "Faltam dados para concluir o cadastro"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {id}")
    seacrh_user = cursor.fetchone()

    if seacrh_user is None:
        return jsonify({
            "msg": "Usuário não encontrado"
        }), 401
    
    # Verifica se o usuário é administador e se o campo 'is_admin' foi enviado
    if((is_admin[1] == 1) and ('is_admin' in user.keys())):
        cursor.execute(
            f"""
                UPDATE users SET 
                name='{user['name']}',
                email='{user['email']}',
                username='{user['username']}',
                password='{user['password']}',
                is_admin={user['is_admin']}
                WHERE id = {id}
            """
        )
    
    else:
        cursor.execute(
            f"""
                UPDATE users SET 
                name='{user['name']}',
                email='{user['email']}',
                username='{user['username']}',
                password='{user['password']}'
                WHERE id = {id}
            """
        )
    
    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            msg='Usuário atualizado com sucesso',
        )
    )

# Deleta um usuário
def delete_user(id):
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    # Verifica se o usuário é administador
    if is_admin[1] == 0:
        return jsonify({
            "msg": "Você não tem permissão para acessar esta rota"
        }), 401
    
    # Verifica se o usuário está tentando deletar o próprio usuário
    if is_admin[0] == id:
        return jsonify({
            "msg": "Você não pode deletar seu próprio usuário"
        }), 401

    cursor = DATABASE.cursor()

    cursor.execute(
        f"SELECT * FROM users WHERE id = {id}"
    )
    user = cursor.fetchone()

    if user is None:
        return jsonify({
            "msg": "Usuário não encontrado"
        }), 401

    cursor.execute(
        f"DELETE FROM users WHERE id = {id}"
    )
    DATABASE.commit()
    cursor.close()

    return jsonify({
        "msg": "Usuário deletado com sucesso!"
    }), 201
