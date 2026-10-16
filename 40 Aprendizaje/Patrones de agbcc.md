---
tags: [decomp, compilador, agbcc, patrones]
creado: 2026-10-15
---

# 🧬 Patrones de agbcc en el pseudocódigo de Ghidra

Cómo se ve el C de Game Freak (compilado con agbcc, GCC ~2.95) después de pasar por
Ghidra. Reconocer estos patrones es lo que más acelera la lectura.

| Lo que ves en Ghidra | Lo que era en C | Por qué |
|---|---|---|
| `__divsi3(x * 0x6e, 100)` | `x * 110 / 100` | El ARM7TDMI no divide por hardware: llama a la rutina de libgcc |
| `uVar = uVar & 0xffff` tras cada operación | variable `u16` | Los registros son de 32 bits; agbcc re-enmascara al guardar en `u16` |
| `param_7 = param_7 & 0xff` al inicio | argumento `u8` | Los argumentos llegan en registros de 32 bits |
| `(x & 0x7fff) << 1` | `x * 2` sobre `u16` | Multiplicar por 2 y truncar a 16 bits |
| `DAT_08069630` | dirección de una tabla/global (`gEnigmaBerries`) | *Literal pool*: la constante de 32 bits va tras la función |
| `*DAT_080695cc = …` | escribir una global (`gBattleMovePower = …`) | El pool guarda la dirección; se desreferencia |
| `param * 0xc + DAT_…` | `tabla[param]` con struct de 12 B | Índice × tamaño del struct + base |
| `ushort *param_1` y `param_1[0x17]` | `struct X *p` y `p->campo` en offset `0x2E` | Ghidra no conoce el struct: multiplica el índice por 2 para obtener el offset |
| comparaciones con `'%'`, `'J'`, `'"'` | constantes pequeñas (37, 74, 34) | Ghidra pinta los `u8` como `char` |
| retorno `undefined8` | `s32` | El análisis de retorno en Thumb/ARMv7 genérico se confunde |

## Pendiente de documentar
- `switch` → tablas de salto (`jump_table_evidence` de REA).
- Bucles con contador `u8` (`for (i = 0; i < N; i++)` con `i & 0xff`).
- Llamadas a punteros de función (`gMain.callback2`) y cómo seguirlas.
