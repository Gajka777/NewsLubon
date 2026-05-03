<?php
// NewsPortal - Strona startowa (landing page)
// Umieść w głównym katalogu domeny (public_html/)
?>
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsPortal • lubon.net.pl</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #0d6efd 0%, #6610f2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .hero {
            text-align: center;
            color: white;
        }
        .hero h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .hero .lead {
            font-size: 1.4rem;
            opacity: 0.9;
        }
        .btn-portal {
            background: white;
            color: #0d6efd;
            font-weight: 600;
            padding: 15px 50px;
            font-size: 1.2rem;
            border-radius: 50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .btn-portal:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            color: #0d6efd;
        }
        .features {
            margin-top: 3rem;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem;
            backdrop-filter: blur(10px);
        }
        .footer {
            position: fixed;
            bottom: 20px;
            width: 100%;
            text-align: center;
            color: rgba(255,255,255,0.6);
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <i class="bi bi-newspaper display-1 mb-4"></i>
            <h1>NewsPortal</h1>
            <p class="lead">Twój portal informacyjny<br>zawsze na bieżąco</p>
            
            <div class="mt-5">
                <a href="http://109.95.158.122:5000" target="_blank" class="btn btn-portal btn-lg">
                    <i class="bi bi-box-arrow-up-right me-2"></i>
                    Wejdź do portalu (testowo)
                </a>
                <div class="mt-3">
                    <small style="opacity:0.7">Później skonfigurujemy domenę (Proxy w panelu)</small>
                </div>
            </div>

            <div class="row features justify-content-center mt-5">
                <div class="col-md-3">
                    <div class="feature">
                        <i class="bi bi-tags fs-2 mb-3 d-block"></i>
                        <h5>Kategorie</h5>
                        <p class="small mb-0">Sport, Polityka, Technologia i więcej</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="feature">
                        <i class="bi bi-chat-dots fs-2 mb-3 d-block"></i>
                        <h5>Komentarze</h5>
                        <p class="small mb-0">Dyskutuj z innymi czytelnikami</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="feature">
                        <i class="bi bi-person-badge fs-2 mb-3 d-block"></i>
                        <h5>Panel Admina</h5>
                        <p class="small mb-0">Zarządzaj newsami i użytkownikami</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>NewsPortal • lubon.net.pl • 2026</p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>