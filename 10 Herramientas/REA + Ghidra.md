---
tags: [decomp, herramientas, rea, ghidra]
creado: 2026-10-15
---

# 🔬 REA + Ghidra

**REA** (Reverse Engineer Anything, `morluto/rea` v6.5.0) orquesta motores de análisis
y devuelve resultados con *Evidence* (qué se observó, con qué límites). Para binarios
nativos usa **Ghidra** en modo headless como proveedor.

## Instalación (torre)
- REA compilado desde fuente en `~/Documentos/rea` y registrado como MCP en Claude Code.
- Ghidra **12.1.2** desde los repos: `sudo pacman -S ghidra` → `/opt/ghidra`
  (REA está verificado contra 12.1.4, pero acepta cualquier 12.1.x).
- JDK 21: `/usr/lib/jvm/java-21-openjdk`.
- Comprobación: `GHIDRA_INSTALL_DIR=/opt/ghidra node ~/Documentos/rea/scripts/rea.mjs doctor --json`
  → todas las comprobaciones `ghidra-*` en `healthy`.

## Variables de entorno que usamos
| Variable | Valor | Para qué |
|---|---|---|
| `GHIDRA_INSTALL_DIR` | `/opt/ghidra` | Dónde está Ghidra |
| `JAVA_HOME` | `/usr/lib/jvm/java-21-openjdk` | JDK para Ghidra |
| `GHIDRA_HEADLESS_MAXMEM` | `8G` | Heap de la JVM (por defecto 2G) |
| `REA_GHIDRA_STARTUP_TIMEOUT_MS` | `5400000` | Margen para importar + auto-análisis |
| `REA_GHIDRA_SEED_FILE` | `seeds-es.tsv` | Funciones/nombres antes del auto-análisis |

## Binarios sin cabecera (ROM de GBA)
```sh
rea decompile ROM.gba --procedure Random \
  --target-format raw-binary --architecture arm --entry-point 0x08000000 \
  --provider ghidra --snapshot esmeralda-es.rea-snapshot
```
- Mapea el archivo completo desde `0x08000000` con `BinaryLoader`.
- Lenguaje fijo `ARM:LE:32:v7` (no hay un perfil v4t/GBA); decodifica bien el Thumb
  del ARM7TDMI, incluidos los `BL` de 2 medias palabras.
- Envoltorio listo: `scripts/rea-es.sh <comando> [args]`.

## Semillas Thumb (parche local)
El script de semillas de REA (`bridge/ghidra/ReaGhidraApplySeeds.java`) no fijaba el
modo Thumb y decodificaba todo como ARM. Lo parcheamos: **una dirección impar en una
semilla `function`/`code` activa `TMode=1`** en esa dirección y crea la función en la
dirección par. Parche guardado en `scripts/rea-thumb-seeds.patch`.

> [!warning] El parche es local
> Un `git pull` en `~/Documentos/rea` puede pisarlo o dar conflicto. Para volver a
> aplicarlo: `git -C ~/Documentos/rea apply "<vault>/10 Herramientas/scripts/rea-thumb-seeds.patch"`.
> Pendiente: proponerlo upstream.

## Rendimiento observado
- ROM de 16 MiB + 12 901 semillas: importación + auto-análisis + decompilación ≈ **3,5 min**.
- El `--snapshot` de la CLI solo guarda el perfil (~27 KB), **no** la base de Ghidra:
  cada llamada CLI vuelve a analizar. Para sesiones largas conviene el MCP (sesión
  persistente) → ver [[Bitacora de optimizaciones]].

Ver también: [[Gotchas y errores resueltos]], [[Flujo de trabajo]].
