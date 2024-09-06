from flask import Flask  #導入Flask類(說明書) -> WSGI 應用程式

app = Flask(__name__) # 透過Flask類說明書 -> 創建app物件

@app.route("/") 
def hello_user(): 
    return "<p>妳好 sui/p>"
