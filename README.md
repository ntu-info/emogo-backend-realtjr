[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/e7FBMwSa)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21926912&assignment_repo_type=AssignmentRepo)
# Deploy FastAPI on Render

Use this repo as a template to deploy a Python [FastAPI](https://fastapi.tiangolo.com) service on Render.

See https://render.com/docs/deploy-fastapi or follow the steps below:

## Manual Steps

1. You may use this repository directly or [create your own repository from this template](https://github.com/render-examples/fastapi/generate) if you'd like to customize the code.
2. Create a new Web Service on Render.
3. Specify the URL to your new repository or this repository.
4. Render will automatically detect that you are deploying a Python service and use `pip` to download the dependencies.
5. Specify the following as the Start Command.

    ```shell
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```

6. Click Create Web Service.

Or simply click:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/render-examples/fastapi)

# 🌟 EmoGo Backend — FastAPI + MongoDB (Render 部署)

本專案為 **NTU 心理資訊學（PsychoInformatics）作業**後端部分，使用 FastAPI + MongoDB 完成：

- 部署後端 API 到 Render
- 從 EmoGo 前端接收情緒紀錄（emotion / GPS / timestamp / video）
- Dashboard 頁面顯示所有資料
- 支援 JSON 與影片下載

---

## 🚀 Backend Base URL（後端主網址）

👉 **https://emogo-backend-realtjr.onrender.com**

---

# 📁 API Endpoints（作業要求功能）

## ✅ 1. Dashboard（資料視覺化頁）

顯示所有 records、影片下載連結、可一鍵下載 JSON。

👉 **https://emogo-backend-realtjr.onrender.com/dashboard**

---

## ✅ 2. 取得所有資料（JSON）


開啟網址：

👉 https://emogo-backend-realtjr.onrender.com/records

---

## ✅ 3. 下載所有資料（JSON 檔案）

👉 https://emogo-backend-realtjr.onrender.com/download/json

下載後檔名：`emogo_records.json`

---

## ✅ 4. 下載影片（已放在 static/videos/）

格式：


例如：

- https://emogo-backend-realtjr.onrender.com/download/video/record_1764263826626.webm  
- https://emogo-backend-realtjr.onrender.com/download/video/record_1764267414643.webm  

---

# 🧱 資料結構（EmogoRecord）

前端送到後端的資料格式如下：

```json
{
  "emotion": "happy",
  "location": { "lat": 24.1477, "lon": 120.6736 },
  "timestamp": 1764263826626,
  "video": "record_1764263826626.webm"
}
