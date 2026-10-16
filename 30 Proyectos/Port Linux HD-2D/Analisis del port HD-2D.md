---
tags: [decomp, esmeralda, port, linux, hd-2d, analisis]
creado: 2026-10-15
actualizado: 2026-10-15
estado: analisis
---

# 🎮 Port de Esmeralda a Linux con gráficos HD-2D

Objetivo: ejecutable **nativo x86_64 para Linux** compilado desde la decomp de pret
(sin emulación), con el overworld y los combates presentados en **2.5D estilo Octopath
Traveler** (mundo 3D de pixel art, sprites como billboards, luces dinámicas,
profundidad de campo, bloom).

> [!info] Base del análisis
> `pret/pokeemerald` @ `731ad5b` en `$HDD/GitHub/pokeemerald` (compila idéntica a BPEE,
> ver [[Proyecto Esmeralda ES]]). Las cifras salen de grep/parseo del árbol (observado).
> Las estimaciones de esfuerzo son **inferidas**.

## 1. Radiografía del código

| Métrica | Valor |
|---|---|
| C en `src/` | 310 archivos, **421 436 líneas** |
| Cabeceras | 335 archivos, 45 433 líneas |
| Asm de código que queda | 4 `.s` (2 736 líneas): `m4a_1.s` (mezclador de audio), `crt0.s`, `libgcnmultiboot.s`, `rom_header.s` |
| `NONMATCHING` | **0**: todo el juego está en C |
| Datos en asm (`data/*.s`, `.inc`) | 166 066 líneas (scripts, mapas, tablas de sonido) |
| Mapas / layouts / grupos | 518 / 441 / 34 |
| Celdas de mapa en total | 324 599 |
| Tilesets / metatiles | 70 (74 combinaciones usadas) / **16 698** |
| PNG / canciones MIDI | 3 850 / 530 |
| `make modern` (gcc) | existe: el C ya compila con gcc moderno |

Archivos más grandes: `battle_script_commands.c` (10 326), `pokemon_storage_system.c`
(10 059), `event_object_movement.c` (8 950), `slot_machine.c`, `pokemon.c`, `tv.c`.

## 2. Superficie de hardware GBA que hay que sustituir

| Área | Tamaño | Qué hacer en el port |
|---|---|---|
| Registros de vídeo vía `SetGpuReg` & cía. | 1 754 llamadas en 104 archivos | Shim fácil: `gpu_regs.c` ya los bufferiza |
| `REG_*` directos | 585 (la mayoría serie/link e `REG_IME`) | Stubs; el link se apaga |
| Macros `VRAM`/`OAM`/`PLTT`/`BG_*_ADDR` | ~527 usos, todos en `include/gba/defines.h` | Redefinir como buffers del host |
| DMA (`Dma*`, `dma3_manager`) | ~200 usos en 50 archivos | `memcpy`/`memset` |
| BIOS | LZ77 165, RL 22, CpuSet 14, ObjAffineSet 6, BgAffineSet 3, Sqrt/Div/ArcTan2 | Reimplementar en C (~400 líneas) |
| Interrupciones | VBlank (211 setters), HBlank (16 reales en 6 archivos), VCount 1 | Bucle de frame del host |
| Efectos por scanline | `scanline_effect.c` usado en 19 archivos (58 con algún efecto) | El PPU tiene que aplicar cambios **línea a línea** |
| Audio m4a | `m4a.c` 1 781 + `m4a_1.s` 1 916 | Mezclador en C (agbplay, LGPL) |
| Guardado flash | `agb_flash*.c` ~600 | Archivo `.sav` |
| RTC | `siirtc.c` + `rtc.c` ~800 | Reloj del sistema |
| Link cable / inalámbrico / e-Reader / multiboot | ~12 000 líneas | Stubs (fase 1); red real opcional después |

## 3. El problema serio: punteros de 32 bits

En x86_64 un puntero mide 8 bytes y el juego asume 4 en todas partes:

- **Bytecode con punteros**: 6 658 `.4byte` en `data/` (scripts de evento, de combate,
  de animación, de IA de concursos) + 5 841 en mapas generados. Se leen con
  `ScriptReadWord` (59 usos) y `T1/T2_READ_PTR` (319 usos).
- **`ScriptContext.data` es `u32[4]`** y guarda punteros (`include/script.h:19`).
- **Punteros partidos en `s16 data[]`** de tareas y sprites: `StoreSpriteCallbackInData6`
  (144), `SetWordTaskArg` (15), 38 `(u32)fn >> 16` escritos a mano.
