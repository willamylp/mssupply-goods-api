from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from config_db import DATABASE

# Criar uma nova Mercadoria
def create_merchandise():
    merchandise = request.json

    # Verifica se todos os campos foram enviados
    if(not merchandise):
        return make_response(
            jsonify(
                msg='Faltam dados para concluir o cadastro',
                status=401
            )
        )

    cursor = DATABASE.cursor()

    cursor.execute(
        f"SELECT * FROM goods WHERE register_number = '{merchandise['register_number']}'"
    )
    merchandise_is_exists = cursor.fetchone()

    # Verifica se o nome da mercadoria já existe
    if merchandise_is_exists:
        return make_response(
            jsonify(
                msg='Mercadoria já cadastrada!',
                status=401
            )
        )

    cursor.execute(
        f"SELECT * FROM users WHERE username = '{get_jwt_identity()}'"
    )
    user = cursor.fetchone()
    
    cursor.execute(
        f"""
            INSERT INTO goods (name, register_number, manufacturer, type, description, user_id)
            VALUES (
                '{merchandise['name']}',
                '{merchandise['register_number']}',
                '{merchandise['manufacturer']}',
                '{merchandise['type']}',
                '{merchandise['description']}',
                {user[0]}
            )
        """
    )

    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            msg='Mercadoria cadastrada com sucesso!',
            status=200
        )
    )


# Retorna todas as Mercadorias
def get_goods():
    cursor = DATABASE.cursor()
    cursor.execute(
        f"""
            SELECT goods.*, users.name AS name_user_added
            FROM goods
            JOIN users ON goods.user_id = users.id
            ORDER BY goods.name ASC;
        """
    )
    goods = cursor.fetchall()
    cursor.close()

    goods = [{
        "id": good[0],
        "name": good[1],
        "register_number": good[2],
        "manufacturer": good[3],
        "type": good[4],
        "description": good[5],
        "user_id": good[6],
        "date_added": good[7],
        "name_user_added": good[8]
    } for good in goods]

    return make_response(
        jsonify(
            msg="Mercadorias encontradas",
            goods=goods,
            status=200
        )
    )


# Retorna uma Mercadoria pelo ID
def get_merchandise(id):
    cursor = DATABASE.cursor()
    cursor.execute(
        f"SELECT * FROM goods WHERE id = {id}"
    )
    merchandise = cursor.fetchone()

    # Verifica se a mercadoria existe
    if not merchandise:
        return make_response(
            jsonify(
                msg='Mercadoria não encontrada',
                status=401
            )
        )

    cursor.close()
    merchandise = {
        "id": merchandise[0],
        "name": merchandise[1],
        "register_number": merchandise[2],
        "manufacturer": merchandise[3],
        "type": merchandise[4],
        "description": merchandise[5],
        "user_id": merchandise[6]
    }

    return make_response(
        jsonify(
            msg="Mercadoria encontrada",
            merchandise=merchandise,
            status=200
        )
    )


# Atualiza uma Mercadoria pelo ID
def update_merchandise(id):
    merchandise = request.json

    # Verifica se todos os campos foram enviados
    if(not merchandise):
        return make_response(
            jsonify(
                msg='Faltam dados para concluir o cadastro',
                status=401
            )
        )

    cursor = DATABASE.cursor()

    cursor.execute(
        f"SELECT register_number FROM goods WHERE id = {id}"
    )

    merchandise_is_exists = cursor.fetchone()

    # Verifica se a mercadoria existe
    if not merchandise_is_exists:
        return make_response(
            jsonify(
                msg='Mercadoria não encontrada',
                status=401
            )
        )

    # Verifica se o número de registro da mercadoria foi alterado e se já existe
    if merchandise_is_exists[0] != merchandise['register_number']:
        cursor.execute(
            f"SELECT * FROM goods WHERE register_number = '{merchandise['register_number']}'"
        )
        merchandise_is_exists = cursor.fetchone()

        # Verifica se o número de registro da mercadoria já existe
        if merchandise_is_exists:
            return make_response(
                jsonify(
                    msg='Número de Registro já cadastrado.',
                    status=401
                )
            )

    cursor.execute(
        f"""
            UPDATE goods SET
            name = '{merchandise['name']}',
            register_number = '{merchandise['register_number']}',
            manufacturer = '{merchandise['manufacturer']}',
            type = '{merchandise['type']}',
            description = '{merchandise['description']}',
            user_id = {merchandise['user_id']}
            WHERE id = {id}
        """
    )

    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            msg='Mercadoria atualizada com sucesso!',
            status=200
        )
    )


# Deleta uma Mercadoria pelo ID
def delete_merchandise(id):
    cursor = DATABASE.cursor()
    cursor.execute(
        f"SELECT register_number FROM goods WHERE id = {id}"
    )

    merchandise_is_exists = cursor.fetchone()

    # Verifica se a mercadoria existe
    if not merchandise_is_exists:
        return make_response(
            jsonify(
                msg='Mercadoria não encontrada',
                status=401
            )
        )

    cursor.execute(
        f"DELETE FROM goods WHERE id = {id}"
    )

    DATABASE.commit()
    cursor.close()

    return make_response(
        jsonify(
            msg='Mercadoria deletada com sucesso!',
            status=204
        )
    )