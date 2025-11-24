#!/bin/sh
set -e

echo "Stopping Video Emoji Service containers..."

docker compose down

echo
echo "Done."
