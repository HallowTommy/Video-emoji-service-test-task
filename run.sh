#!/bin/sh
set -e

echo "Video Emoji Service"

if [ ! -f .env ]; then
  echo
  echo "[ERROR] .env not found."
  echo "Скопируйте .env.example в .env и укажите TELEGRAM_BOT_TOKEN."
  echo "Пример:"
  echo "  TELEGRAM_BOT_TOKEN=your_token_here"
  echo "  BACKEND_URL=http://backend:8000"
  exit 1
fi

echo
echo "Starting containers..."
docker compose up -d --build

echo
echo "Done. Open http://localhost in your browser."
echo "Для остановки используйте ./stop.sh"
