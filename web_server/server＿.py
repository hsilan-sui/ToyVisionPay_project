from flask import Flask, render_template
from flask_mqtt import Mqtt
import json

app = Flask(__name__)  # 創建 Flask 應用

# mqtt client 設置
app.config['MQTT_BROKER_URL'] = 'mqttgo.io'  # MQTT Broker 地址
app.config['MQTT_BROKER_PORT'] = 1883  # MQTT 端口
app.config['MQTT_USERNAME'] = ''  # MQTT 用户名（如果需要）
app.config['MQTT_PASSWORD'] = ''  # MQTT 密码（如果需要）
app.config['MQTT_KEEPALIVE'] = 60  # 心跳包间隔
app.config['MQTT_TLS_ENABLED'] = False  # 如果需要加密则设置为 True

mqtt = Mqtt(app)  # 創建 MQTT 客戶端

# 保存收到的 MQTT 訊息
received_products = {}  # 修改這裡，將它設置為全局變數

# .on_connect() 連接上 mqtt broker 時觸發
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('sui/pokemon/product')
    print('已訂閱主題: sui/pokemon/product')

# 當收到 MQTT 訊息時觸發
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global received_products
    
    # 每次收到新消息時清空購物車
    received_products = {}
    
    payload = message.payload.decode()
    print(f"收到 MQTT 訊息: {payload}")
    
    try:
        # 解析 JSON 訊息，並更新購物車商品數量
        msg_json = json.loads(payload)
        for key, value in msg_json.items():
            name = value.get('name')
            if name in received_products:
                received_products[name] += 1  # 增加商品數量
            else:
                received_products[name] = 1  # 首次添加該商品
    except json.JSONDecodeError:
        print("無法解析收到的 JSON 訊息")

# 使用 Bootstrap 顯示購物車頁面
@app.route("/")
def index():
    return render_template("index.html", products=received_products)

if __name__ == "__main__":
    app.run(debug=True)
