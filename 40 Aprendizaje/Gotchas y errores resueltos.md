---
tags: [decomp, troubleshooting, errores]
creado: 2026-10-15
---

# 🧯 Gotchas y errores resueltos

Bitácora de muros que rompimos. Si algo falla, busca aquí primero.

## Herramientas

> [!bug] REA abre la ROM pero no descompila nada
> Sin Ghidra/IDA/rizin, REA solo ofrece inventario. `binary_session` muestra
> `analysis_provider_binding: null`. Solución: instalar Ghidra 12.1.x
> (`pacman -S ghidra`) y pasar `GHIDRA_INSTALL_DIR=/opt/ghidra` → [[REA + Ghidra]].

> [!bug] Las semillas de REA decodifican Thumb como ARM
> `ReaGhidraApplySeeds.java` llamaba a `disassemble()` sin fijar `TMode`, así que una
> función Thumb salía como basura ARM. Solución: parche local, dirección impar ⇒
> `TMode=1`. Resultado: 12 901 creadas, 0 fallidas.

> [!bug] Cada llamada a la CLI de REA tarda ~3,5 min
> El `--snapshot` de la CLI no guarda la base de datos de Ghidra; reanaliza siempre.
> Agrupa preguntas o usa la sesión MCP persistente.

> [!bug] `pacman -S ghidra` "se colgó" más de 10 min
> Eran ~740 MiB de descarga del mirror de CachyOS; terminó bien. Lánzalo en segundo
> plano.

## Análisis

> [!bug] Saltos de delta gigantes al comparar versiones
> Indexar las funciones del ELF **por nombre** mezcla funciones `static` homónimas
> (`Cmd_nop`, `MainCB`, `VBlankCB`…: 95 nombres repetidos). Indexa **por dirección**.
> Parecían coincidencias falsas del porte y no lo eran: el filtro de atípicos descartó 0.

> [!bug] "rev 01" no es la revisión
> En la cabecera GBA, `0xB0` = fabricante (`01` = Nintendo). La versión está en `0xBC`
> (`0x00` en nuestra ROM) → [[GBA - Mapa de memoria y cabecera]].

> [!bug] El arranque no está en `0x080000c0`
> Esmeralda salta a `0x08000204` (`ea00007f`). Verifícalo siempre desensamblando, no de memoria.

## Ports nativos con render propio

> [!bug] Los colores de un PNG de la decomp no coinciden con los del juego
> Los PNG amplían los 5 bits de la paleta como `c·255/31`; el juego (y el port) como
> `(c << 3) | (c >> 2)`. Difieren en 1 en varios valores. Si identificas recursos por hash
> de sus píxeles, convierte a 5 bits y vuelve a ampliar como el juego antes de hashear.

> [!tip] Sustituir recursos sin tocar el juego: hash del fotograma decodificado
> El port decodifica cada sprite desde la VRAM emulada. El render calcula un hash (FNV-1a
> 64) de ese RGBA y, si hay una versión nueva con ese hash, la usa; si no, usa la de siempre.
> Prueba también el hash del reflejo (las vistas de lado suelen ser el mismo fotograma
> invertido). Un modo de volcado (variable de entorno) guarda los fotogramas sin sustituto,
> así sabes cuáles faltan.

> [!tip] Texto en alta resolución: registrar glifos y validar contra la imagen
> Engancha la función que copia cada glifo a la ventana (posición, máscara de la letra,
> clases de píxel) y las que rellenan, borran o desplazan ventanas. En cada fotograma,
> valida cada glifo contra la imagen 1x (cada clase de píxel con un solo color). Si cuadra,
> borra la letra 1x y dibuja encima la de una fuente SDF generada desde la original, con los
> colores leídos de la pantalla (así respeta fundidos y paletas). Una entrada sobrante no
> estorba: simplemente no valida.

> [!bug] El registro va un fotograma por delante de lo que se ve
> Lo que el juego prepara en un fotograma llega a la VRAM en el VBlank (DMA). Si capturas la
> imagen antes del VBlank y los datos del juego (sprites, glifos) en el mismo momento, no
> casan: sprites "revueltos" al girar y destellos de la letra vieja al cambiar de página.
> Captura todo **después** del VBlank.

