---
tags: [decomp, optimizacion, bitacora]
creado: 2026-10-15
---

# 📈 Bitácora de optimizaciones

Cada mejora del proceso, **medida**: qué cambiamos, antes → después, y por qué funcionó.

## Registro
| Fecha | Cambio | Antes | Después | Por qué |
|---|---|---|---|---|
| 2026-10-15 | Ghidra + REA sobre la ROM ES | sin decompilador | pseudocódigo de cualquier función | Proveedor de análisis profundo instalado |
| 2026-10-15 | Portar símbolos de pret (v1: comodines en punteros) | 0 nombres | 6 734 (42,5 %) | Los literal pools cambian entre versiones |
| 2026-10-15 | v2: comodines también en `BL` Thumb | 42,5 % | **81,4 %** | Los `BL` son relativos: cambian si la función llamada se movió |
| 2026-10-15 | Semillas Thumb (`TMode`) en REA | Thumb mal decodificado | 12 901 funciones creadas, 0 fallidas | Ghidra necesita el contexto `TMode` |
| 2026-10-15 | v3: filtro de atípicos | — | 0 descartadas | Red de seguridad; los "atípicos" eran nombres repetidos |

## Pendientes (ordenadas por impacto esperado)
- [ ] **Sesión MCP persistente** con `GHIDRA_INSTALL_DIR` en el registro de REA: de ~3,5 min por consulta a segundos (requiere reiniciar Claude Code).
- [ ] **Portar datos además de funciones** (`OBJECT` del ELF: `gBattleMoves`, `gSpeciesInfo`…) como semillas `label` → los `DAT_` tendrían nombre.
- [ ] **Importar tipos** (structs de `include/*.h` de pret) en Ghidra → `param_1->item` en vez de `param_1[0x17]`.
- [ ] **Desambiguar nombres `static`** con el `.map` (`Nombre@archivo`).
- [ ] Rescatar parte de las 2 384 funciones sin coincidencia: comparación difusa (ratio de bytes iguales) en el hueco entre vecinas ya portadas.
- [ ] Acelerar el script (~3 min): índice por *n-gramas* en vez de una regex por función.
- [ ] Proponer el parche Thumb de semillas a REA upstream.
