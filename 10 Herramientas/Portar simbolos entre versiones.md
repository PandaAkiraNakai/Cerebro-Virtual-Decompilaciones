---
tags: [decomp, herramientas, simbolos, script]
creado: 2026-10-15
---

# 🏷️ Portar símbolos entre versiones

Script: `scripts/port_symbols.py`. Lleva los nombres de función de un ELF de referencia
(pret, USA) a otra ROM del mismo juego (ES) **sin símbolos**.

```sh
G=$HDD/GitHub/pokeemerald
python3 -I "scripts/port_symbols.py" $G/pokeemerald.elf $G/pokeemerald.gba \
  "$HOME/Descargas/Pokemon - Edicion Esmeralda (Spain).gba" \
  ~/.local/share/pokeemerald-es/seeds-es.tsv
```

## Cómo funciona
1. Lee del ELF cada `FUNC` con tamaño > 0 (bit 0 del valor = Thumb).
2. Toma sus bytes en la ROM de referencia y construye una regex con **comodines** en:
   - Palabras alineadas a 4 cuyo byte alto es `0x02`–`0x09` → punteros absolutos de
     *literal pool* (EWRAM, IWRAM, E/S, VRAM, ROM), que cambian si algo se movió.
   - Pares `BL` Thumb (`F000–F7FF` + `F800–FFFF`) → saltos relativos, que cambian si la
     función llamada se movió.
3. Busca primero en una ventana de ±128 KiB alrededor del **desplazamiento actual** (el
   código se mueve en tramos) y, si no aparece, en toda la ROM.
4. Acepta solo coincidencias **únicas** y con la misma alineación módulo 4.
5. Descarta atípicos: un delta que se aleja ≥ 4 KiB de dos vecinas que coinciden entre sí.
6. Escribe semillas `0x<dir>\tfunction\t<nombre>` (dir impar = Thumb) para [[REA + Ghidra]].

## Resultados medidos (Esmeralda USA → ES)
| Versión del script | Portadas | Notas |
|---|---|---|
| v1: comodines solo en punteros | 6 734 (42,5 %) | Los `BL` rompían casi todo |
| v2: + comodines en `BL` | **12 901 (81,4 %)** | 2 384 sin coincidencia única, 568 < 12 B |
| v3: + filtro de atípicos | 12 901 (81,4 %) | 0 descartadas: no había falsos positivos de ese tipo |

## Límites conocidos
- Funciones < 12 B (568) no se intentan: demasiado ambiguas.
- **95 nombres repetidos**: funciones `static` homónimas en distintos `.c`
  (p. ej. 8× `StartSendOutAnim`). Ghidra las acepta, pero `--procedure <nombre>` es
  ambiguo → usar la dirección. Mejora pendiente: sufijo con el archivo usando el `.map`.
- Una coincidencia única de bytes es una **inferencia**, no una prueba.
