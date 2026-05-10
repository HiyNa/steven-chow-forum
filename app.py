"""
周星驰电影论坛 - Flask 后端服务器
Steven Chow Movies Forum - Backend API Server
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'steven_chow_forum_secret_key_2024'
CORS(app)

DATABASE = 'forum.db'

# 周星驰电影数据（包含豆瓣评分）
MOVIES_DATA = [
    {
        "id": 1,
        "title": "大话西游之大圣娶亲",
        "year": 1995,
        "rating": 9.2,
        "director": "刘镇伟",
        "genre": "爱情/喜剧/奇幻",
        "duration": "110分钟",
        "description": "至尊宝（周星驰）被月光宝盒带回到五百年前，遇见紫霞仙子（朱茵），被对方打上烙印成为其奴仆，为了救白晶晶，他回到五百年前，但此时紫霞已爱上了他...",
        "poster": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2561716440.webp",
        "votes": 185632
    },
    {
        "id": 2,
        "title": "大话西游之月光宝盒",
        "year": 1995,
        "rating": 9.0,
        "director": "刘镇伟",
        "genre": "喜剧/爱情/奇幻",
        "duration": "105分钟",
        "description": "讲述了唐僧师徒前世的故事。孙悟空（周星驰）因陪唐三藏去西天取经，与牛魔王串通要吃掉唐僧，被观音菩萨惩罚转世为至尊宝...",
        "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2455053546.webp",
        "votes": 168542
    },
    {
        "id": 3,
        "title": "喜剧之王",
        "year": 1999,
        "rating": 8.8,
        "director": "周星驰/李力持",
        "genre": "剧情/喜剧/爱情",
        "duration": "89分钟",
        "description": "尹天仇（周星驰）是一个醉心戏剧却始终不得志的临时演员，他最大的理想就是成为一名真正的演员。在认识了舞女柳飘飘之后，他的生活开始发生变化...",
        "poster": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2572829926.webp",
        "votes": 145892
    },
    {
        "id": 4,
        "title": "功夫",
        "year": 2004,
        "rating": 8.7,
        "director": "周星驰",
        "genre": "喜剧/动作",
        "duration": "100分钟",
        "description": "1940年代的上海，自小受尽欺辱的街头混混阿星（周星驰）为了能出人头地，窥见机会想加入手段狠毒的黑帮斧头帮。他假冒\"斧头帮\"成员，试图在一个叫\"猪笼城寨\"的地方对居民敲诈...",
        "poster": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2561439800.webp",
        "votes": 156234
    },
    {
        "id": 5,
        "title": "少林足球",
        "year": 2001,
        "rating": 8.1,
        "director": "周星驰",
        "genre": "喜剧/动作/运动",
        "duration": "113分钟",
        "description": "二十年前，有“黄金右脚”之称的足球员明锋（吴孟达）被人打伤右脚，在一街边捡垃圾为生。偶然机会认识了星（周星驰），发现他的惊人力量，决定传授少林足球...",
        "poster": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2219775253.webp",
        "votes": 132456
    },
    {
        "id": 6,
        "title": "国产凌凌漆",
        "year": 1994,
        "rating": 8.1,
        "director": "周星驰/李力持",
        "genre": "喜剧/动作",
        "duration": "84分钟",
        "description": "凌凌漆（周星驰）是国家后备特工，长期被上级弃用。这次他被派往香港执行任务，调查恐龙化石被盗案件...",
        "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2355456517.webp",
        "votes": 98654
    },
    {
        "id": 7,
        "title": "九品芝麻官",
        "year": 1994,
        "rating": 8.6,
        "director": "王晶",
        "genre": "喜剧/古装",
        "duration": "108分钟",
        "description": "包龙星（周星驰）自幼家贫，但父亲常以贪官的下场告诫他要做一个清官。他长大后考取功名，成为一名县令，却因不会收受贿赂而被贬为八品...",
        "poster": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2561547409.webp",
        "votes": 118765
    },
    {
        "id": 8,
        "title": "唐伯虎点秋香",
        "year": 1993,
        "rating": 8.7,
        "director": "李力持",
        "genre": "喜剧/爱情/古装",
        "duration": "102分钟",
        "description": "唐伯虎（周星驰）身为江南四大才子之首，身边伴有八个老婆。但其实他常感叹真心的少之又少，直到有一次偶遇华府的秋香...",
        "poster": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2561435564.webp",
        "votes": 142678
    },
    {
        "id": 9,
        "title": "食神",
        "year": 1996,
        "rating": 8.1,
        "director": "李力持/周星驰",
        "genre": "喜剧",
        "duration": "100分钟",
        "description": "史蒂芬周（周星驰）是香港食神，人称食神。在一次与帮派冲突中，他被人陷害，失去了食神之位，落魄街头...",
        "poster": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2561714910.webp",
        "votes": 112345
    },
    {
        "id": 10,
        "title": "赌圣",
        "year": 1990,
        "rating": 7.8,
        "director": "元奎/刘镇伟",
        "genre": "喜剧/奇幻",
        "duration": "116分钟",
        "description": "左颂星（周星驰）是一个有特异功能的大陆青年，来到香港投奔三叔。三叔是个赌徒，他把左颂星带到了赌坛，希望他能利用特异功能在赌坛大展身手...",
        "poster": "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2561048776.webp",
        "votes": 87654
    },
    {
        "id": 11,
        "title": "鹿鼎记",
        "year": 1992,
        "rating": 8.2,
        "director": "王晶",
        "genre": "喜剧/古装",
        "duration": "110分钟",
        "description": "清朝初期，康熙皇帝为了对付在广西势力日益壮大的平西王吴三桂，把自己的格格建宁公主嫁到广西...",
        "poster": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2561439812.webp",
        "votes": 106789
    },
    {
        "id": 12,
        "title": "长江七号",
        "year": 2008,
        "rating": 7.3,
        "director": "周星驰",
        "genre": "喜剧/科幻/家庭",
        "duration": "86分钟",
        "description": "小狄（徐娇）是一个在单亲家庭长大的孩子，他的父亲周铁（周星驰）是一个穷困潦倒的工人，为了让儿子过上好日子...",
        "poster": "https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2191930566.webp",
        "votes": 95678
    }
]

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            avatar TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建帖子表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_id INTEGER,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # 创建评论表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # 创建点赞表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(post_id, user_id)
        )
    ''')
    
    # 创建管理员账号
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_password = hashlib.md5('admin123'.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            ('admin', admin_password, 'admin@stevenchow.com', 'admin')
        )
    
    # 创建示例帖子
    cursor.execute("SELECT COUNT(*) FROM posts")
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin_id = cursor.fetchone()[0]
        
        sample_posts = [
            (admin_id, 1, "《大话西游》为什么被称为经典？", 
             "这部电影不仅仅是一部喜剧，更是对爱情和命运的深刻思考。你们觉得至尊宝最后的选择对吗？", 1),
            (admin_id, 4, "《功夫》中的细节你注意到了吗？",
             "周星驰在这部电影里埋藏了很多致敬经典功夫片的彩蛋，细心的观众可以发现很多。", 1),
            (admin_id, 3, "《喜剧之王》 - 周星驰的自传",
             "有人说这是周星驰的自传式作品，反映了他早年跑龙套的经历。你们怎么看？", 1),
            (admin_id, 8, "《唐伯虎点秋香》经典台词大赏",
             "这部电影里有很多经典台词，比如'别人笑我太疯癫'，你们最喜欢哪一句？", 1),
            (admin_id, 7, "《九品芝麻官》的讽刺艺术",
             "王晶导演通过喜剧的形式讽刺了古代官场的黑暗，周星驰的表演堪称完美。", 1),
        ]
        
        for post in sample_posts:
            cursor.execute(
                "INSERT INTO posts (user_id, movie_id, title, content, views) VALUES (?, ?, ?, ?, ?)",
                post
            )
    
    conn.commit()
    conn.close()

def hash_password(password):
    """密码哈希"""
    return hashlib.md5(password.encode()).hexdigest()

# ==================== 页面路由 ====================

@app.route('/')
def index():
    """首页"""
    return render_template('index.html', movies=MOVIES_DATA)

@app.route('/user')
def user_page():
    """用户页面"""
    if 'user_id' not in session:
        return render_template('login.html', error="请先登录")
    return render_template('user.html', movies=MOVIES_DATA)

@app.route('/admin')
def admin_page():
    """管理员页面"""
    if 'user_id' not in session:
        return render_template('login.html', error="请先登录")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    if not user or user['role'] != 'admin':
        return render_template('index.html', movies=MOVIES_DATA, error="无权限访问管理员页面")
    
    return render_template('admin.html', movies=MOVIES_DATA)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """电影详情页"""
    movie = next((m for m in MOVIES_DATA if m['id'] == movie_id), None)
    if not movie:
        return "电影不存在", 404
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取该电影相关的帖子
    cursor.execute('''
        SELECT p.*, u.username, u.avatar
        FROM posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.movie_id = ?
        ORDER BY p.created_at DESC
    ''', (movie_id,))
    posts = [dict(row) for row in cursor.fetchall()]
    
    # 获取该电影的所有评论
    for post in posts:
        cursor.execute('''
            SELECT c.*, u.username, u.avatar
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        ''', (post['id'],))
        post['comments'] = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('movie_detail.html', movie=movie, posts=posts)

@app.route('/login')
def login_page():
    """登录页面"""
    return render_template('login.html')

@app.route('/register')
def register_page():
    """注册页面"""
    return render_template('register.html')

# ==================== API 路由 ====================

@app.route('/api/movies', methods=['GET'])
def get_movies():
    """获取所有电影"""
    return jsonify(MOVIES_DATA)

@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """获取单个电影详情"""
    movie = next((m for m in MOVIES_DATA if m['id'] == movie_id), None)
    if not movie:
        return jsonify({"error": "电影不存在"}), 404
    return jsonify(movie)

@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    """获取帖子列表或创建新帖子"""
    if request.method == 'GET':
        movie_id = request.args.get('movie_id')
        conn = get_db()
        cursor = conn.cursor()
        
        if movie_id:
            cursor.execute('''
                SELECT p.*, u.username, u.avatar
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.movie_id = ?
                ORDER BY p.created_at DESC
            ''', (movie_id,))
        else:
            cursor.execute('''
                SELECT p.*, u.username, u.avatar, m.title as movie_title
                FROM posts p
                JOIN users u ON p.user_id = u.id
                LEFT JOIN movies m ON p.movie_id = m.id
                ORDER BY p.created_at DESC
            ''')
        
        posts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(posts)
    
    elif request.method == 'POST':
        if 'user_id' not in session:
            return jsonify({"error": "请先登录"}), 401
        
        data = request.json
        movie_id = data.get('movie_id')
        title = data.get('title')
        content = data.get('content')
        
        if not title or not content:
            return jsonify({"error": "标题和内容不能为空"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (user_id, movie_id, title, content) VALUES (?, ?, ?, ?)",
            (session['user_id'], movie_id, title, content)
        )
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()
        
        return jsonify({"success": True, "post_id": post_id})

@app.route('/api/posts/<int:post_id>', methods=['GET', 'DELETE'])
def handle_post(post_id):
    """获取或删除帖子"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('''
            SELECT p.*, u.username, u.avatar
            FROM posts p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = ?
        ''', (post_id,))
        post = cursor.fetchone()
        
        if not post:
            conn.close()
            return jsonify({"error": "帖子不存在"}), 404
        
        # 增加浏览量
        cursor.execute("UPDATE posts SET views = views + 1 WHERE id = ?", (post_id,))
        conn.commit()
        
        # 获取评论
        cursor.execute('''
            SELECT c.*, u.username, u.avatar
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        ''', (post_id,))
        comments = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        result = dict(post)
        result['comments'] = comments
        return jsonify(result)
    
    elif request.method == 'DELETE':
        if 'user_id' not in session:
            return jsonify({"error": "请先登录"}), 401
        
        cursor.execute("SELECT user_id, movie_id FROM posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()
        
        if not post:
            conn.close()
            return jsonify({"error": "帖子不存在"}), 404
        
        cursor.execute("SELECT role FROM users WHERE id = ?", (session['user_id'],))
        user = cursor.fetchone()
        
        if post['user_id'] != session['user_id'] and user['role'] != 'admin':
            conn.close()
            return jsonify({"error": "无权限删除"}), 403
        
        cursor.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
        cursor.execute("DELETE FROM likes WHERE post_id = ?", (post_id,))
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"success": True})

@app.route('/api/comments', methods=['POST'])
def add_comment():
    """添加评论"""
    if 'user_id' not in session:
        return jsonify({"error": "请先登录"}), 401
    
    data = request.json
    post_id = data.get('post_id')
    content = data.get('content')
    
    if not post_id or not content:
        return jsonify({"error": "参数不完整"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)",
        (post_id, session['user_id'], content)
    )
    conn.commit()
    comment_id = cursor.lastrowid
    
    # 获取评论信息
    cursor.execute('''
        SELECT c.*, u.username, u.avatar
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.id = ?
    ''', (comment_id,))
    comment = dict(cursor.fetchone())
    conn.close()
    
    return jsonify(comment)

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """删除评论"""
    if 'user_id' not in session:
        return jsonify({"error": "请先登录"}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM comments WHERE id = ?", (comment_id,))
    comment = cursor.fetchone()
    
    if not comment:
        conn.close()
        return jsonify({"error": "评论不存在"}), 404
    
    cursor.execute("SELECT role FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    
    if comment['user_id'] != session['user_id'] and user['role'] != 'admin':
        conn.close()
        return jsonify({"error": "无权限删除"}), 403
    
    cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True})

@app.route('/api/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    """点赞/取消点赞"""
    if 'user_id' not in session:
        return jsonify({"error": "请先登录"}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查是否已点赞
    cursor.execute(
        "SELECT * FROM likes WHERE post_id = ? AND user_id = ?",
        (post_id, session['user_id'])
    )
    like = cursor.fetchone()
    
    if like:
        # 取消点赞
        cursor.execute("DELETE FROM likes WHERE post_id = ? AND user_id = ?",
                      (post_id, session['user_id']))
        cursor.execute("UPDATE posts SET likes = likes - 1 WHERE id = ?", (post_id,))
        liked = False
    else:
        # 添加点赞
        cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (?, ?)",
                      (post_id, session['user_id']))
        cursor.execute("UPDATE posts SET likes = likes + 1 WHERE id = ?", (post_id,))
        liked = True
    
    cursor.execute("SELECT likes FROM posts WHERE id = ?", (post_id,))
    likes_count = cursor.fetchone()['likes']
    
    conn.commit()
    conn.close()
    
    return jsonify({"liked": liked, "likes": likes_count})

@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    
    cursor.execute(
        "SELECT id, username, role, avatar FROM users WHERE username = ? AND password = ?",
        (username, hashed_password)
    )
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({"error": "用户名或密码错误"}), 401
    
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['role'] = user['role']
    
    return jsonify({
        "success": True,
        "user": {
            "id": user['id'],
            "username": user['username'],
            "role": user['role'],
            "avatar": user['avatar']
        }
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # 检查用户名是否已存在
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "用户名已存在"}), 400
    
    hashed_password = hash_password(password)
    cursor.execute(
        "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
        (username, hashed_password, email)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    
    session['user_id'] = user_id
    session['username'] = username
    session['role'] = 'user'
    
    return jsonify({
        "success": True,
        "user": {
            "id": user_id,
            "username": username,
            "role": "user"
        }
    })

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    return jsonify({"success": True})

@app.route('/api/auth/current', methods=['GET'])
def get_current_user():
    """获取当前用户信息"""
    if 'user_id' not in session:
        return jsonify({"logged_in": False})
    
    return jsonify({
        "logged_in": True,
        "user": {
            "id": session['user_id'],
            "username": session['username'],
            "role": session['role']
        }
    })

@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    """获取所有用户（管理员）"""
    if 'user_id' not in session:
        return jsonify({"error": "请先登录"}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({"error": "无权限"}), 403
    
    cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(users)

@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    """获取统计数据（管理员）"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM users")
    users_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM posts")
    posts_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM comments")
    comments_count = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify({
        "users": users_count,
        "posts": posts_count,
        "comments": comments_count,
        "movies": len(MOVIES_DATA)
    })

@app.route('/api/admin/users/<int:user_id>', methods=['PUT', 'DELETE'])
def manage_user(user_id):
    """管理用户（管理员）"""
    if 'user_id' not in session:
        return jsonify({"error": "请先登录"}), 401
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({"error": "无权限"}), 403
    
    if request.method == 'PUT':
        data = request.json
        new_role = data.get('role')
        if new_role in ['user', 'admin']:
            cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
            conn.commit()
            conn.close()
            return jsonify({"success": True})
        conn.close()
        return jsonify({"error": "无效的角色"}), 400
    
    elif request.method == 'DELETE':
        if user_id == session['user_id']:
            conn.close()
            return jsonify({"error": "不能删除自己"}), 400
        
        cursor.execute("DELETE FROM comments WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM likes WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM posts WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})

if __name__ == '__main__':
    init_db()
    print("=" * 50)
    print("🎬 周星驰电影论坛已启动!")
    print("=" * 50)
    print("📍 访问地址: http://localhost:5000")
    print("👤 管理员账号: admin / admin123")
    print("=" * 50)
    app.run(debug=True, port=5000)
