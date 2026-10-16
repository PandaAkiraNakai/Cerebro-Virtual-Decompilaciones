---
tags: [decomp, esmeralda, localizacion, analisis]
creado: 2026-10-15
---

# 🌍 Diferencias de código ES vs USA

Al portar símbolos ([[Portar simbolos entre versiones]]), el **delta** (dirección ES −
dirección USA) es constante en tramos largos. Donde el delta **salta**, el código ES
entre esas dos funciones tiene otro tamaño: ahí está lo que Game Freak cambió para la
versión española. Las funciones que no se pudieron portar en ese hueco son las
candidatas a estar modificadas.

> [!info] Tipo de evidencia
> Los deltas son **observados** (salen del script). Que el cambio se deba a la
> localización es **inferido** por los nombres de las funciones; falta comprobarlo
> leyendo cada una.

## Tramos principales (≥ 40 funciones con el mismo delta)
| Rango USA | Delta | Funciones | Desde … hasta |
|---|---|---|---|
| `0x080003a4`–`0x0806f01c` | `0` | ~1 900 | `AgbMain` … `HandleSetPokedexFlag` |
| `0x0806f0b0`–`0x0807fd64` | `−0x4` | 343 | `GetTrainerNameFromId` … |
| `0x080841e4`–`0x080bae5c` | `+0x14` | 2 187 | `PlayTimeCounter_Reset` … |
| `0x080c0620`–`0x080c4630` | `−0x23c` | 112 | `GetPokedexCategoryName` … |
| `0x080f9984`–`0x0813391c` | `−0x3e8` | 1 797 | `CompareMonSize` … `Cmd_if_flash_fired` |
| `0x082ded70`–`0x082e7de8` | `+0x778c` | 277 | `GameCubeMultiBoot_Hash` … `__unpack_d` |

El combate (`CalculateBaseDamage`, scripts de batalla) está en el tramo de delta 0:
la lógica es idéntica y ni siquiera se movió.

## Puntos donde cambia el tamaño del código (candidatos a función localizada)
| Cambio | Hueco (funciones sin portar) | Hipótesis |
|---|---|---|
| `+0x18` | `PrintBlendingResults`, `PrintMadePokeblockString` | Textos de la Licuadora de bayas |
| `+0x14` | `FrameType_DrawChoices`, `ButtonMode_*` | Menú de Opciones |
| `−0x264` | `PrintMonInfo`, `PrintMonHeight`, `PrintMonWeight` | **Pokédex en sistema métrico** (m/kg en vez de ft/lb) |
| `−0x170` | `DrawCardBackStats` | Ficha de entrenador |
| `−0x10` | `LoadContestResultsTitleBarTilemaps` | Gráficos con texto de concursos |
| `−0x34` | `FormatMonSizeRecord` | Récord de tamaño en cm en vez de pulgadas |
| `+0x18` | `BufferBattleTowerElevatorFloors` | Formato del piso del ascensor |
| `+0x12c` / `−0xbc` | `BufferStringBattle`, `BattleStringExpandPlaceholders`… | Gramática de los mensajes de combate (artículos, género) |
| `+0xb0` | (entre `FillFactoryTentTrainerParty` y `FrontierSpeechToString`) | Frases del Frente Batalla |
| `−0x158` | `LoadTheEndScreen`, `GetLetterMapTile`, `DrawTheEnd`… | Pantalla "FIN" de los créditos |
| `−0x20` | `PrintAllBerryData`, `PrintBerrySize`… | Ficha de bayas (tamaño en cm) |
| `+0x14` | `AddItemQuantityWindow`, `PrintItemQuantity` | Ventana de cantidad en tiendas |
| `+0x48` | `MailboxMenu_AddWindow` | Menú del buzón |

> [!warning] Saltos gigantes = nombres repetidos, no cambios
> En el primer análisis aparecían saltos de ±0x53990, ±0xd0250… en `Cmd_nop`,
> `MainCB`, `VBlankCB`, `SpriteCB_Player`. Eran **funciones `static` con el mismo
> nombre** en distintos archivos, mezcladas al indexar por nombre. Ver
> [[Gotchas y errores resueltos]].

## Siguiente estudio sugerido
`PrintMonHeight` / `PrintMonWeight`: comparar la versión USA (pies/libras) con la ES
(metros/kilos). Es un caso perfecto de "misma función, distinto código".
