#!/bin/bash

echo "[+] Creating settings files"
cp settings.json.sample settings.json
cp subscribers.json.sample subscribers.json
cp blacklist.txt.sample blacklist.txt

echo "[OK] Files created"
echo "  [-] Put your settings on settings.json"
echo "  [-] Put your list's subscribers on subscribers.json following the given format"
echo "  [-] Put the moderated emails on blacklist.txt (one email per line)"
