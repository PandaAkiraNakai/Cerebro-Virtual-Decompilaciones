---
tags: [decomp, gba, arm, thumb, plataforma]
creado: 2026-10-15
---

# 🧠 GBA — ARM7TDMI y Thumb

## CPU
- **ARM7TDMI** a 16,78 MHz, arquitectura **ARMv4T**. Sin caché, sin división por
  hardware (de ahí las llamadas a `__divsi3`, ver [[Patrones de agbcc]]).
- Dos juegos de instrucciones:
  - **ARM**: 32 bits por instrucción. Se usa en el arranque, en las interrupciones y
    en rutinas críticas copiadas a IWRAM.
  - **Thumb**: 16 bits por instrucción. Casi todo el juego está en Thumb porque el bus
    de la ROM es de 16 bits y así va más rápido.

## Cambiar de modo (interworking)
- `BX Rn`: salta a la dirección de `Rn`; si su **bit 0 = 1**, entra en Thumb.
- Por eso los punteros a funciones Thumb son **impares** (`AgbMain` = `0x080003a5`).
- En Ghidra el modo es el registro de contexto **`TMode`**. Si se decodifica Thumb como
  ARM, sale basura → [[Gotchas y errores resueltos]].

## Llamadas en Thumb
- `BL` son **dos medias palabras** (`F000+hi`, `F800+lo`) con un desplazamiento relativo
  de ±4 MiB. Si la función destino se mueve, cambian los bytes del `BL`.
- Constantes y direcciones de 32 bits van en **literal pools** tras la función y se
  cargan con `ldr rX, [pc, #imm]` → Ghidra las muestra como `DAT_08xxxxxx`.

## Convención de llamada (la que genera agbcc)
| Registro | Uso |
|---|---|
| `r0–r3` | 4 primeros argumentos; `r0` (y `r1`) retorno |
| `r4–r7` (+`r8–r11`) | Preservados por la función llamada |
| `sp` (`r13`) | Pila; argumentos 5.º en adelante |
| `lr` (`r14`) | Dirección de retorno |
- Los argumentos `u8`/`u16` llegan en registros de 32 bits y se **re-enmascaran** dentro de
  la función (`param & 0xff`).

Ver: [[GBA - Mapa de memoria y cabecera]].