- **Structs superpuestos a `task->data`**: 33 casos; `list_menu.c:18`
  `STATIC_ASSERT(sizeof(struct ListMenu) <= 32)` **falla** en 64 bits.
- `Set/GetWindowAttribute` pasa punteros como `u32`.

Opciones (de menos a más invasiva):
1. **Compilar en 32 bits (`-m32`)**: lo hacía el port original de NTx86. Funciona, pero
   las distros están quitando las multilib (pokeemerald-native avisa que en Ubuntu 25+
   no va).
2. **Base + offset de 32 bits** para los scripts (`.4byte label - ScriptBase`) y
   **tablas de índices** para punteros a funciones y plantillas. Lo menos invasivo en 64.
3. Convertir los scripts a arrays de C con punteros nativos (lo más trabajo).

**Cómo lo resolvió `pokeemerald-native` (comprobado en su código):** una variante de la
opción 3 sin reescribir los scripts. Los datos en asm se ensamblan **para el host** con GNU
`as`, y los macros emiten el puntero con el ancho nativo (`asm/macros/bit_width.inc`):
`ptrvalue` → `.quad` en 64 bits / `.int` en 32, `ptr_align` → `.balign 8`, y en C
`T1_READ_PTR` lee 64 bits bajo `-DPORTABLE` (`include/global.h:149`). Compila con
`-Werror=pointer-to-int-cast -Werror=int-to-pointer-cast`, así que los casts peligrosos
ya están todos corregidos.

## 4. Overworld → 3D: lo que dan los datos

### Formato
- Celda de `map.bin` (u16): metatile `0x03FF`, colisión `0x0C00`, **elevación** `0xF000`
  (`include/global.fieldmap.h:7`).
- Metatile = 8 entradas de tilemap: 4 de la **capa inferior** y 4 de la **superior**.
  `metatile_attributes.bin`: comportamiento (bits 0-7) y tipo de capa (bits 12-15:
  NORMAL / COVERED / SPLIT).
- Capas de BG en el overworld (`overworld.c:266`): BG1 = capa superior (tapa sprites),
  BG2 = media, BG3 = inferior.

### Hallazgo clave: la elevación NO es altura
Comprobado en el código y en los datos:
- 0 = transición (154 705 de sus 166 635 celdas son muros), 1 = agua, 3 = suelo normal,
  15 = multinivel. Villa Raíz entera es elevación 3 + 0; las montañas de Ruta 111/112 y
  el Monte Cenizo también.
- Solo **67 de 441 layouts** usan elevaciones 4-9 (puentes, Arborada, Algaria, cuevas).
- Sirve para colisión (`IsElevationMismatchAt`, `event_object_movement.c:7673`) y
  para la prioridad de dibujo (`sElevationToPriority`, `:7695`).
- Los saltos (`MB_JUMP_*`) son un arco del sprite; la altura nunca se guarda.

**Conclusión**: la geometría 3D no se puede sacar directamente de la elevación. El arte
GBA es una **proyección frontal ¾**: fachadas y acantilados están dibujados de frente,
así que hay que "levantarlos".

### Prueba de concepto (hecha y verificada)
Repo local `$HDD/GitHub/pokeemerald-hd2d` (los recursos se extraen en `build/`, nunca
al repo):
- `tools/export_map.py`: layout + tilesets → atlas de metatiles (capa inferior y
  superior) + rejilla JSON. Comprobado renderizando la vista cenital de Villa Raíz
  idéntica al juego.
- `tools/build_scene.py`: heurística automática. Celdas bloqueadas agrupadas por
  columna; los 2 metatiles del sur del tramo (la fachada) se levantan en vertical y el
  resto queda como techo plano. Agua hundida, saltos como escalón.
- `viewer/main.c` (SDL3 + OpenGL 3.3 core): sombras direccionales con alpha-test
  (siguen la silueta del pixel art), luz puntual cálida, bloom, DOF + tilt-shift,
  ACES, viñeta; jugador billboard 16×32 que camina respetando la colisión real.

Resultado en Villa Raíz, Petalia y Ruta 104:
- ✅ Casas, vallas, carteles y bordes quedan como volúmenes creíbles sin tocar nada.
- ✅ El aspecto HD-2D (sombras, DOF, bloom) sale con muy poco código.
- ❌ Los **bosques** densos se convierten en muros/mesetas planas: el árbol necesita
  modelo (tronco + copa o billboards cruzados).
- ❌ Objetos planos bloqueados (macizos, alfombras de entrada) se levantan cuando no
  deberían.

