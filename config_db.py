import mysql.connector

DATABASE = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="MainUser",
    password="MainPassword",
    database="mssupply_goods_api",
)

