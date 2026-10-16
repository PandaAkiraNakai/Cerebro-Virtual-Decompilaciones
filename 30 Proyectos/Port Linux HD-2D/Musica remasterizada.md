---
tags: [decomp, esmeralda, port, audio, m4a, mp2k, midi]
creado: 2026-10-15
actualizado: 2026-10-15
estado: en pruebas
---

# 🎵 Música y efectos remasterizados desde los MIDI de pret

Objetivo: sonido moderno (48 kHz, sin el ruido de 8 bits ni los 13 379 Hz del mezclador
GBA) **sin cambiar la composición ni los timbres característicos**. Código en
`tools/remaster_music.py` del repo de la prueba ([[Villa Raiz HD-2D]]).

## Hallazgos (observados en la decomp)
- Los samples se llaman `sc88pro_*`, `sd90_*`: Game Freak compuso con un **Roland
  SC-88Pro** (módulo GS). Los MIDI de `sound/songs/midi/` son casi General MIDI.
- Pero el número de programa pasa por el **voicegroup** de cada canción (`-G` en
  `midi.cfg`): en `littleroot` el 0 es la batería, el 1 el piano (keysplit) y del 4 al 7
  cuadradas PSG. Hay que traducir programa → instrumento real, no usar GM a ciegas.
- `mid2agb` (`tools/mid2agb/agb.cpp`): CC1 MOD, CC7 VOL (×`-V`), CC10 PAN, **CC20 BENDR**,
  CC21 LFOS, CC22 MODT, CC24 TUNE, CC26 LFODL. **El CC11 se ignora**.
- Bucles: metaeventos de marcador `[` y `]` (en Villa Raíz, ticks 36 y 2340).
- Ruido PSG: `MidiKeyToCgbFreq` usa `gNoiseTable[key-21]` → registro NR43
  (reloj = 524288 / r / 2^(s+1), LFSR de 15 o 7 bits).
- `se_wall_hit` es una cuadrada con **sweep de hardware** (NR10 = 106 = 0x6A: baja cada
  47 ms, shift 2): de ahí su "tump" descendente.

## Pipeline
1. Partes sampleadas → MIDI GM → FluidSynth con *GeneralUser GS* (modo XG para batería
   en cualquier canal con CC0 = 127).
2. Voces PSG → síntesis propia a 48 kHz: cuadradas con polyBLEP (sin aliasing), duty,
   sweep, envolvente CGB escalonada (suavizada 2 ms), pitch bend en el tiempo, LFO;
   paso bajo de 7 kHz y paneo al 80 %.
3. Reverb por convolución (sala corta para `se_*`), limitador suave a −1 dBFS.

## Bucle sin clics (lección)
| Intento | Salto en el empalme | Problema |
|---|---|---|
| Cortar en `]` y sumar la cola al inicio | 0,31 | El audio del inicio no es la continuación |
| Intro + 2 vueltas, bucle en la 2.a | 0,30 | El final de la 2.a llevaba "notes off"; el de la 1.a, ataques adelantados |
| Intro + **3** vueltas, cortar al empezar la 3.a | 0,052 | Diferencias de cola de reverb |
| + fundido de 10 ms hacia el final de la 1.a | **0,0121** | Igual a la continuación natural (0,0121) |

## Alternativas investigadas
- `ipatix/agbplay` (LGPL-3.0): renderiza el motor MP2K original con remuestreo y reverb
  limpios y exporta stems por pista; lee ROMs.
- `huderlem/poryaaaa` (MIT): carga directamente voicegroups y samples de pokeemerald.
- `Thysbelon/gba-mus-ripper` (MIT): MIDI + SF2 desde la ROM.
- Legal: no distribuir audio ni bancos con samples de Nintendo; generar en local.

## Pendiente
- Validar a oído el balance PSG/sampleado (`PSG_GAIN`) y la reverb.
- Modo "original HQ": los samples de la GBA con interpolación limpia.
- Gritos (WAV de 8 bits a 13 kHz): remuestreo de calidad o superresolución (AudioSR).