### Propuesta de pipeline de mapas
1. **Tabla de prefabs por metatile** (la pieza central): para cada uno de los 16 698
   metatiles, una entrada `{suelo | fachada | techo | árbol | agua | prop, altura, malla
   opcional}`. Se autora **por tileset, no por mapa**: un árbol de `general` vale para
   todo Hoenn. La heurística de la prueba rellena el 70-80 % y se corrige a mano.
2. Alturas de terreno: flood-fill de regiones transitables separadas por acantilados
   (tramos bloqueados entre dos zonas transitables) y por saltos; puentes según
   `BRIDGE_*` (LOW/MED/HIGH = 12/28/44 px).
3. Capa superior NORMAL con contenido (30 025 celdas): copas y tejados como volumen.
4. Luces: tabla autorada + máscaras emisivas por paleta (ventanas, lava, antorchas).
5. **La lógica no cambia**: la rejilla, la colisión y la elevación originales siguen
   mandando; el 3D es solo una vista.

### Efectos del overworld que pasan a posproceso
| Efecto GBA | Truco original | En HD-2D |
|---|---|---|
| Oscuridad de cueva / Destello | ventana WIN0H por scanline | luz puntual real con radio |
| Niebla, tormenta de arena, ceniza | sprites con alpha | niebla volumétrica / partículas |
| Sequía, sol | blend de aclarado | color grading + bloom |
| Tinte del clima | mapas de color de paleta | LUT de color |
| Reflejos en agua | sprite volteado | reflejo planar / SSR |
| Fundidos | paleta | posproceso |

## 5. Combates

- Separación lógica/presentación **bastante limpia**: la lógica emite 57 comandos de
  controlador (`include/battle_controllers.h:184`) a 9 controladores. Hay fugas
  (`battle_main.c` toca 25 `SetGpuReg`, `Cmd_drawlvlupbox`, `Cmd_trainerslidein`).
- Animaciones: 356 de movimientos, 48 opcodes, **451 `AnimTask_*` en C** (~45k líneas).
  Dependencias: afín OAM 1 123 líneas, blending 227, scanline 92 (8 familias: siniestro,
  dragón, fantasma, tierra, psíquico, agua…), ventanas 54. **Ninguna usa BG afín.**
- 10 entornos de combate; 419 sprites frontales (64×64, 2 frames) y 418 traseros.

Propuesta: mantener intactos la máquina de estados y los intérpretes de scripts;
cambiar los controladores por un presentador 3D (escenario por entorno, Pokémon y
entrenadores como billboards, afín OAM → transformación del billboard, blending →
alpha de material). Las 8 familias de scanline se reescriben como shaders. Las barras
de vida, el cuadro de texto y los menús quedan como capa 2D.

## 6. Menús, texto y audio

- UI: todo sobre BG de tiles 8×8; 88 pantallas con callback propio (equipo, ficha,
  mochila, Pokédex, PC, Pokénav, concursos…). **Se renderizan con un PPU por software a
  240×160 y se componen escalados encima del 3D**; luego se puede cambiar la fuente por
  una HD enganchando `RenderText`.
- Texto: codificación propia (`charmap.txt`), la resuelve `preproc`. Sirve tal cual.
- Audio: 530 MIDI → mid2agb, 182 voicegroups, 544 WAV (388 gritos), mezcla a
  13 379 Hz. Opción: agbplay (LGPL-3.0, ya embebido en el port de Minish Cap) o el m4a en
  C de pokeemerald-multiplatform; mezclar a 48 kHz.

## 7. Trabajo previo (no partir de cero)

