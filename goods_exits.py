from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from config_db import DATABASE

# Cria uma nova Saída de Mercadoria
def create_exit():
    
    exit = request.json

    # Verifica se todos os campos foram enviados
    if(not exit):
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
            INSERT INTO goods_exits (quantity, date, location, goods_id, user_id)
            VALUES (
                '{exit['quantity']}',
                '{exit['date']}',
                '{exit['location']}',
                {exit['goods_id']},
                {user[0]}
            )
        """
    )

    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            messagem='Saída cadastrada com sucesso!'
        ), 200
    )


# Retorna todas as Saídas de Mercadorias
def get_exits():
    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            SELECT
                goods_exits.id,
                goods_exits.quantity,
                goods_exits.date,
                goods_exits.location,
                goods_exits.goods_id,
                goods_exits.user_id,
                goods.name,
                goods.register_number,
                goods.manufacturer,
                goods.type,
                goods.description,
                users.name
            FROM goods_exits
            INNER JOIN goods ON goods_exits.goods_id = goods.id
            INNER JOIN users ON goods_exits.user_id = users.id
        """
    )
    exits = cursor.fetchall()
    cursor.close()

    return make_response(
        jsonify(exits), 200
    )


# Retorna uma Saída de Mercadoria específica
def get_exit(id):
    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            SELECT
                goods_exits.id,
                goods_exits.quantity,
                goods_exits.date,
                goods_exits.location,
                goods_exits.goods_id,
                goods_exits.user_id,
                goods.name,
                goods.register_number,
                goods.manufacturer,
                goods.type,
                goods.description,
                users.name
            FROM goods_exits
            INNER JOIN goods ON goods_exits.goods_id = goods.id
            INNER JOIN users ON goods_exits.user_id = users.id
            WHERE goods_exits.id = {id}
        """
    )
    exit = cursor.fetchone()
    cursor.close()

    return make_response(
        jsonify(exit), 200
    )


# Atualiza uma Saída de Mercadoria
def update_exit(id):
    exit = request.json

    # Verifica se todos os campos foram enviados
    if(not exit):
        return jsonify({
            "msg": "Faltam dados para concluir o cadastro"
        }), 401

    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            UPDATE goods_exits SET
                quantity = '{exit['quantity']}',
                date = '{exit['date']}',
                location = '{exit['location']}',
                goods_id = {exit['goods_id']}
            WHERE id = {id}
        """
    )

    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            messagem='Saída atualizada com sucesso!'
        ), 200
    )


# Deleta uma Saída de Mercadoria
def delete_exit(id):
    cursor = DATABASE.cursor()
    cursor.execute(
        f"DELETE FROM goods_exits WHERE id = {id}"
    )
    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            messagem='Saída deletada com sucesso!'
        ), 200
    )

