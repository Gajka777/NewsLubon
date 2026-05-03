#!/usr/bin/env python3
"""
News Portal - Skrypt do zarządzania newsami na stronie internetowej
Portal newsowy z użytkownikami, adminem, kategoriami, komentarzami
"""

import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for, 
    flash, g, session, abort
)
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user, 
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Konfiguracja
app = Flask(__name__)
app.config['SECRET_KEY'] = 'news-portal-secret-key-2026-change-in-production'
# Na Render używamy /tmp (plik jest tworzony przy każdym restarcie)
app.config['DATABASE'] = os.environ.get('DATABASE_URL', '/tmp/news.db')
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Upewnij się że foldery istnieją
os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicjalizacja bazy danych (ważne dla gunicorn / Render)
with app.app_context():
    init_db()

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'
login_manager.login_message_category = 'warning'

# Klasa User dla Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email, role):
        self.id = id
        self.username = username
        self.email = email
        self.role = role

    def is_admin(self):
        return self.role == 'admin'

    def is_author(self):
        return self.role in ('admin', 'author')

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute(
        'SELECT id, username, email, role FROM users WHERE id = ?', 
        (user_id,)
    ).fetchone()
    if user:
        return User(user['id'], user['username'], user['email'], user['role'])
    return None


def get_db():
    """Pobierz połączenie z bazą danych"""
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    """Zamknij połączenie z bazą po zakończeniu żądania"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Inicjalizacja bazy danych"""
    db = get_db()
    
    # Sprawdź czy tabela users istnieje
    tables = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
    ).fetchall()
    
    if not tables:
        # Wczytaj i wykonaj schema
        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf-8'))
        
        # Dodaj domyślne kategorie
        categories = [
            ('Sport', 'Najnowsze wiadomości sportowe'),
            ('Polityka', 'Polityka krajowa i międzynarodowa'),
            ('Technologia', 'Innowacje, IT, gadżety'),
            ('Biznes', 'Gospodarka, finanse, biznes'),
            ('Kultura', 'Sztuka, film, muzyka, literatura'),
            ('Zdrowie', 'Medycyna, porady zdrowotne'),
            ('Nauka', 'Odkrycia naukowe, badania'),
            ('Motoryzacja', 'Samochody, motocykle, transport'),
        ]
        for name, desc in categories:
            db.execute(
                'INSERT INTO categories (name, description) VALUES (?, ?)',
                (name, desc)
            )
        
        # Utwórz konto admina (jeśli nie istnieje)
        admin_pass = generate_password_hash('admin123')
        db.execute(
            '''INSERT OR IGNORE INTO users 
               (username, email, password, role) 
               VALUES (?, ?, ?, ?)''',
            ('admin', 'admin@newsportal.pl', admin_pass, 'admin')
        )
        
        # Przykładowy autor
        author_pass = generate_password_hash('author123')
        db.execute(
            '''INSERT OR IGNORE INTO users 
               (username, email, password, role) 
               VALUES (?, ?, ?, ?)''',
            ('redaktor1', 'redaktor@newsportal.pl', author_pass, 'author')
        )
        
        db.commit()
        print("Baza danych zainicjalizowana pomyślnie!")
        print("Konto admina: admin / admin123")
        print("Konto redaktora: redaktor1 / author123")


