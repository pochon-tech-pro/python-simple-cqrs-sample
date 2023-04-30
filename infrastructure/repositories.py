import mysql.connector
from domain.models import Product


class MySqlProductRepository:
    def __init__(self):
        self.config = {
            "user": "user",
            "password": "password",
            "host": "localhost",
            "port": 33000,
            "database": "product_db",
        }

    def _connect(self):
        return mysql.connector.connect(**self.config)

    def add(self, product):
        query = "INSERT INTO products (name, description) " "VALUES (%s, %s)"
        data = (product.name, product.description)

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            product.id = cursor.lastrowid

    def get_all(self, page, per_page):
        query = (
            "SELECT id, name, description "
            "FROM products "
            "ORDER BY id ASC "
            "LIMIT %s OFFSET %s"
        )
        offset = (page - 1) * per_page
        data = (per_page, offset)

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, data)
            result = cursor.fetchall()

        return [Product(name=row[1], description=row[2], id=row[0]) for row in result]
