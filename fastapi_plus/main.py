from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="FastAPI Plus", description="工程化 FastAPI 模板项目", version="0.1.0")

# 添加跨域支持（可选）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产建议改为指定前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 示例接口
@app.get("/")
async def root():
    return {"message": "🚀 FastAPI Plus 项目启动成功！"}

# 入口函数
def main():
    uvicorn.run("fastapi_plus.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
