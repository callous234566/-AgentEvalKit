# 启动 RAG 知识库助手前端服务
# 使用 Python 3.11 环境

Write-Host "正在启动 Streamlit 前端服务..." -ForegroundColor Green
Write-Host "服务地址：http://localhost:8501" -ForegroundColor Yellow
Write-Host ""

D:\anaconda3\envs\ai_project\python.exe -m streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
