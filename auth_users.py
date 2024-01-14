from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, unset_jwt_cookies
from config_db import DATABASE
from passlib.hash import bcrypt

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
        return make_response(
            jsonify(
                msg='Faltam dados para concluir o login',
                status=401
            )
        )

    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            SELECT * FROM users 
            WHERE username = '{username}'
        """
    )
    user = cursor.fetchone()
    cursor.close()

    # Verifica se o usuário existe
    if user is None:
        return make_response(
            jsonify(
                msg='Usuário não encontrado',
                status=401
            )
        )
    
    if user[6] == 0:
        return make_response(
            jsonify(
                msg='Usuário inativo',
                status=401
            )
        )
    
    if bcrypt.verify(password, user[4]):
        access_token = create_access_token(identity=username)

        return make_response(
            jsonify(
                msg='Login realizado com sucesso!',
                access_token=access_token,
                user={
                    "id": user[0],
                    "name": user[1],
                    "email": user[2],
                    "username": user[3],
                    "is_admin": user[5],
                },
                status=200
            )
        )

    else:
        return make_response(
            jsonify(
                msg='Credenciais inválidas!',
                status=401
            )
        )


# Logout do usuário
def logout():
    response = jsonify({
        "msg": "Logout realizado com sucesso!"
    })
    unset_jwt_cookies(response)
    return response

# Criar um novo Usuário
def create_user():
    user = request.json
    
    # Verifica se todos os campos foram enviados
    if(not user):
        return make_response(
            jsonify(
                msg='Faltam dados para concluir o cadastro',
                status=401
            )
        )
    
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
        return make_response(
            jsonify(
                msg='Usuário já cadastrado!',
                status=401
            )
        )
    
    hashed_password = bcrypt.hash(user['password'])

    cursor.execute(
        f"""
            INSERT INTO users (name, email, username, password) 
            VALUES (
                '{user['name']}',
                '{user['email']}',
                '{user['username']}',
                '{hashed_password}'
            )
        """
    )

    DATABASE.commit()
    cursor.close()
    return make_response(
        jsonify(
            msg='Usuário criado com sucesso!',
            status=201
        )
    )

# Retorna todos os usuários
def get_users():    
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    # Verifica se o usuário não é administador
    if is_admin[1] == 0:
        return make_response(
            jsonify(
                msg='Você não tem permissão para acessar esta rota',
                status=401
            )
        )

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
        "is_admin": user[5],
        "is_active": user[6]
    } for user in users]

    return make_response(
        jsonify(
            msg='Lista de Usuários',
            users=users,
            status=200
        )
    )

# Retorna um usuário específico
def get_user(id):
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    # Verifica se o usuário é administador ou se o id do usuário é o mesmo do token
    if(is_admin[0] != id) and (is_admin[1] == 0):
        return make_response(
            jsonify(
                msg='Você não tem permissão para acessar esta rota',
                status=401
            )
        )

    cursor = DATABASE.cursor()
    cursor.execute(
        f"SELECT * FROM users WHERE id = {id}"
    )
    user = cursor.fetchone()

    if user is None:
        return make_response(
            jsonify(
                msg='Usuário não encontrado',
                status=401
            )
        )

    cursor.close()

    return make_response(
        jsonify(
            msg='Dados do Usuário',
            user= {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "username": user[3],
                "is_admin": user[5],
            },
            status=200
        )
    )

# Atualiza um usuário
def update_user(id):
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)
    user = request.json

    # Verifica se o usuário é administador ou
    # se o id do usuário é o mesmo do token
    if(is_admin[0] != id) and (is_admin[1] == 0):
        return make_response(
            jsonify(
                msg='Você não tem permissão para acessar esta rota',
                status=401
            )
        )
    
    if(not user):
        return make_response(
            jsonify(
                msg='Faltam dados para concluir o cadastro',
                status=401
            )
        )
    
    cursor = DATABASE.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {id}")
    seacrh_user = cursor.fetchone()

    if seacrh_user is None:
        return make_response (
            jsonify(
                msg='Usuário não encontrado',
                status=401
            )
        )
    
    hashed_password = ''
    if('password' in user.keys()):
        hashed_password = bcrypt.hash(user['password'])
    
    # Verifica se o usuário é administador
    # e se o campo 'is_admin' foi enviado
    if((is_admin[1] == 1) and ('is_admin' in user.keys()) or ('is_active' in user.keys())):
        cursor.execute(
            f"""
                UPDATE users SET 
                name='{user['name']}',
                email='{user['email']}',
                username='{user['username']}',
                password='{hashed_password if 'password' in user.keys() else seacrh_user[4]}',
                is_admin={user['is_admin'] if 'is_admin' in user.keys() else seacrh_user[5]},
                is_active={user['is_active' if 'is_active' in user.keys() else seacrh_user[6]]}
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
                password='{hashed_password}'
                WHERE id = {id}
            """
        )
    
    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            msg='Usuário atualizado com sucesso!',
            status=201
        )
    )

# Deleta um usuário
def delete_user(id):
    user_id = get_jwt_identity()
    is_admin = user_is_admin(user_id)

    # Verifica se o usuário é administador
    if is_admin[1] == 0:
        return make_response(
            jsonify(
                msg='Você não tem permissão para acessar esta rota',
                status=401
            )
        )
    
    # Verifica se o usuário está tentando deletar o próprio usuário
    if is_admin[0] == id:
        return make_response(
            jsonify(
                msg='Você não pode deletar seu próprio usuário',
                status=401
            )
        )

    cursor = DATABASE.cursor()

    cursor.execute(
        f"SELECT * FROM users WHERE id = {id}"
    )
    user = cursor.fetchone()

    if user is None:
        return make_response(
            jsonify(
                msg='Usuário não encontrado',
                status=401
            )
        )

    cursor.execute(
        f"DELETE FROM users WHERE id = {id}"
    )
    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            msg='Usuário deletado com sucesso!',
            status=204
        )
    )
