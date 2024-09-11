# 專案大綱

- 剛從健行科大『AIoT 物聯網暨人工智慧工程師實戰班』結訓，就想說把 AI 這塊和 IOT 物聯網串連起來，於是就以自己手邊有的寶可夢公仔為 AI 模型訓練的資料，做一個商品辨識結帳系統，以下是我的專案架構 以及 AI 模型訓練流程：
  - ![專案架構圖](./aiot_visionpay.png)
  - AI 模型訓練流程
    - ![AI 模型訓練流程](./ai_training_flow.png)

## DEMO 成果(YT)

## 專案初始化

```bash
$ mkdir ToyVisionPay_project
 # 建立專案資料夾
$ cd ToyVisionPay_project # 進入該專案資料夾
$ git init . # 在本地數據庫-建立空儲存庫

$ mkdir web_server
$ python3 -m venv web\_server/
$ source web\_server/bin/activate
$ cd web_server
$ touch server.py
$ flask --app server run --debug #runserver 你要在web_server底下執行
#or
$ flask --app server run --port 5001


```
