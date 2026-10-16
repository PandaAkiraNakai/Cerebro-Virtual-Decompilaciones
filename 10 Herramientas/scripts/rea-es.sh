#!/usr/bin/env bash
# Ejecuta un comando de REA (Ghidra) sobre la Esmeralda española con los
# símbolos portados de pret/pokeemerald. Cada llamada importa y analiza la ROM
# (~3,5 min); el snapshot solo guarda el perfil de análisis.
# Uso: rea-es.sh <comando-rea> [args...]   p. ej.: rea-es.sh decompile --procedure Random
set -euo pipefail
DATA="$HOME/.local/share/pokeemerald-es"     # artefactos generados (fuera del vault)
ROM="$HOME/Descargas/Pokemon - Edicion Esmeralda (Spain).gba"

export GHIDRA_INSTALL_DIR=/opt/ghidra
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk
export GHIDRA_HEADLESS_MAXMEM=8G
export REA_GHIDRA_STARTUP_TIMEOUT_MS=5400000
export REA_GHIDRA_SEED_FILE="$DATA/seeds-es.tsv"

cmd="$1"; shift
exec node "$HOME/Documentos/rea/scripts/rea.mjs" "$cmd" "$ROM" "$@" \
  --target-format raw-binary --architecture arm --entry-point 0x08000000 \
  --provider ghidra --snapshot "$DATA/esmeralda-es.rea-snapshot"