def admin_required(f):
    """Dekorator wymagający uprawnień admina"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Brak uprawnień administratora.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def author_required(f):
    """Dekorator wymagający uprawnień autora lub admina"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_author():
            flash('Tylko autorzy i administratorzy mogą dodawać newsy.', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Strona główna - lista najnowszych newsów"""
    db = get_db()
    
    # Pobierz wszystkie kategorie (do sidebar)
    categories = db.execute(
        'SELECT id, name FROM categories ORDER BY name'
    ).fetchall()
    
    # Pobierz najnowsze newsy (ostatnie 20)
    news = db.execute('''
        SELECT n.id, n.title, n.excerpt, n.created_at, n.image_url,
               c.name as category_name, u.username as author_name
        FROM news n
        JOIN categories c ON n.category_id = c.id
        JOIN users u ON n.author_id = u.id
        ORDER BY n.created_at DESC
        LIMIT 20
    ''').fetchall()
    
    return render_template('index.html', 
                         news=news, 
                         categories=categories,
                         title="Portal Newsowy")


@app.route('/category/<int:cat_id>')
def category(cat_id):
    """Newsy z danej kategorii"""
    db = get_db()
    
    categories = db.execute(
        'SELECT id, name FROM categories ORDER BY name'
    ).fetchall()
    
    cat = db.execute(
        'SELECT id, name, description FROM categories WHERE id = ?',
        (cat_id,)
    ).fetchone()
    
    if not cat:
        abort(404)
    
    news = db.execute('''
        SELECT n.id, n.title, n.excerpt, n.created_at, n.image_url,
               c.name as category_name, u.username as author_name
        FROM news n
        JOIN categories c ON n.category_id = c.id
        JOIN users u ON n.author_id = u.id
        WHERE n.category_id = ?
        ORDER BY n.created_at DESC
    ''', (cat_id,)).fetchall()
    
    return render_template('category.html',
                         news=news,
                         categories=categories,
                         current_category=cat,
                         title=f"Newsy - {cat['name']}")


@app.route('/news/<int:news_id>')
def news_detail(news_id):
    """Szczegóły newsa + komentarze"""
    db = get_db()
    
    categories = db.execute(
        'SELECT id, name FROM categories ORDER BY name'
    ).fetchall()
    
    news = db.execute('''
        SELECT n.*, c.name as category_name, u.username as author_name
        FROM news n
        JOIN categories c ON n.category_id = c.id
        JOIN users u ON n.author_id = u.id
        WHERE n.id = ?
    ''', (news_id,)).fetchone()
    
    if not news:
        abort(404)
    
    comments = db.execute('''
        SELECT c.id, c.content, c.created_at, u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.news_id = ?
        ORDER BY c.created_at ASC
    ''', (news_id,)).fetchall()
    
    return render_template('news_detail.html',
                         news=news,
                         comments=comments,
                         categories=categories,
                         title=news['title'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Rejestracja użytkownika"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        
        if not username or not email or not password:
            flash('Wszystkie pola są wymagane.', 'danger')
            return redirect(url_for('register'))
        
        if password != password2:
            flash('Hasła nie są identyczne.', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Hasło musi mieć minimum 6 znaków.', 'danger')
            return redirect(url_for('register'))
        
        db = get_db()
        
        # Sprawdź czy istnieje
        existing = db.execute(
            'SELECT id FROM users WHERE username = ? OR email = ?',
            (username, email)
        ).fetchone()
        
        if existing:
            flash('Użytkownik o podanej nazwie lub emailu już istnieje.', 'danger')
            return redirect(url_for('register'))
        
        # Utwórz użytkownika
        hashed = generate_password_hash(password)
        db.execute(
            'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
            (username, email, hashed, 'user')
        )
        db.commit()
        
        flash('Rejestracja pomyślna! Możesz się teraz zalogować.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title="Rejestracja")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logowanie"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            (username, username)
        ).fetchone()
        
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['id'], user['username'], user['email'], user['role'])
            login_user(user_obj)
            flash(f'Witaj, {user["username"]}!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Nieprawidłowa nazwa użytkownika lub hasło.', 'danger')
    
    return render_template('login.html', title="Logowanie")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Zostałeś wylogowany.', 'info')
    return redirect(url_for('index'))


@app.route('/create-news', methods=['GET', 'POST'])
@login_required
@author_required
def create_news():
    """Dodawanie nowego newsa"""
    db = get_db()
    categories = db.execute(
        'SELECT id, name FROM categories ORDER BY name'
    ).fetchall()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category_id = request.form.get('category_id', type=int)
        excerpt = request.form.get('excerpt', '').strip()
        image_url = request.form.get('image_url', '').strip()
        
        if not title or not content or not category_id:
            flash('Tytuł, treść i kategoria są wymagane.', 'danger')
            return redirect(url_for('create_news'))
        
        if not excerpt:
            excerpt = content[:200] + '...' if len(content) > 200 else content
        
        # Dodaj news
        db.execute('''
            INSERT INTO news (title, content, excerpt, category_id, author_id, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, excerpt, category_id, current_user.id, image_url or None))
        db.commit()
        
        flash('News został pomyślnie dodany!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_news.html',
                         categories=categories,
                         title="Dodaj nowy news")


@app.route('/edit-news/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    """Edycja newsa"""
    db = get_db()
    
    news = db.execute(
        'SELECT * FROM news WHERE id = ?',
        (news_id,)
    ).fetchone()
    
    if not news:
        abort(404)
    
    # Tylko autor lub admin
    if news['author_id'] != current_user.id and not current_user.is_admin():
        flash('Nie masz uprawnień do edycji tego newsa.', 'danger')
        return redirect(url_for('news_detail', news_id=news_id))
    
    categories = db.execute(
        'SELECT id, name FROM categories ORDER BY name'
    ).fetchall()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category_id = request.form.get('category_id', type=int)
        excerpt = request.form.get('excerpt', '').strip()
        image_url = request.form.get('image_url', '').strip()
        
        if not title or not content or not category_id:
            flash('Tytuł, treść i kategoria są wymagane.', 'danger')
            return redirect(url_for('edit_news', news_id=news_id))
        
        if not excerpt:
            excerpt = content[:200] + '...' if len(content) > 200 else content
        
        db.execute('''
            UPDATE news 
            SET title = ?, content = ?, excerpt = ?, category_id = ?, 
                image_url = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, content, excerpt, category_id, image_url or None, news_id))
        db.commit()
        
        flash('News został zaktualizowany!', 'success')
        return redirect(url_for('news_detail', news_id=news_id))
    
    return render_template('edit_news.html',
                         news=news,
                         categories=categories,
                         title="Edytuj news")


@app.route('/delete-news/<int:news_id>', methods=['POST'])
@login_required
def delete_news(news_id):
    """Usuwanie newsa"""
    db = get_db()
    
    news = db.execute(
        'SELECT author_id FROM news WHERE id = ?',
        (news_id,)
    ).fetchone()
    
    if not news:
        abort(404)
    
    if news['author_id'] != current_user.id and not current_user.is_admin():
        flash('Nie masz uprawnień do usunięcia tego newsa.', 'danger')
        return redirect(url_for('news_detail', news_id=news_id))
    
    db.execute('DELETE FROM news WHERE id = ?', (news_id,))
    db.commit()
    
    flash('News został usunięty.', 'success')
    return redirect(url_for('index'))


@app.route('/add-comment/<int:news_id>', methods=['POST'])
@login_required
def add_comment(news_id):
    """Dodawanie komentarza"""
    content = request.form.get('content', '').strip()
    
    if not content:
        flash('Komentarz nie może być pusty.', 'danger')
        return redirect(url_for('news_detail', news_id=news_id))
    
    db = get_db()
    
    # Sprawdź czy news istnieje
    news = db.execute('SELECT id FROM news WHERE id = ?', (news_id,)).fetchone()
    if not news:
        abort(404)
    
    db.execute(
        'INSERT INTO comments (news_id, user_id, content) VALUES (?, ?, ?)',
        (news_id, current_user.id, content)
    )
    db.commit()
    
    flash('Komentarz dodany!', 'success')
    return redirect(url_for('news_detail', news_id=news_id))


@app.route('/delete-comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Usuwanie komentarza (właściciel lub admin)"""
    db = get_db()
    
    comment = db.execute(
        'SELECT user_id, news_id FROM comments WHERE id = ?',
        (comment_id,)
    ).fetchone()
    
    if not comment:
        abort(404)
    
    if comment['user_id'] != current_user.id and not current_user.is_admin():
        flash('Nie masz uprawnień do usunięcia tego komentarza.', 'danger')
        return redirect(url_for('news_detail', news_id=comment['news_id']))
    
    db.execute('DELETE FROM comments WHERE id = ?', (comment_id,))
    db.commit()
    
    flash('Komentarz usunięty.', 'success')
    return redirect(url_for('news_detail', news_id=comment['news_id']))


# ==================== ADMIN PANEL ====================

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Panel administratora"""
    db = get_db()
    
    # Statystyki
    stats = {
        'users': db.execute('SELECT COUNT(*) FROM users').fetchone()[0],
        'news': db.execute('SELECT COUNT(*) FROM news').fetchone()[0],
        'comments': db.execute('SELECT COUNT(*) FROM comments').fetchone()[0],
        'categories': db.execute('SELECT COUNT(*) FROM categories').fetchone()[0],
    }
    
    # Ostatni użytkownicy
    users = db.execute('''
        SELECT id, username, email, role, created_at 
        FROM users ORDER BY created_at DESC LIMIT 10
    ''').fetchall()
    
    # Ostatnie newsy
    recent_news = db.execute('''
        SELECT n.id, n.title, n.created_at, u.username as author
        FROM news n JOIN users u ON n.author_id = u.id
        ORDER BY n.created_at DESC LIMIT 10
    ''').fetchall()
    
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    
    return render_template('admin_dashboard.html',
                         stats=stats,
                         users=users,
                         recent_news=recent_news,
                         categories=categories,
                         title="Panel Administratora")


@app.route('/admin/users/<int:user_id>/role', methods=['POST'])
@login_required
@admin_required
def change_user_role(user_id):
    """Zmiana roli użytkownika"""
    new_role = request.form.get('role')
    if new_role not in ('user', 'author', 'admin'):
        flash('Nieprawidłowa rola.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    db = get_db()
    db.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
    db.commit()
    
    flash('Rola użytkownika została zmieniona.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/categories/add', methods=['POST'])
@login_required
@admin_required
def add_category():
    """Dodawanie kategorii"""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not name:
        flash('Nazwa kategorii jest wymagana.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    db = get_db()
    try:
        db.execute(
            'INSERT INTO categories (name, description) VALUES (?, ?)',
            (name, description)
        )
        db.commit()
        flash('Kategoria dodana pomyślnie.', 'success')
    except sqlite3.IntegrityError:
        flash('Kategoria o takiej nazwie już istnieje.', 'danger')
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/categories/<int:cat_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(cat_id):
    """Usuwanie kategorii (tylko jeśli pusta)"""
    db = get_db()
    
    news_count = db.execute(
        'SELECT COUNT(*) FROM news WHERE category_id = ?',
        (cat_id,)
    ).fetchone()[0]
    
    if news_count > 0:
        flash('Nie można usunąć kategorii, która zawiera newsy.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    db.execute('DELETE FROM categories WHERE id = ?', (cat_id,))
    db.commit()
    flash('Kategoria usunięta.', 'success')
    return redirect(url_for('admin_dashboard'))


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="Nie znaleziono strony"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', title="Błąd serwera"), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*50)
    print("🚀 NEWS PORTAL uruchomiony!")
    print(f"   Adres: http://0.0.0.0:{port}")
    print("   Admin: admin / admin123")
    print("   Redaktor: redaktor1 / author123")
    print("="*50 + "\n")
    
    # W produkcji Render używa gunicorn, więc debug=False
    app.run(debug=False, host='0.0.0.0', port=port)