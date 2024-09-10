from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)  # 創建 Flask 應用
CORS(app)  # 允許跨域請求

# 設置上傳文件夾
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 配置 PostgreSQL 資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/pokemon_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化資料庫和 SocketIO
db = SQLAlchemy(app)

# 定義 Product 模型對應 PostgreSQL 資料表
class Product(db.Model):
    __tablename__ = 'products'  # 資料表名稱
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # 商品英文名稱
    price = db.Column(db.Numeric(10, 2), nullable=False)  # 商品價格（對應PostgreSQL的MONEY類型）
    image_path = db.Column(db.String(255), nullable=False)  # 儲存圖片路徑

# mqtt client 設置
app.config['MQTT_BROKER_URL'] = 'mqttgo.io'  # MQTT Broker 地址
app.config['MQTT_BROKER_PORT'] = 1883  # MQTT 端口
app.config['MQTT_USERNAME'] = ''  # MQTT 用户名（如果需要）
app.config['MQTT_PASSWORD'] = ''  # MQTT 密碼（如果需要）
app.config['MQTT_KEEPALIVE'] = 60  # 心跳包間隔
app.config['MQTT_TLS_ENABLED'] = False  # 如果需要加密則設置為 True

mqtt = Mqtt(app)  # 創建 MQTT 客戶端
socketio = SocketIO(app, cors_allowed_origins="*")  # 使用 SocketIO 並允許所有跨域

# 保存收到的 MQTT 訊息
received_products = {}  # 設置全局變數

# 英文名稱對應中文名稱
pokemon_translation = {
    "charmander": "小火龍 公仔/神奇寶貝系列",
    "bulbasaur": "妙蛙種子 公仔/神奇寶貝系列",
    "squirtle": "傑尼龜 公仔/神奇寶貝系列",
    "psyduck": "可達鴨 公仔/神奇寶貝系列"
}

# 當連接到 MQTT Broker 時觸發
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('sui/pokemon/product')
    print('已訂閱主題: sui/pokemon/product')

# 當收到 MQTT 訊息時觸發
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global received_products

    payload = message.payload.decode()
    print(f"收到 MQTT 訊息: {payload}")
    
    try:
        # 清空購物車
        received_products = {}

        # 解析 JSON 訊息
        msg_json = json.loads(payload) #解析成python 字典

        # 處理特殊情況：無檢測到物品 ｜如果訊息表示無物品，顯示空購物車
        if "message" in msg_json and msg_json["message"] == "no objects detected":
            # 通過Socket.IO即時更新前端購物車的內容
            socketio.emit('update_cart', received_products)
        else:
            # 在應用上下文中查詢資料庫
            with app.app_context():
                    # 更新購物車商品數量和價格
                    # msg_json.items() 會返回這個字典的每個鍵值對，
                    # key 是每個項目的鍵（例如 "product0"）
                    # value 是包含商品訊息的字典（如名稱和其他資訊）
                    #  {"product1":{"name":"charmander","confidence":89}}
                for key, value in msg_json.items():
                    english_name = value.get('name')
                    translated_name = pokemon_translation.get(english_name, english_name)  # 將英文名稱轉換為中文
                    product = Product.query.filter_by(name=english_name).first()  # 查詢資料庫中的價格

                    if product:
                        price = float(product.price)
                        image_path = product.image_path  # 從資料庫中提取圖片路徑
                        if translated_name in received_products:
                            received_products[translated_name]['quantity'] += 1
                        else:
                            received_products[translated_name] = {
                                'quantity': 1, 
                                'price': price,
                                'image_path': image_path
                            }

                # 通過 WebSocket 即時更新前端
                socketio.emit('update_cart', received_products)

    except json.JSONDecodeError:
        print("無法解析收到的 JSON 訊息")

# 使用 Bootstrap 顯示購物車頁面
@app.route("/")
def index():
    return render_template("index.html", products=received_products)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
