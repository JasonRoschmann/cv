#!/usr/bin/env bash
# CI-Werkzeuge für den PDF-Build: pandoc 3.10 (gepinnt + Prüfsumme), Poppler, Arial-kompatible Schrift
set -euo pipefail
sudo apt-get update -qq
sudo apt-get install -y -qq poppler-utils fonts-liberation fonts-dejavu-core
curl -fsSL -o /tmp/pandoc.deb https://github.com/jgm/pandoc/releases/download/3.10/pandoc-3.10-1-amd64.deb
echo "d502599878eb29af3ae5f0cb5d559134df96534125d452c7a0674a5bad2c5ecf  /tmp/pandoc.deb" | sha256sum -c -
sudo dpkg -i /tmp/pandoc.deb
pandoc --version | head -1
google-chrome --version
