from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from config_db import DATABASE

# Cria uma nova Saída de Mercadoria
def create_exit():
    try:
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
                INSERT INTO goods_exit (quantity, date, location, goods_id, user_id)
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
                msg='Saída cadastrada com sucesso!',
                status=200
            )
        )
    
    except Exception as error:
        return make_response(
            jsonify(
                msg=str(error),
                status=401
            )
        )
    
    finally:
        if 'cursor' in locals():
            cursor.close()


# Retorna todas as Saídas de Mercadorias
def get_exits():
    try:
        cursor = DATABASE.cursor()
        cursor.execute(
            f"""
                SELECT
                    goods_exit.id,
                    goods_exit.quantity,
                    goods_exit.date,
                    goods_exit.location,
                    goods_exit.goods_id,
                    goods_exit.user_id,
                    goods.name,
                    goods.register_number,
                    goods.manufacturer,
                    goods.type,
                    goods.description,
                    users.name
                FROM goods_exit
                INNER JOIN goods ON goods_exit.goods_id = goods.id
                INNER JOIN users ON goods_exit.user_id = users.id
            """
        )
        exits = cursor.fetchall()
        cursor.close()

        exits =[{
            "id": exit[0],
            "quantity": exit[1],
            "date": exit[2],
            "location": exit[3],
            "goods_id": exit[4],
            "user_id": exit[5],
            "goods_name": exit[6],
            "goods_register_number": exit[7],
            "goods_manufacturer": exit[8],
            "goods_type": exit[9],
            "goods_description": exit[10],
            "user_username": exit[11]
        } for exit in exits]

        return make_response(
            jsonify(
                msg="Saídas de Mercadorias Encontradas.",
                exits=exits,
            ), 200
        )

    except Exception as error:
        return make_response(
            jsonify(
                msg=str(error),
                status=401
            )
        )
    
    finally:
        if 'cursor' in locals():
            cursor.close()


# Retorna uma Saída de Mercadoria específica
def get_exit(id):
    try:
        cursor = DATABASE.cursor()
        cursor.execute(
            f"""
                SELECT
                    goods_exit.id,
                    goods_exit.quantity,
                    goods_exit.date,
                    goods_exit.location,
                    goods_exit.goods_id,
                    goods_exit.user_id,
                    goods.name,
                    goods.register_number,
                    goods.manufacturer,
                    goods.type,
                    goods.description,
                    users.name
                FROM goods_exit
                INNER JOIN goods ON goods_exit.goods_id = goods.id
                INNER JOIN users ON goods_exit.user_id = users.id
                WHERE goods_exit.id = {id}
            """
        )
        exit = cursor.fetchone()
        cursor.close()

        exit = [{
            "id": exit[0],
            "quantity": exit[1],
            "date": exit[2],
            "location": exit[3],
            "goods_id": exit[4],
            "user_id": exit[5],
            "name": exit[6],
            "register_number": exit[7],
            "manufacturer": exit[8],
            "type": exit[9],
            "description": exit[10],
            "user_name": exit[11]
        } for exit in exit]

        return make_response(
            jsonify(
                msg="Saída de Mercadoria Encontrada.",
                exit=exit,
            ), 200
        )

    except Exception as error:
        return make_response(
            jsonify(
                msg=str(error),
                status=401
            )
        )
    
    finally:
        if 'cursor' in locals():
            cursor.close()

# Atualiza uma Saída de Mercadoria
def update_exit(id):
    try:
        exit = request.json

        # Verifica se todos os campos foram enviados
        if(not exit):
            return make_response(
                jsonify(
                    msg='Faltam dados para concluir o cadastro',
                    status=401
                )
            )
        
        cursor = DATABASE.cursor()
        cursor.execute(
            f"""
                UPDATE goods_exit SET
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
                msg='Saída atualizada com sucesso!',
                status=200
            )
        )
    
    except Exception as error:
        return make_response(
            jsonify(
                msg=str(error),
                status=401
            )
        )
    
    finally:
        if 'cursor' in locals():
            cursor.close()


# Deleta uma Saída de Mercadoria
def delete_exit(id):
    try:
        cursor = DATABASE.cursor()
        cursor.execute(
            f"DELETE FROM goods_exit WHERE id = {id}"
        )
        DATABASE.commit()
        cursor.close()

        return make_response(
            jsonify(
                msg='Saída deletada com sucesso!',
                status=204
            )
        )

    except Exception as error:
        return make_response(
            jsonify(
                msg=str(error),
                status=401
            )
        )
    
    finally:
        if 'cursor' in locals():
            cursor.close()

