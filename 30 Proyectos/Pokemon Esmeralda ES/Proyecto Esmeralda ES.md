---
tags: [decomp, proyecto, gba, pokemon, esmeralda]
creado: 2026-10-15
actualizado: 2026-10-15
estado: activo
---

# 💚 Proyecto: Pokémon Esmeralda (ES)

Objetivo: **aprender ingeniería inversa** decompilando la versión española de Pokémon
Esmeralda, usando la decomp de pret (USA) como referencia para comprobar lo que sacamos.

## Identidad del binario
| Campo | Valor |
|---|---|
| Archivo | `~/Descargas/Pokemon - Edicion Esmeralda (Spain).gba` (no se copia al vault) |
| Tamaño | 16 777 216 B (16 MiB) |
| SHA-1 | `fe1558a3dcb0360ab558969e09b690888b846dd9` |
| SHA-256 | `e32c82bd10f174cf4019123b36f3ef7729105fb6634d9aa6b61413ee5101a55e` |
| Cabecera | `POKEMON EMER` · `BPES` · fabricante `01` · versión `0x00` |
| Referencia | pret/pokeemerald USA `BPEE`, sha1 `f3ae0881…` ([[pret y agbcc]]) |

## Configuración de análisis
- [[REA + Ghidra]]: `raw-binary`, `arm`, entrada `0x08000000`, Ghidra 12.1.2,
  `ARM:LE:32:v7`, 8 GiB de heap, semillas Thumb.
- Semillas: `~/.local/share/pokeemerald-es/seeds-es.tsv`
  ([[Portar simbolos entre versiones]]).
- Envoltorio: `10 Herramientas/scripts/rea-es.sh`.

## Estado
| Métrica | Valor | Fecha |
|---|---|---|
| Funciones en la referencia | 15 853 | 2026-10-15 |
| Funciones con nombre portado | **12 901 (81,4 %)** | 2026-10-15 |
| Semillas aplicadas en Ghidra | 12 901 creadas, 0 fallidas | 2026-10-15 |
| Funciones estudiadas | 1 | 2026-10-15 |

## Funciones estudiadas
```dataview
TABLE estado, dir_es AS "ES", dir_usa AS "USA", archivo
FROM "30 Proyectos/Pokemon Esmeralda ES/Funciones"
SORT file.name ASC
```
- [[CalculateBaseDamage]] — fórmula de daño (Gen III).

## Hallazgos
- El código ES está **desplazado por tramos** respecto a USA (0, +0x14, −0x3e8…): ver
  [[Diferencias ES vs USA]].

## Próximos pasos
- [ ] Estudiar las funciones que **cambiaron** en ES (Pokédex en sistema métrico, textos de combate…).
- [ ] Desambiguar los 95 nombres repetidos con el `.map`.
- [ ] Sesión MCP persistente para no reanalizar en cada consulta.
- [ ] Portar también **datos** (tablas como `gBattleMoves`, `gSpeciesInfo`) para que los `DAT_` tengan nombre.
