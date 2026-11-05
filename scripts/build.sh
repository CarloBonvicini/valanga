#!/usr/bin/env bash
# Assembles the installable site in dist/ from the game page and web/.
set -euo pipefail

BUILD="${GITHUB_SHA:-local}"
BUILD="${BUILD:0:7}"

rm -rf dist
mkdir dist
cp web/* dist/

{
  cat <<'HTML'
<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="theme-color" content="#0d2229">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-192.png">
<script>
window.VALANGA_BUILD = '__BUILD__';
if ('serviceWorker' in navigator) {
  addEventListener('load', () => navigator.serviceWorker.register('sw.js'));
}
</script>
HTML
  cat prototype/index.html
} > dist/index.html

sed -i "s/__BUILD__/${BUILD}/g" dist/index.html dist/sw.js
echo "Built ${BUILD}: $(du -sh dist | cut -f1)"
