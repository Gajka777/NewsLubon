import sys
import os

# Ścieżka do virtualenv (dhosting.pl tworzy ją automatycznie)
# Zostaw puste - panel sam to obsłuży
INTERP = "/usr/bin/python3"

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

from app import app as application