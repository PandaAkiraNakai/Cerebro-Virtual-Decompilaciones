---
tags: [decomp, index, ia, entrypoint]
creado: 2026-10-15
alias: [Indice IA, AI Index, Entrada]
proposito: Punto de entrada único y denso para que una IA recorra el vault con mínima lectura.
---

# 🧠 _INDEX (IA) — Punto de entrada

> [!abstract] Lee ESTO primero
> Mapa maestro del vault "Decompilaciones". Vista humana → [[Decompilaciones - MOC]].

## 1. Resumen del dominio (TL;DR)
Ingeniería inversa de binarios con **REA** (orquestador MCP/CLI) + **Ghidra 12.1.2**
headless (`/opt/ghidra`). Proyecto activo: **Pokémon Esmeralda ES** (GBA, BPES v0).
Como referencia usamos la decomp de pret (`pokeemerald`, versión USA BPEE), que compila
idéntica en `$HDD/GitHub/pokeemerald`. Portamos sus símbolos a la ROM
ES por coincidencia de bytes y se los damos a Ghidra como **semillas Thumb**, así el
pseudocódigo sale con nombres reales.

## 2. Grafo de dependencias (orden de lectura)
```
[[GBA - ARM7TDMI y Thumb]] ──► [[GBA - Mapa de memoria y cabecera]]
            │
            ▼
[[pret y agbcc]] ──(ELF con símbolos)──► [[Portar simbolos entre versiones]]
                                                │  seeds-es.tsv
                                                ▼
                                        [[REA + Ghidra]] ──► [[Flujo de trabajo]]
                                                                   │
                                                                   ▼
                                  [[Proyecto Esmeralda ES]] ──► [[CalculateBaseDamage]]
                                                                   [[Diferencias ES vs USA]]

Transversal: [[Gotchas y errores resueltos]] · [[Patrones de agbcc]] ·
             [[Bitacora de optimizaciones]] · [[Convenciones]] · [[Recursos y enlaces]]
```

## 3. Rutas y artefactos clave
`$HDD` = disco de trabajo de la torre (`/run/media/<usuario>/HDD`).

| Qué | Dónde |
|---|---|
| ROM ES (no se copia al vault) | `~/Descargas/Pokemon - Edicion Esmeralda (Spain).gba` |
| Decomp pret + agbcc | `$HDD/GitHub/{pokeemerald,agbcc}` |
| Scripts propios (versionados aquí) | `10 Herramientas/scripts/` |
| Artefactos generados (semillas, snapshot) | `~/.local/share/pokeemerald-es/` |
| REA (checkout fuente, con parche Thumb) | `~/Documentos/rea` |

## 4. Comandos de un vistazo
```sh
S="$HDD/Obsidian/Decompilaciones/10 Herramientas/scripts"
"$S/rea-es.sh" decompile --procedure CalculateBaseDamage --format json   # ~3,5 min (reanaliza)
python3 -I "$S/port_symbols.py" <elf> <rom_ref> <rom_destino> <salida.tsv> # ~3 min
```

## 5. Estado (2026-10-15)
- Símbolos portados: **12 901 / 15 853 (81,4 %)**; 95 nombres repetidos (funciones `static`).
- Funciones estudiadas a fondo: 1 ([[CalculateBaseDamage]]).
- Próximas mejoras: ver [[Bitacora de optimizaciones]] § Pendientes.
