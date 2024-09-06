# 專案大綱

- 剛結束健行科大 AIOT 人工智慧既實戰班，就想把 AI 這塊和物聯網串連起來，於是以自己手邊有的寶可夢公仔為資料，做公仔商品辨識結帳系統，以下是我四大階段：
  - 第一階段=> AI：收集資料 與 YOLOV4-TINY 訓練自己的模型
  - 第二階段=> IOT: AME882
  - 第三階段=> 後端： FLASK
  - 第四階段=> 前端： 購物車顯示與結帳

## AI 模型訓練 與 IOT 的結合

- 我把自己實作的詳細筆記寫在:

  - [(AI 模型訓練)如何訓練並使用自己建好的 YOLOv4-tiny 模型](https://hackmd.io/ImQCIrtrQquPfkxcwYCUxw)
  - [IOT:AMB882 模型轉檔 使用自己建好的模型](https://hackmd.io/QMJgo3SaQw27v_8IS0a3cw?view)

- AI 模型訓練流程與架構圖
  - ![ai_training_flow.png](./ai_training_flow.png)

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

```
