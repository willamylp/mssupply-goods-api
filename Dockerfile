# Imagem oficial do MySQL
FROM mysql:5.7

# Adicionando os scripts SQL para criação do banco e tabelas
COPY ./db/ /docker-entrypoint-initdb.d/


# docker build -t mstar-supply-api .
# docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=RootPassword -e MYSQL_DATABASE=mssupply_goods_api -e MYSQL_USER=MainUser -e MYSQL_PASSWORD=MainPassword mstar-supply-api