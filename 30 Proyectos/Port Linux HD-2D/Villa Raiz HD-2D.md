---
tags: [decomp, esmeralda, port, hd-2d, render, prefabs]
creado: 2026-10-15
actualizado: 2026-10-15
estado: hecho
---

# 🏡 Villa Raíz en HD-2D (prefabs por metatile)

Primer mapa "acabado" de la prueba de concepto ([[Analisis del port HD-2D]]). Repo local
`$HDD/GitHub/pokeemerald-hd2d`, commit `e1fa371`. Se ejecuta con `make run`.

## Qué se hizo y por qué

| Pieza | Problema con la heurística automática | Solución |
|---|---|---|
| Casas | Cortadas por columnas, sin paredes laterales | Componente conexo de metatiles de edificio → volumen con paredes generadas |
| Tejado | Arte ¾ pegado plano sobre un techo | Casa de **dos niveles** deducida de los píxeles (ver abajo) |
| Laboratorio | Chimenea pintada en el techo | Techo plano + pretil + **cilindro**; `roof_replace` borra la pintada |
| Árboles | Muros de copa plana | Tronco cónico + 18 racimos de hojas pixel art con la paleta original |
| Flores | Calcomanía plana | Hojas como mata + cada flor (componente conexo no verde) sobre un tallo |
| Pasto | Rejilla regular de puntos de GBA | Textura procedural repetible de 64×64 con el tile original como paleta |

### Cortes del arte de la casa (`cuts`)
El tejado (3 filas) y la fachada (2 filas) apilados dan 80 px. Leyendo los colores de
las filas de píxeles de `0x219` y `0x232` salen las franjas:

| px | franja | en 3D |
|---|---|---|
| 0–36 | tejado superior | dos aguas, alero 0,34 |
| 36–40 | moldura gris/azul | cara del alero + cantos laterales |
| 40–45 | muro blanco | muro alto retranqueado |
| 45–52 | tejas | faldón inclinado en los 4 lados |
| 52–56 | borde del faldón | canto vertical |
| 56–80 | planta baja | caja de 1,5 de alto |

> [!tip] Lección
> El arte GBA es una proyección frontal: para "levantarlo" hay que **entender qué
> representa cada banda de píxeles**, no solo qué metatile es. Una tabla por tileset
> con estos cortes basta para todas las casas iguales de Hoenn.

## Técnicas de render que marcan la diferencia
- **Muestreo nítido** (`sharp()` en GLSL): filtrado lineal + `fwidth` → bloques de
  píxel perfectos con bordes antialiasados; sin parpadeo al mover la cámara.
- **Sombras con alpha-test** en el shadow map: la sombra sigue la silueta del pixel art.
- **Normales desde la luminancia** (Sobel) + canal de brillo: vidrio detectado por
  color (azul dominante) y tejas con brillo medio.
- **AO horneada** en el suelo subdividido 4×4 (distancia a edificios, troncos y NPC).
- **Tramado de oclusión en pantalla**: se descartan con Bayer 4×4 los fragmentos más
  cercanos que el jugador dentro de una elipse sobre su figura y **por encima de sus
  pies** (si no, se trama también el techo que queda debajo en pantalla).
- **Perspectiva aérea** + suelo lejano: sin él se veía el color del cielo al fondo de
  la conexión norte.
- Paleta de hojas un 12-20 % más oscura que la GBA: con sol + bloom la original queda
  lima chillón.

## Personajes (commit siguiente)
- El GBA solo tiene 2 poses por casilla (`sAnim_GoSouth`: paso 8 frames + quieto 8).
  Se generan intermedios moviendo **el torso 1 px** (filas 0-20 de 32) sin tocar los
  pies: estirado en el paso de pie, comprimido en el contacto → 4 poses por casilla.
- Correr: `running.png` con el reparto 5:3 de `sAnim_RunSouth`.
- NPC con `MOVEMENT_TYPE_WANDER_AROUND`: esperan 32/64/96/128 frames y caminan dentro
  de `movement_range_x/y`.
- Los pies van a `y + 0.88` (borde sur de la casilla, como el anclaje del sprite GBA):
  así las flores de su propia casilla quedan detrás y no "cortan" las piernas.
- **Lección**: el tramado de oclusión no debe aplicarse a personajes; si no, un NPC
  delante del jugador se ve cortado en vez de taparlo.

## Pendiente para este mapa
- Interiores (casa del jugador, laboratorio) y animación de puertas.
- Flores animadas (el metatile tiene animación de tileset).
