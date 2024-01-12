from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity
from config_db import DATABASE
from auth_users import user_is_admin

def create_good():
    good = request.json

    # Verifica se todos os campos foram enviados
    if(not good):
        return jsonify({
            "msg": "Faltam dados para concluir o cadastro"
        }), 401

    cursor = DATABASE.cursor()

    cursor.execute(
        f"SELECT * FROM goods WHERE register_number = '{good['register_number']}'"
    )
    good_is_exists = cursor.fetchone()

    # Verifica se o nome da mercadoria já existe
    if good_is_exists:
        return jsonify({
            "msg": "Mercadoria já cadastrada"
        }), 401

    cursor.execute(
        f"""
            INSERT INTO goods (name, register_number, manufacturer, type, description, user_id)
            VALUES ('{good['name']}', '{good['register_number']}', '{good['manufacturer']}', '{good['type']}', '{good['description']}', '{get_jwt_identity()}')
        """
    )

    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            messagem='Mercadoria cadastrada com sucesso!'
        ), 200
    )

