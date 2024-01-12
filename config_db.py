import mysql.connector

DATABASE = mysql.connector.connect(
    host="localhost",
    user="MainUser",
    password="MainPassword",
    database="mssupply_goods_api"
)

