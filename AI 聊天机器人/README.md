# AI 聊天机器人

一个基于 RAG（检索增强生成）技术的智能问答系统，支持用户上传文档资料进行训练，实现基于个人知识库的智能问答。

## 项目结构

```
├── backend/                 # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py         # FastAPI 应用入口
│   │   ├── api/
│   │   │   ├── upload.py   # 文件上传 API
│   │   │   ├── chat.py     # 聊天对话 API
│   │   │   └── knowledge.py # 知识库管理 API
│   │   ├── models/
│   │   │   └── schemas.py  # 数据模型
│   │   └── services/
│   │       ├── document_processor.py  # 文档解析
│   │       ├── embeddings.py          # 文本向量化
│   │       ├── vector_store.py         # 向量存储
│   │       ├── rag_engine.py          # RAG 问答引擎
│   │       └── conversation_store.py  # 对话记录
│   ├── storage/             # 数据存储目录
│   └── run.py               # 启动脚本
├── web-ui/                  # Web 测试界面
│   └── index.html
├── miniprogram/             # 微信小程序源码
│   ├── app.json
│   ├── app.js
│   ├── app.wxss
│   └── pages/
│       ├── chat/            # 对话页面
│       ├── upload/          # 上传页面
│       └── knowledge/       # 知识库页面
└── README.md
```

## 快速启动

### 后端服务

```bash
cd backend
python run.py
```

服务将在 http://localhost:8000 启动，Web UI 自动可用。

### API 接口

- `GET /api/health` - 健康检查
- `POST /api/upload` - 上传文档
- `POST /api/chat` - 发送消息
- `GET /api/knowledge/list` - 获取知识库列表
- `DELETE /api/knowledge/{id}` - 删除文档
- `GET /api/knowledge/stats` - 知识库统计

### 微信小程序部署

1. 打开微信开发者工具
2. 导入 `miniprogram/` 目录
3. 修改 `app.js` 中的 `apiBaseUrl` 为你的服务器地址
4. 在微信小程序后台配置服务器域名白名单
5. 上传并发布

## 技术栈

- **后端**: Python FastAPI + scikit-learn (TF-IDF)
- **向量化**: TF-IDF + Cosine Similarity
- **中文分词**: jieba
- **前端测试**: 原生 HTML/CSS/JS
- **微信小程序**: 原生小程序框架
