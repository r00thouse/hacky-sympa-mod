#!/bin/bash

echo "[+] Creating settings files"
cp settings.json.sample settings.json
cp subscribers.json.sample subscribers.json

echo "[OK] Files created"
echo "  [-] Put your settings on settings.json"
echo "  [-] Put your list's subscribers on subscribers.json following the given format"
