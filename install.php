<?php
// NewsPortal - Webowy instalator (dla przeglądarki)
// Umieść ten plik w tym samym folderze co app.py

$step = isset($_GET['step']) ? (int)$_GET['step'] : 1;
$baseUrl = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
$baseUrl = rtrim(dirname($baseUrl), '/\\');
?>
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsPortal - Instalator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .card { border: none; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        .step { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        .step.active { background: #0d6efd; color: white; }
        .step.done { background: #198754; color: white; }
        .terminal { background: #1e1e1e; color: #00ff00; font-family: 'Courier New', monospace; padding: 20px; border-radius: 10px; }
        .copy-btn { position: absolute; top: 10px; right: 10px; }
    </style>
</head>
<body>
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            
            <!-- Header -->
            <div class="text-center mb-4">
                <i class="bi bi-newspaper display-1 text-white"></i>
                <h1 class="text-white mt-3">NewsPortal</h1>
                <p class="text-white-50">Instalator przez przeglądarkę</p>
            </div>

            <div class="card">
                <div class="card-body p-5">
                    
                    <!-- Progress -->
                    <div class="d-flex justify-content-between mb-4">
                        <?php for($i=1; $i<=4; $i++): ?>
                            <div class="text-center">
                                <div class="step mx-auto mb-2 <?= $i < $step ? 'done' : ($i == $step ? 'active' : 'bg-light text-muted') ?>">
                                    <?= $i ?>
                                </div>
                                <small class="text-muted">
                                    <?= $i==1 ? 'Sprawdzenie' : ($i==2 ? 'SSH' : ($i==3 ? 'Instalacja' : 'Gotowe')) ?>
                                </small>
                            </div>
                        <?php endfor; ?>
                    </div>

                    <?php if($step == 1): ?>
                        <!-- KROK 1: Sprawdzenie środowiska -->
                        <h3 class="mb-4"><i class="bi bi-search me-2"></i>Krok 1: Sprawdzenie środowiska</h3>
                        
                        <div class="alert alert-info">
                            <i class="bi bi-info-circle me-2"></i>
                            Ten instalator pomoże Ci uruchomić NewsPortal na Twoim hostingu.
                        </div>

                        <h5>Co musisz mieć:</h5>
                        <ul class="list-group mb-4">
                            <li class="list-group-item"><i class="bi bi-check-circle text-success me-2"></i> Dostęp do SSH (Secure Shell)</li>
                            <li class="list-group-item"><i class="bi bi-check-circle text-success me-2"></i> Python 3.8+ na serwerze</li>
                            <li class="list-group-item"><i class="bi bi-check-circle text-success me-2"></i> pip (menedżer pakietów Python)</li>
                        </ul>

                        <div class="d-grid">
                            <a href="?step=2" class="btn btn-primary btn-lg">
                                Rozpocznij instalację <i class="bi bi-arrow-right ms-2"></i>
                            </a>
                        </div>

                    <?php elseif($step == 2): ?>
                        <!-- KROK 2: Instrukcje SSH -->
                        <h3 class="mb-4"><i class="bi bi-terminal me-2"></i>Krok 2: Połącz się przez SSH</h3>
                        
                        <div class="alert alert-warning">
                            <i class="bi bi-exclamation-triangle me-2"></i>
                            <strong>Potrzebujesz dostępu SSH.</strong> Jeśli nie masz, poproś support dhosting.pl o jego włączenie.
                        </div>

                        <h5>Jak się połączyć:</h5>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="card bg-light mb-3">
                                    <div class="card-body">
                                        <h6><i class="bi bi-windows me-2"></i>Windows (PuTTY)</h6>
                                        <small>Pobierz PuTTY → wpisz host: <code>twojadomena.pl</code></small>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card bg-light mb-3">
                                    <div class="card-body">
                                        <h6><i class="bi bi-apple me-2"></i>Mac / Linux</h6>
                                        <small>Otwórz Terminal i wpisz:<br><code>ssh login@twojadomena.pl</code></small>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-between mt-4">
                            <a href="?step=1" class="btn btn-outline-secondary">← Wstecz</a>
                            <a href="?step=3" class="btn btn-primary">Mam SSH, kontynuuj →</a>
                        </div>

                    <?php elseif($step == 3): ?>
                        <!-- KROK 3: Komendy instalacyjne -->
                        <h3 class="mb-4"><i class="bi bi-terminal-fill me-2"></i>Krok 3: Uruchom instalację</h3>
                        
                        <p>Połącz się przez SSH i wpisz te komendy <strong>po kolei</strong>:</p>

                        <div class="position-relative mb-3">
                            <div class="terminal">
                                <code>cd public_html/news</code>
                            </div>
                            <button class="btn btn-sm btn-outline-light copy-btn" onclick="copyToClipboard(this, 'cd public_html/news')">
                                <i class="bi bi-clipboard"></i>
                            </button>
                        </div>

                        <div class="position-relative mb-3">
                            <div class="terminal">
                                <code>bash install.sh</code>
                            </div>
                            <button class="btn btn-sm btn-outline-light copy-btn" onclick="copyToClipboard(this, 'bash install.sh')">
                                <i class="bi bi-clipboard"></i>
                            </button>
                        </div>

                        <div class="alert alert-success mt-4">
                            <i class="bi bi-lightbulb me-2"></i>
                            <strong>Instalator zrobi wszystko automatycznie!</strong><br>
                            Zainstaluje biblioteki, przygotuje bazę danych i pokaże Ci jak uruchomić portal.
                        </div>

                        <div class="d-flex justify-content-between mt-4">
                            <a href="?step=2" class="btn btn-outline-secondary">← Wstecz</a>
                            <a href="?step=4" class="btn btn-primary">Zainstalowałem, dalej →</a>
                        </div>

                    <?php elseif($step == 4): ?>
                        <!-- KROK 4: Gotowe -->
                        <div class="text-center py-4">
                            <i class="bi bi-check-circle-fill display-1 text-success"></i>
                            <h2 class="mt-4 text-success">Instalacja zakończona!</h2>
                            
                            <div class="alert alert-light mt-4 text-start">
                                <h5>Twoje dane logowania:</h5>
                                <table class="table table-sm mb-0">
                                    <tr><td><strong>Admin</strong></td><td><code>admin</code> / <code>admin123</code></td></tr>
                                    <tr><td><strong>Redaktor</strong></td><td><code>redaktor1</code> / <code>author123</code></td></tr>
                                </table>
                            </div>

                            <div class="mt-4">
                                <h5>Wejdź na portal:</h5>
                                <a href="<?= $baseUrl ?>" target="_blank" class="btn btn-success btn-lg">
                                    <i class="bi bi-box-arrow-up-right me-2"></i>Otwórz NewsPortal
                                </a>
                            </div>

                            <div class="mt-4 text-muted small">
                                Jeśli coś nie działa, wróć do SSH i wpisz:<br>
                                <code>screen -r newsportal</code>
                            </div>
                        </div>
                    <?php endif; ?>

                </div>
            </div>

            <div class="text-center mt-4">
                <small class="text-white-50">NewsPortal • Automatyczny instalator • dhosting.pl</small>
            </div>

        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
function copyToClipboard(element, text) {
    navigator.clipboard.writeText(text).then(() => {
        const originalHTML = element.innerHTML;
        element.innerHTML = '<i class="bi bi-check-lg"></i>';
        element.classList.add('btn-success');
        element.classList.remove('btn-outline-light');
        
        setTimeout(() => {
            element.innerHTML = originalHTML;
            element.classList.remove('btn-success');
            element.classList.add('btn-outline-light');
        }, 1500);
    }).catch(() => {
        // Fallback dla starszych przeglądarek
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        alert('Skopiowano: ' + text);
    });
}
</script>
</body>
</html>