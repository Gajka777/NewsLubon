# NewsPortal - Skrypt do pisania newsów na stronie internetowej

## Opis
Kompletny, gotowy do użycia portal newsowy zbudowany na Flask. 
Posiada wszystkie wymagane funkcje:
- Rejestracja i logowanie użytkowników
- Konto administratora z pełnymi uprawnieniami
- Konta redaktorów (autorów newsów)
- Dodawanie, edycja i usuwanie newsów
- Kategorie newsów (z lewej strony - sidebar)
- System komentarzy
- Panel administratora do zarządzania użytkownikami, kategoriami i treściami
- Przyjazny, responsywny interfejs w stylu portalu (Bootstrap 5)
- Możliwość rozbudowy (czysty kod, modularna struktura)

## 🚀 Szybki start na Render.com (zalecane)

### Krok po kroku (5 minut):

1. **Utwórz repozytorium na GitHub**
   - Załóż konto na [github.com](https://github.com) (jeśli nie masz)
   - Utwórz nowe repozytorium (publiczne lub prywatne)

2. **Wrzuć pliki**
   - Wgraj wszystkie pliki z tego folderu do repozytorium (oprócz `venv/`, `instance/`, `__pycache__/`)

3. **Połącz z Render**
   - Wejdź na [render.com](https://render.com) → Sign Up (z GitHub)
   - Kliknij **"New +"** → **"Web Service"**
   - Wybierz swoje repozytorium
   - Render automatycznie wykryje `render.yaml`

4. **Zakończ**
   - Kliknij **"Create Web Service"**
   - Po 1-2 minutach portal będzie dostępny na adresie typu `https://newsportal-xxx.onrender.com`

5. **Podłącz własną domenę** (opcjonalnie)
   - W Render → Settings → Custom Domains
   - Dodaj `lubon.net.pl` lub `www.lubon.net.pl`

**Dane logowania:**
- Admin: `admin` / `admin123`
- Redaktor: `redaktor1` / `author123`

---

## Szybki start (lokalnie na Twoim komputerze)

### 1. Przygotowanie
1. Rozpakuj plik `news_portal.zip` w dowolnym folderze na swoim komputerze.
2. Otwórz terminal (macOS/Linux) lub Wiersz poleceń / PowerShell (Windows) **w tym folderze**.

### 2. Zainstaluj wymagane biblioteki
```bash
pip install flask flask-login flask-wtf
```

### 3. Uruchom aplikację
```bash
python app.py
```
lub na Windows:
```bash
python app.py
```

### 4. Otwórz w przeglądarce
Wejdź na adres: **http://127.0.0.1:5000**

### Konta demo:
- **Administrator** (pełne uprawnienia): `admin` / `admin123`
- **Redaktor** (może dodawać/edytować newsy): `redaktor1` / `author123`

Przy pierwszym uruchomieniu baza danych (`instance/news.db`) zostanie automatycznie utworzona z domyślnymi kategoriami.

## Funkcje

### Dla wszystkich użytkowników:
- Przeglądanie newsów według kategorii (sidebar z lewej)
- Czytanie pełnych artykułów
- Dodawanie komentarzy (po zalogowaniu)

### Dla redaktorów i adminów:
- Dodawanie nowych newsów (`/create-news`)
- Edycja i usuwanie własnych newsów
- Możliwość dodawania URL zdjęcia

### Dla administratora:
- Panel `/admin`:
  - Statystyki portalu
  - Zarządzanie rolami użytkowników (user → author → admin)
  - Dodawanie i usuwanie kategorii
  - Lista najnowszych artykułów z linkami do edycji

## Struktura projektu

```
news_portal/
├── app.py              # Główna aplikacja Flask
├── schema.sql          # Schemat bazy danych
├── templates/          # Szablony Jinja2
│   ├── base.html       # Szablon bazowy z navbar i sidebar
│   ├── index.html      # Strona główna
│   ├── category.html   # Lista newsów w kategorii
│   ├── news_detail.html# Pełny artykuł + komentarze
│   ├── login.html
│   ├── register.html
│   ├── create_news.html
│   ├── edit_news.html
│   ├── admin_dashboard.html
│   ├── 404.html
│   └── 500.html
├── static/             # Pliki statyczne (CSS/JS/images)
└── instance/           # Baza danych (news.db)
```

## Rozbudowa

Aplikacja jest przygotowana do łatwej rozbudowy:

- **Nowe pola w newsach** — wystarczy dodać kolumnę w bazie i pola w formularzach
- **Tagi** — można dodać tabelę tags + relacje
- **Wyszukiwarka** — dodać route `/search?q=...`
- **Paginacja** — użyć Flask-SQLAlchemy lub ręcznie
- **Rich text editor** — zintegrować TinyMCE lub CKEditor
- **Upload zdjęć** — już przygotowany folder `static/uploads`
- **API REST** — dodać endpointy Flask-RESTful
- **Dark mode** — dodać przełącznik w base.html

## Bezpieczeństwo

- Hasła hashowane (Werkzeug)
- Flask-Login do zarządzania sesjami
- Ochrona przed nieautoryzowanym dostępem (dekoratory `@login_required`, `@admin_required`, `@author_required`)
- CSRF ochrona w formularzach (domyślnie w Flask)

## Uwagi

- Do produkcji zmień `SECRET_KEY` w `app.py`
- Użyj prawdziwej bazy (PostgreSQL/MySQL) przez SQLAlchemy
- Dodaj walidację i sanitizację treści (np. bleach)
- Skonfiguruj nginx + gunicorn dla produkcji

Stworzony dla Ciebie — gotowy do użycia i rozbudowy! 🚀
```

**Instrukcja:** Uruchom `python3 app.py` w katalogu `news_portal` i otwórz przeglądarkę pod adresem http://127.0.0.1:5000

Miłego pisania newsów! 🎉