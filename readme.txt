[ディレクトリ構成]
├─ app.py
├─ application
│   ├─ commands.py
│   └─ queries.py
├─ domain
│   ├─ events.py
│   └─ models.py
├─ infrastructure
│   ├─ event_publishers.py
│   ├─ event_subscribers.py
│   └─ repositories.py
└─ requirements.txt


# MysqlおよびRedisの起動＆テーブル作成（Terminal 0）
docker-compose up -d
docker-compose exec mysql bash
mysql -u user -ppassword -Dproduct_db
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255)
);

# サブスクライバーの起動（Terminal 1）
export PYTHONPATH="$PWD"
python infrastructure/event_subscribers.py

# Webサーバ起動（Terminal 2）
python app.py

# 動作検証（Terminal 3）
curl -X POST -H "Content-Type: application/json" -d '{"name": "Example Product", "description": "This is an example product."}' http://localhost:5001/products
curl -X GET "http://localhost:5001/products?page=1&per_page=10"
