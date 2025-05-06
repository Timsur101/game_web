from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from functools import wraps
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id') or session.get('role') != 'admin':
            flash('Доступ запрещен. Требуются права администратора', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    
    # Новость недели (теперь включая image_path)
    cur.execute('''
        SELECT n.title, n.content, n.image_path, 
               g.title as game_name, u.username
        FROM news n
        JOIN games g ON n.id_game = g.id_game
        JOIN users u ON n.author_id = u.id_user
        WHERE n.is_weekly = TRUE
        LIMIT 1
    ''')
    weekly_news = cur.fetchone()
    
    # Обычные новости (без изменений)
    cur.execute('''
        SELECT n.title, n.content, g.title as game_name, u.username
        FROM news n
        JOIN games g ON n.id_game = g.id_game
        JOIN users u ON n.author_id = u.id_user
        WHERE n.is_weekly = FALSE OR n.is_weekly IS NULL
        ORDER BY n.id_news DESC
        LIMIT 10
    ''')
    regular_news = cur.fetchall()
    
    cur.close()
    
    return render_template('index.html',
                        weekly_news=weekly_news,
                        regular_news=regular_news)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        
        if user and user[3] == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[4]
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('index'))
        flash('Неверные учетные данные', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            mysql.connection.commit()
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Ошибка регистрации: {str(e)}', 'danger')
        finally:
            cur.close()
    return render_template('register.html')

@app.route('/add_news', methods=['GET', 'POST'])
@admin_required
def add_news():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        game_id = request.form['game_id']
        author_id = session['user_id']
        
        try:
            cur.execute("""
                INSERT INTO news (title, content, author_id, id_game)
                VALUES (%s, %s, %s, %s)
            """, (title, content, author_id, game_id))
            mysql.connection.commit()
            flash('Новость добавлена!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Ошибка: {str(e)}', 'danger')
    
    cur.execute("SELECT id_game, title FROM games")
    games = cur.fetchall()
    cur.close()
    return render_template('add_news.html', games=games)

@app.route('/weekly_news', methods=['GET', 'POST'])
@admin_required
def weekly_news():
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        try:
            cur.execute("UPDATE news SET is_weekly = FALSE")
            news_id = request.form['news_id']
            cur.execute("UPDATE news SET is_weekly = TRUE WHERE id_news = %s", (news_id,))
            
            if 'weekly_image' in request.files:
                file = request.files['weekly_image']
                if file and file.filename:
                    filename = secure_filename(f"weekly_{news_id}.{file.filename.rsplit('.', 1)[1].lower()}")
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    cur.execute("UPDATE news SET image_path = %s WHERE id_news = %s", 
                               (f"uploads/{filename}", news_id))
            
            mysql.connection.commit()
            flash('Новость недели обновлена!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Ошибка: {str(e)}', 'danger')
        finally:
            cur.close()
        return redirect(url_for('weekly_news'))
    
    cur.execute('SELECT id_news, title FROM news ORDER BY id_news DESC')
    news_list = cur.fetchall()
    
    cur.execute('''
        SELECT n.id_news, n.title, n.image_path, g.title as game_name 
        FROM news n
        JOIN games g ON n.id_game = g.id_game
        WHERE n.is_weekly = TRUE
        LIMIT 1
    ''')
    current_weekly = cur.fetchone()
    
    cur.close()
    return render_template('weekly_news.html',
                         news_list=news_list,
                         current_weekly=current_weekly)

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы успешно вышли из системы', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)