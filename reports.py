from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from config_db import DATABASE

def all_merchandise_report():
    try:
        cursor = DATABASE.cursor()

        cursor.execute(
            f"""
                SELECT
                YEAR(date_series) AS year,
                MONTH(date_series) AS month,
                COALESCE(COUNT(goods.date_added), 0) AS total_records
                FROM (
                    SELECT 
                    CURRENT_DATE - INTERVAL n MONTH AS date_series
                    FROM (
                        SELECT 0 AS n
                        UNION ALL SELECT 1
                        UNION ALL SELECT 2
                        UNION ALL SELECT 3
                        UNION ALL SELECT 4
                        UNION ALL SELECT 5
                        UNION ALL SELECT 6
                        UNION ALL SELECT 7
                        UNION ALL SELECT 8
                        UNION ALL SELECT 9
                        UNION ALL SELECT 10
                        UNION ALL SELECT 11
                        UNION ALL SELECT 12
                    ) numbers
                ) AS Months
                LEFT JOIN
                goods ON YEAR(goods.date_added) = YEAR(Months.date_series)
                        AND MONTH(goods.date_added) = MONTH(Months.date_series)
                GROUP BY
                YEAR(Months.date_series), MONTH(Months.date_series)
                ORDER BY
                year, month;
            """
        )

        total_records = cursor.fetchall()
        cursor.close()

        total_records = [{
            "year": record[0],
            "month": record[1],
            "total": record[2]
        } for record in total_records]

        return make_response(
            jsonify(
                total_records=total_records,
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

def all_merchandise_entry_report():
    try:
        cursor = DATABASE.cursor()

        cursor.execute(
            f"""
                SELECT
                YEAR(date_series) AS year,
                MONTH(date_series) AS month,
                COALESCE(COUNT(goods_entries.date), 0) AS total_records
                FROM (
                    SELECT 
                    CURRENT_DATE - INTERVAL n MONTH AS date_series
                    FROM (
                        SELECT 0 AS n
                        UNION ALL SELECT 1
                        UNION ALL SELECT 2
                        UNION ALL SELECT 3
                        UNION ALL SELECT 4
                        UNION ALL SELECT 5
                        UNION ALL SELECT 6
                        UNION ALL SELECT 7
                        UNION ALL SELECT 8
                        UNION ALL SELECT 9
                        UNION ALL SELECT 10
                        UNION ALL SELECT 11
                        UNION ALL SELECT 12
                    ) numbers
                ) AS Months
                LEFT JOIN
                goods_entries ON YEAR(goods_entries.date) = YEAR(Months.date_series)
                        AND MONTH(goods_entries.date) = MONTH(Months.date_series)
                GROUP BY
                YEAR(Months.date_series), MONTH(Months.date_series)
                ORDER BY
                year, month;
            """
        )

        total_records = cursor.fetchall()
        cursor.close()

        total_records = [{
            "year": record[0],
            "month": record[1],
            "total": record[2]
        } for record in total_records]

        return make_response(
            jsonify(
                total_records=total_records,
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


def all_merchandise_exit_report():
    try:
        cursor = DATABASE.cursor()

        cursor.execute(
            f"""
                SELECT
                YEAR(date_series) AS year,
                MONTH(date_series) AS month,
                COALESCE(COUNT(goods_exit.date), 0) AS total_records
                FROM (
                    SELECT 
                    CURRENT_DATE - INTERVAL n MONTH AS date_series
                    FROM (
                        SELECT 0 AS n
                        UNION ALL SELECT 1
                        UNION ALL SELECT 2
                        UNION ALL SELECT 3
                        UNION ALL SELECT 4
                        UNION ALL SELECT 5
                        UNION ALL SELECT 6
                        UNION ALL SELECT 7
                        UNION ALL SELECT 8
                        UNION ALL SELECT 9
                        UNION ALL SELECT 10
                        UNION ALL SELECT 11
                        UNION ALL SELECT 12
                    ) numbers
                ) AS Months
                LEFT JOIN
                goods_exit ON YEAR(goods_exit.date) = YEAR(Months.date_series)
                        AND MONTH(goods_exit.date) = MONTH(Months.date_series)
                GROUP BY
                YEAR(Months.date_series), MONTH(Months.date_series)
                ORDER BY
                year, month;
            """
        )

        total_records = cursor.fetchall()
        cursor.close()

        total_records = [{
            "year": record[0],
            "month": record[1],
            "total": record[2]
        } for record in total_records]

        return make_response(
            jsonify(
                total_records=total_records,
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

def merchandise_by_user_report():
    try:
        cursor = DATABASE.cursor()

        cursor.execute(
            f"""
                SELECT
                    users.name AS name_user,
                    COALESCE(COUNT(goods.date_added), 0) AS total_records
                FROM goods
                    JOIN users ON goods.user_id = users.id
                GROUP BY
                    users.name
                ORDER BY
                    users.name;
            """
        )

        total_records = cursor.fetchall()
        cursor.close()

        total_records = [{
            "name_user": record[0],
            "total": record[1]
        } for record in total_records]

        return make_response(
            jsonify(
                total_records=total_records,
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


def merchandise_entry_by_user_report():
    try:
        cursor = DATABASE.cursor()

        cursor.execute(
            f"""
                SELECT
                    users.name AS name_user,
                    COALESCE(COUNT(goods_entries.date), 0) AS total_records
                FROM goods_entries
                    JOIN users ON goods_entries.user_id = users.id
                GROUP BY
                    users.name
                ORDER BY
                    users.name;
            """
        )

        total_records = cursor.fetchall()
        cursor.close()

        total_records = [{
            "name_user": record[0],
            "total": record[1]
        } for record in total_records]

        return make_response(
            jsonify(
                total_records=total_records,
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


def merchandise_exit_by_user_report():
    try:
        cursor = DATABASE.cursor()

        cursor.execute(
            f"""
                SELECT
                    users.name AS name_user,
                    COALESCE(COUNT(goods_exit.date), 0) AS total_records
                FROM goods_exit
                    JOIN users ON goods_exit.user_id = users.id
                GROUP BY
                    users.name
                ORDER BY
                    users.name;
            """
        )

        total_records = cursor.fetchall()
        cursor.close()

        total_records = [{
            "name_user": record[0],
            "total": record[1]
        } for record in total_records]

        return make_response(
            jsonify(
                total_records=total_records,
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

