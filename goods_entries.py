from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from config_db import DATABASE

# Criar uma nova Entrada de Mercadoria
def create_entry():

    entry = request.json

    # Verifica se todos os campos foram enviados
    if(not entry):
        return jsonify({
            "msg": "Faltam dados para concluir o cadastro"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(
        f"SELECT * FROM users WHERE username = '{get_jwt_identity()}'"
    )
    user = cursor.fetchone()
    
    cursor.execute(
        f"""
            INSERT INTO goods_entries (quantity, date, location, goods_id, user_id)
            VALUES (
                '{entry['quantity']}',
                '{entry['date']}',
                '{entry['location']}',
                {entry['goods_id']},
                {user[0]}
            )
        """
    )

    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            messagem='Entrada cadastrada com sucesso!'
        ), 200
    )


# Retorna todas as Entradas de Mercadorias
def get_entries():
    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            SELECT
                goods_entries.id,
                goods_entries.quantity,
                goods_entries.date,
                goods_entries.location,
                goods_entries.goods_id,
                goods_entries.user_id,
                goods.name,
                goods.register_number,
                goods.manufacturer,
                goods.type,
                goods.description,
                users.username
            FROM goods_entries
            INNER JOIN goods ON goods_entries.goods_id = goods.id
            INNER JOIN users ON goods_entries.user_id = users.id
        """
    )
    entries = cursor.fetchall()
    cursor.close()

    entries = [{
        "id": entry[0],
        "quantity": entry[1],
        "date": entry[2],
        "location": entry[3],
        "goods_id": entry[4],
        "user_id": entry[5],
        "goods_name": entry[6],
        "goods_register_number": entry[7],
        "goods_manufacturer": entry[8],
        "goods_type": entry[9],
        "goods_description": entry[10],
        "user_username": entry[11]
    } for entry in entries]

    return make_response(
        jsonify(
            msg="Entradas Eecontradas",
            entries=entries
        ), 200
    )


# Retorna uma Entrada de Mercadoria pelo ID
def get_entry(id):
    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            SELECT
                goods_entries.id,
                goods_entries.quantity,
                goods_entries.date,
                goods_entries.location,
                goods_entries.goods_id,
                goods_entries.user_id,
                goods.name,
                goods.register_number,
                goods.manufacturer,
                goods.type,
                goods.description,
                users.username
            FROM goods_entries
            INNER JOIN goods ON goods_entries.goods_id = goods.id
            INNER JOIN users ON goods_entries.user_id = users.id
            WHERE goods_entries.id = {id}
        """
    )
    entry = cursor.fetchone()
    cursor.close()

    entry = {
        "id": entry[0],
        "quantity": entry[1],
        "date": entry[2],
        "location": entry[3],
        "goods_id": entry[4],
        "user_id": entry[5],
        "goods_name": entry[6],
        "goods_register_number": entry[7],
        "goods_manufacturer": entry[8],
        "goods_type": entry[9],
        "goods_description": entry[10],
        "user_username": entry[11]
    }

    return make_response(
        jsonify(
            msg="Entrada encontrada",
            entry=entry
        ), 200
    )

# Atualiza uma Entrada de Mercadoria pelo ID
def update_entry(id):
    entry = request.json

    # Verifica se todos os campos foram enviados
    if(not entry):
        return jsonify({
            "msg": "Faltam dados para concluir o cadastro"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(
        f"SELECT * FROM users WHERE username = '{get_jwt_identity()}'"
    )
    user = cursor.fetchone()

    cursor.execute(
        f"""
            UPDATE goods_entries SET
                quantity = '{entry['quantity']}',
                date = '{entry['date']}',
                location = '{entry['location']}',
                goods_id = {entry['goods_id']},
                user_id = {user[0]}
            WHERE id = {id}
        """
    )

    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            messagem='Entrada atualizada com sucesso!'
        ), 200
    )

# Deleta uma Entrada de Mercadoria pelo ID
def delete_entry(id):
    cursor = DATABASE.cursor()
    cursor.execute(
        f"DELETE FROM goods_entries WHERE id = {id}"
    )
    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            messagem='Entrada deletada com sucesso!'
        ), 200
    )