> [!bug] En el modo de prueba el render solo dibuja en las capturas
> Si avanzas el reloj del render 1/60 s por llamada, las animaciones casi no avanzan entre
> capturas. Pásale `dt = capturas_cada / 60`.

> [!tip] "Bilineal nítido" para pixel art ampliado
> Mide desde la costura entre texels: `c = floor(p + 0.5)` y
> `p = c + clamp((p − c) / fwidth(p), −0.5, 0.5)`. Con `floor(p)` (el índice del texel) se
> muestrea en el borde y se mezclan los vecinos: queda borroso.

> [!tip] Hora real en un juego con RTC sin romper los contadores de días
> En los Pokémon de GBA, `gLocalTime = RTC − localTimeOffset` (el desfase se guarda al poner el
> reloj al empezar). Para que la hora del día sea la del PC, ignora horas, minutos y segundos
> del desfase pero **conserva los días**: así bayas y eventos diarios siguen contando igual.
> Ponlo detrás de una bandera del port para que las pruebas deterministas no cambien.

> [!bug] Llamar cada fotograma a una función de la plataforma que imprime
> En pokeemerald-native `DBGPRINTF` está siempre activo (`PORTABLE`) y `Platform_GetDateTime`
> imprime una línea por llamada. Para leer la hora en cada fotograma, añade una función que
> actualice el reloj interno sin el registro.

> [!tip] El mapa de Hoenn está en un fondo afín de 8 bpp
> `graphics/pokenav/region_map/map.png` son tiles de 8 bpp y `map.bin` un mapa afín de
> **1 byte por casilla** (64×64). Si lo lees como mapa de texto (u16 con flips y paleta) sale
> basura. Los colores: la paleta del propio PNG (el juego la carga en `BG_PLTT_ID(7)`).

> [!bug] Dibujar el mismo fotograma de la GBA más de una vez avanza el juego
> En el emulador de pantalla del port, cada línea ejecuta la interrupción de HBlank y los DMA
> de HBlank (efectos por línea: entradas de combate, ondas). Si dibujas varias capas por
> fotograma, guarda y restaura los registros de E/S y el estado de los DMA alrededor de cada
> dibujo extra; si no, el efecto avanza varias líneas por fotograma.

> [!tip] Remasterizar una escena fija: cámara calibrada con la pantalla original
> Fija la cámara 3D y deriva todo de ella: cada píxel de la pantalla original es un rayo, su
> corte con el suelo da la posición en el mundo y el tamaño de un píxel a esa profundidad. Así
> sprites, plataformas y efectos se colocan donde los pone el juego, y su interfaz y sus
> animaciones 2D cuadran encima. Para que una forma pintada (elipse) coincida con su volumen
> 3D, proyecta su contorno punto a punto: con perspectiva ya no es la misma forma en el mundo.

> [!tip] Fundidos y tintes de paleta en un render moderno
> Compara la paleta fundida con la original: con los dos colores más distintos sacas la
> cantidad y el color del fundido. Si fondos y sprites se funden igual es un fundido de
> pantalla (aplícalo a la escena entera); si no, es un tinte de un sprite (destello, golpe).

> [!bug] Sprites de combate de Blanco/Negro (2): no salen al decodificar lineal
> En `a/0/0/4` (20 archivos por especie, LZ11) la imagen fija de 96×96 va en **cuatro
> bloques de OAM** seguidos (64×64, 32×64, 64×32, 32×32), cada uno en baldosas de 8×8 con
> mapeo 1D. Decodificada como una sola imagen lineal o en baldosas sale troceada.

> [!bug] Sprites de combate de HeartGold/SoulSilver: datos cifrados
> Los RGCN de `a/0/0/4` van cifrados con un LCG (`×0x41C64E6D + 0x6073`) sembrado con la
> primera palabra, hacia adelante. Las especies solo hembra traen vacío el archivo de macho.

## Shell (torre)

> [!bug] La herramienta Bash es zsh
> `--include=*.md` sin comillas da `no matches found`; `head -c 0xc0` no acepta hex.
> Para lógica no trivial, escribe un `.sh` y córrelo con `bash`.