| Proyecto | Qué aporta | Estado (verificado 2026-10-15) |
|---|---|---|
| [fuddlesworth/pokeemerald-native](https://github.com/fuddlesworth/pokeemerald-native) | Port SDL2 Linux/Win/macOS **en 64 bits**, sale de NTx86. Capa de plataforma de solo 3 416 líneas (`src/platform/`: PPU software `gba_easy_draw.c` 909, `sdl2.c` 844, bios, dma, cgb_audio) | Activo (último push 2026-09-27), sin licencia declarada. **Compilado en la torre** (`make linux`, gcc 16, sin errores) → `pokeemerald64` ELF x86-64 de 31 MB que arranca, lee el guardado y el RTC |
| [gradenGnostic/pokeemerald-multiplatform](https://github.com/gradenGnostic/pokeemerald-multiplatform) | `src/platform/` (bios, dma, cgb_audio, PPU), m4a en C, **renderer voxel 2.5D experimental** | Activo (2026-08), licencia NOASSERTION |
| [999sian/tmc](https://github.com/999sian/tmc) (Minish Cap) | Mejor referencia de arquitectura: SDL3, PPU vendorizado, SDL_GPU, agbplay, ROM del usuario validada por SHA-1 | GPL-3.0 |
| [mstan/EmeraldRecomp](https://raw.githubusercontent.com/mstan/EmeraldRecomp/HEAD/README.md) | Recompilación estática del binario (otro enfoque) | v0.0.1 |
| *Pokémon Gamma Emerald* (fan, UE5) | Remake HD-2D desde cero, no usa la decomp | Early Access 2026-08 |

Referencia técnica HD-2D: [pipeline HD-2D en DX12](https://dev.to/gaurav_de/creating-an-hd-2d-rendering-pipeline-on-dx12-205k)
(G-buffer diferido, normal maps en sprites, sombras alpha-test, contact shadows, bokeh).

## 8. Arquitectura recomendada

```
┌──────────── lógica original (C de pret, sin tocar salvo 64 bits) ────────────┐
│ overworld · scripts · combate · menús · Pokémon · guardado                   │
└──────┬───────────────────────────────┬───────────────────────────────┬──────┘
       │ registros/VRAM/OAM            │ estado del mundo              │ m4a
┌──────▼──────┐               ┌────────▼─────────┐              ┌──────▼──────┐
│ PPU software│ 240×160       │ Presentador HD-2D│ cámara,      │ mezclador C │
│ (menús, UI, │──── capa 2D ─▶│ mapa 3D, sprites │ objetos,     │ 48 kHz      │
│  fallback)  │               │ billboard, luces │ clima        └─────────────┘
└─────────────┘               └────────┬─────────┘
                              SDL3 + OpenGL 4.x / SDL_GPU (Vulkan)
```

Principio: **el PPU por software dibuja todo** desde el día 1 (el juego es jugable
aunque el 3D no esté), y el presentador HD-2D va **sustituyendo** capas: primero el
overworld (BG1-3 + sprites de objetos), después el combate. Si una escena no tiene
versión 3D (intro, Rayquaza, minijuegos), se ve la 2D escalada.

Stack: C17, SDL3 (ventana, input, audio), OpenGL 4.6 al principio (la torre tiene
RX 6700 XT con Mesa 26) y SDL_GPU/Vulkan después si hace falta.

## 9. Hoja de ruta

| Fase | Entregable | Esfuerzo (inferido, 1 persona) |
|---|---|---|
| 0 ✅ | Prueba de concepto del diorama (este análisis) | hecho |
| 1 | Base nativa x86_64 jugable en 2D: fork de pokeemerald-native (ya compila y arranca aquí), migrar a SDL3 y separar el PPU en un módulo | 1-2 semanas |
| 2 | Hooks de estado: exportar cámara, objetos, mapa y clima del overworld al presentador | 2-3 semanas |
| 3 | Overworld HD-2D: prefabs por metatile para los tilesets de Villa Raíz → Petalia, NPCs como billboards, transiciones, puertas animadas | 2-3 meses |
| 4 | Resto de Hoenn: 74 combinaciones de tilesets, cuevas con luz, agua, puentes, clima | 4-6 meses |
| 5 | Combate HD-2D: 10 escenarios, billboards, traducir efectos de animación | 3-6 meses |
| 6 | Pulido: fuente HD, ultrapanorámico, mandos, opciones gráficas | continuo |

## 10. Legal

- No distribuir recursos ni binarios con recursos: el usuario aporta su ROM y el
  primer arranque construye la caché (como tmc y EmeraldRecomp). El repo de la prueba ya
  sigue esa regla (`.gitignore` de `build/`, `*.png`, `*.rgba`).
- Nintendo tumbó el port de SM64 (2020), Link's Awakening DX y cientos de fangames de
  Pokémon. Recomendación: mantenerlo **privado** mientras sea un proyecto de
  aprendizaje.

## Siguiente paso sugerido
Fase 1 → 2: hacer fork de `pokeemerald-native` (clonado en `$HDD/GitHub/pokeemerald-native`),
estudiar `gba_easy_draw.c` y añadir el primer hook: exportar en cada frame la posición de
la cámara (`gTotalCameraPixelOffset*`), el mapa actual y la lista de objetos al visor de
la prueba de concepto, para ver el overworld real moviéndose en 3D.

Relacionado: [[Proyecto Esmeralda ES]] · [[pret y agbcc]] · [[GBA - Mapa de memoria y cabecera]]
