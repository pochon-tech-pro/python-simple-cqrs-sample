from flask import Flask, request, jsonify
from application.commands import RegisterProductCommand
from application.queries import GetProductsQuery
import asyncio

app = Flask(__name__)


@app.route("/products", methods=["POST"])
def register_product():
    data = request.get_json()
    name = data["name"]
    description = data.get("description", None)

    cmd = RegisterProductCommand(name, description)
    asyncio.run(cmd.execute())

    return jsonify({"message": "Product registered."})


@app.route("/products", methods=["GET"])
def get_products():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    query = GetProductsQuery(page, per_page)
    products = query.execute()

    return jsonify({"products": [product.to_dict() for product in products]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
