#!/bin/bash

echo "[+] Creating settings files"
cp settings.json.sample settings.json
cp subscribers.json.sample subscribers.json
cp listanegra.txt.sample listanegra.txt

echo "[OK] Files created"
echo "  [-] Put your settings on settings.json"
echo "  [-] Put your list's subscribers on subscribers.json following the given format"
echo "  [-] Put the moderated emails on listanegra.txt (one email per line)"
