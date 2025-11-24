@echo off
echo Video Emoji Service

if not exist .env (
    echo.
    echo [ERROR] .env not found.
    echo Скопируйте .env.example в .env и укажите TELEGRAM_BOT_TOKEN.
    echo Пример:
    echo   TELEGRAM_BOT_TOKEN=your_token_here
    echo   BACKEND_URL=http://backend:8000
    echo.
    pause
    exit /b 1
)

echo.
echo Starting containers...
docker compose up -d --build

echo.
echo Done. Open http://localhost in your browser.
echo Для остановки используйте stop.bat
echo.
pause
