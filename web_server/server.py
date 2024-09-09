from flask import Flask, render_template
from flask_cors import CORS
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)  # 創建 Flask 應用
CORS(app)  # 允許跨域請求

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
        msg_json = json.loads(payload)

        # 如果訊息表示無物品，顯示空購物車
        if "message" in msg_json and msg_json["message"] == "no objects detected":
            socketio.emit('update_cart', received_products)
        else:
            # 更新購物車商品數量
            for key, value in msg_json.items():
                name = value.get('name')
                translated_name = pokemon_translation.get(name, name)  # 將英文名稱轉換為中文，沒有對應的名稱則保留原樣
                if translated_name in received_products:
                    received_products[translated_name] += 1  # 增加商品數量
                else:
                    received_products[translated_name] = 1  # 首次添加該商品
            
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
