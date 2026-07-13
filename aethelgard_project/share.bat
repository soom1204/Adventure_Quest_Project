@echo off
title Aethelgard - Web Server
echo.
echo   ============================================
echo     AETHELGARD - Web Edition
echo   ============================================
echo.
echo   Starting server on port 5000...
echo   Open http://localhost:5000 in your browser
echo.
echo   To share with friends over the internet:
echo   1. Download cloudflared from:
echo      https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
echo   2. In another terminal, run:
echo      cloudflared tunnel --url http://localhost:5000
echo   3. Copy the public URL it gives you and share it
echo.
echo   Press Ctrl+C to stop the server.
echo   ============================================
echo.
python server.py
pause
