#!/bin/bash
################################################################################
# NewsPortal - Automatyczny instalator (wersja bez venv - dla shared hostingu)
# Uruchom: bash install.sh
################################################################################

echo "🚀 NewsPortal - Automatyczny instalator (wersja bez venv)"
echo "========================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Błąd: Nie znaleziono pliku app.py${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Znaleziono pliki aplikacji${NC}"

# Sprawdź Pythona
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}✅ Python3: $(python3 --version)${NC}"
else
    echo -e "${RED}❌ Nie znaleziono Python3!${NC}"
    exit 1
fi

echo ""
echo "📥 Instalowanie bibliotek (używam --user - bez roota)..."

# Spróbuj użyć pip z --user
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3 install --user"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip install --user"
else
    PIP_CMD="$PYTHON_CMD -m pip install --user"
fi

echo "Używana komenda: $PIP_CMD"

# Zainstaluj zależności
$PIP_CMD -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Biblioteki zainstalowane pomyślnie${NC}"
else
    echo -e "${RED}❌ Błąd instalacji${NC}"
    echo ""
    echo "Spróbuj ręcznie:"
    echo "  $PIP_CMD flask==2.0.3 flask-login==0.5.0 flask-wtf==1.0.1"
    exit 1
fi

# Utwórz folder instance
mkdir -p instance

# Inicjalizacja bazy
echo ""
echo "🗄️  Inicjalizacja bazy danych..."

$PYTHON_CMD -c "
import sys
sys.path.insert(0, '.')
from app import app, init_db
with app.app_context():
    init_db()
print('Baza danych gotowa!')
" 2>/dev/null || echo -e "${YELLOW}⚠️  Baza już istnieje${NC}"

echo ""
echo "========================================"
echo -e "${GREEN}✅ INSTALACJA ZAKOŃCZONA!${NC}"
echo "========================================"
echo ""
echo "📌 Uruchom portal:"
echo ""
echo "   screen -S newsportal"
echo "   $PYTHON_CMD app.py"
echo ""
echo "   (Ctrl+A, potem D żeby odłączyć)"
echo ""
echo "🌐 Wejdź na: https://twojadomena.pl/news"
echo ""
echo "🔑 Login: admin / admin123"
echo ""
echo "Jeśli proces zostanie zabity - uruchom ponownie powyższe komendy."
echo "========================================"