from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity
from config_db import DATABASE
from auth_users import user_is_admin

def create_merchandise():
    merchandise = request.json

    # Verifica se todos os campos foram enviados
    if(not merchandise):
        return jsonify({
            "msg": "Faltam dados para concluir o cadastro"
        }), 401

    cursor = DATABASE.cursor()

    cursor.execute(
        f"SELECT * FROM goods WHERE register_number = '{merchandise['register_number']}'"
    )
    merchandise_is_exists = cursor.fetchone()

    # Verifica se o nome da mercadoria já existe
    if merchandise_is_exists:
        return jsonify({
            "msg": "Mercadoria já cadastrada"
        }), 401

    cursor.execute(
        f"SELECT * FROM users WHERE username = '{get_jwt_identity()}'"
    )
    user = cursor.fetchone()
    
    cursor.execute(
        f"""
            INSERT INTO goods (name, register_number, manufacturer, type, description, user_id)
            VALUES ('{merchandise['name']}', '{merchandise['register_number']}', '{merchandise['manufacturer']}', '{merchandise['type']}', '{merchandise['description']}', {user[0]})
        """
    )

    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            messagem='Mercadoria cadastrada com sucesso!'
        ), 200
    )

def get_goods():
    cursor = DATABASE.cursor()
    cursor.execute(
        f"SELECT * FROM goods"
    )
    goods = cursor.fetchall()
    cursor.close()

    return make_response(
        jsonify(
            goods
        ), 200
    )