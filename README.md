# 周星驰电影论坛 (Steven Chow Movies Forum)

🎬 一个展示周星驰经典电影及其豆瓣评分的社区论坛

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌐 在线预览

**网站地址**: https://08vrut06mn63.space.minimaxi.com

## ✨ 功能特点

### 🏠 首页
- 展示周星驰经典电影（共12部）
- 显示豆瓣评分、导演、年份等信息
- 电影搜索过滤功能
- 按评分筛选（9分+/8分+/7分+）
- 点击电影卡片查看详细信息

### 📝 电影详情页
- 查看电影完整介绍和豆瓣评分
- 浏览和参与电影讨论
- 发布新帖和评论
- 点赞功能

### 👤 用户中心
- 查看个人信息
- 浏览所有电影
- 管理个人帖子

### 🔧 管理员后台
- 用户管理（升级/降级/删除）
- 统计数据概览
- 电影信息管理

## 🛠️ 技术栈

- **前端**: HTML5 + CSS3 + JavaScript (原生)
- **后端**: Python Flask
- **数据库**: SQLite
- **部署**: 静态页面 + 可选后端服务

## 📁 项目结构

```
steven_chow_forum/
├── app.py              # Flask 后端服务器
├── requirements.txt    # Python 依赖
├── templates/          # Flask 模板文件
│   ├── index.html      # 首页
│   ├── movie_detail.html
│   ├── login.html
│   ├── register.html
│   ├── user.html
│   └── admin.html
├── static/             # 静态资源
└── dist/               # 部署版本（纯静态）
```

## 🚀 快速开始

### 本地运行（完整版）

1. **克隆项目**
```bash
git clone <repository-url>
cd steven_chow_forum
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务器**
```bash
python app.py
```

4. **访问网站**
打开浏览器访问: http://localhost:5000

### 默认账号

- **用户名**: admin
- **密码**: admin123

## 🎬 收录电影

| 电影名称 | 年份 | 豆瓣评分 |
|---------|------|---------|
| 大话西游之大圣娶亲 | 1995 | 9.2 |
| 大话西游之月光宝盒 | 1995 | 9.0 |
| 喜剧之王 | 1999 | 8.8 |
| 功夫 | 2004 | 8.7 |
| 唐伯虎点秋香 | 1993 | 8.7 |
| 九品芝麻官 | 1994 | 8.6 |
| 少林足球 | 2001 | 8.1 |
| 国产凌凌漆 | 1994 | 8.1 |
| 食神 | 1996 | 8.1 |
| 鹿鼎记 | 1992 | 8.2 |
| 赌圣 | 1990 | 7.8 |
| 长江七号 | 2008 | 7.3 |

## 📝 API 接口

| 方法 | 路径 | 描述 |
|-----|------|-----|
| GET | `/api/movies` | 获取所有电影 |
| GET | `/api/movies/<id>` | 获取单个电影 |
| GET | `/api/posts` | 获取所有帖子 |
| POST | `/api/posts` | 创建帖子 |
| POST | `/api/comments` | 添加评论 |
| POST | `/api/like/<id>` | 点赞帖子 |
| POST | `/api/auth/login` | 用户登录 |
| POST | `/api/auth/register` | 用户注册 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

**致敬经典，欢笑永恒** 🎭