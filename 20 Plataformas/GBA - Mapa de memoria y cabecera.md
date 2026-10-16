---
tags: [decomp, gba, memoria, plataforma]
creado: 2026-10-15
---

# 🗺️ GBA — Mapa de memoria y cabecera

## Mapa de memoria
| Región | Dirección | Tamaño | Notas |
|---|---|---|---|
| BIOS | `0x00000000` | 16 KiB | SWI (llamadas al sistema) |
| EWRAM | `0x02000000` | 256 KiB | RAM lenta; `gSaveBlock*`, `gBattle*`… |
| IWRAM | `0x03000000` | 32 KiB | RAM rápida; pila, `gMain`, código ARM copiado |
| E/S | `0x04000000` | ~1 KiB | Registros de vídeo, sonido, DMA, timers, teclas |
| Paletas | `0x05000000` | 1 KiB | |
| VRAM | `0x06000000` | 96 KiB | Tiles y mapas |
| OAM | `0x07000000` | 1 KiB | Sprites |
| ROM | `0x08000000` | hasta 32 MiB | Espejos con otros *wait states* en `0x0A…`, `0x0C…` |
| Guardado | `0x0E000000` | | Esmeralda usa Flash de 128 KiB |

> [!tip] Leer un `DAT_` en Ghidra
> El byte alto del valor indica la región: `0x02…` variable en EWRAM, `0x03…` en
> IWRAM, `0x04…` registro de hardware, `0x08…` tabla o función en ROM.

## Cabecera de la ROM (`0x08000000`–`0x080000BF`)
| Offset | Campo | Esmeralda ES | Esmeralda USA |
|---|---|---|---|
| `0x00` | Salto ARM al código de arranque | `b 0x08000204` (`ea00007f`) | igual |
| `0x04` | Logo de Nintendo (156 B) | | |
| `0xA0` | Título (12 B) | `POKEMON EMER` | `POKEMON EMER` |
| `0xAC` | Código de juego (4 B) | `BPES` | `BPEE` |
| `0xB0` | Código de fabricante | `01` (Nintendo) | `01` |
| `0xBC` | **Versión** | `0x00` | `0x00` |
| `0xBD` | Checksum complementario | `0x64` | `0x72` |

En el código de juego: `B` = juego normal, `PE` = Esmeralda, último carácter = región
(`E` inglés/USA, `S` España, `D` Alemania, `F` Francia, `I` Italia, `J` Japón).

> [!note] Arranque en `0x08000204`, no en `0x080000c0`
> El estándar deja el código justo tras la cabecera (`0xC0`), pero Esmeralda guarda ahí
> más metadatos de Game Freak y su `crt0` empieza en `0x204`. Verificado con
> `arm-none-eabi-objdump -D -b binary -marm --adjust-vma=0x08000000`.

> [!bug] No confundir fabricante con versión
> El `01` en `0xB0` es el **fabricante**. La revisión está en `0xBC`.
