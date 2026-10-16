---
tags: [decomp, herramientas, pret, gba]
creado: 2026-10-15
---

# 📚 pret y agbcc

**pret** es la comunidad que decompiló los Pokémon clásicos a C que compila **byte a
byte idéntico** a la ROM original (*matching decomp*). Es nuestra referencia de
"respuesta correcta" para comparar con lo que saca Ghidra.

## Montaje (2026-10-15)
```sh
cd $HDD/GitHub
git clone --depth 1 https://github.com/pret/pokeemerald.git
git clone --depth 1 https://github.com/pret/agbcc.git
sudo pacman -S arm-none-eabi-binutils           # as, ld, objcopy, readelf
cd agbcc && ./build.sh && ./install.sh ../pokeemerald
cd ../pokeemerald && make -j$(nproc)
sha1sum -c rom.sha1                             # "La suma coincide"
```
- Genera `pokeemerald.gba` (USA, BPEE, sha1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`).
- Archivos clave tras compilar:
  - `pokeemerald.elf` → símbolos con tamaño (`arm-none-eabi-readelf -sW`), bit 0 = Thumb.
  - `pokeemerald.map` → dirección de cada símbolo y de qué `.o` viene.
  - `build/emerald/src/*.o` → para ver el ensamblador de una sola función.

## agbcc
Es el GCC antiguo (~2.95) que usó Game Freak, parcheado por pret. Necesario para el
*matching*; un GCC moderno genera otro código. Sus manías se ven en el pseudocódigo
→ [[Patrones de agbcc]].

## Ver el ensamblador de una función
```sh
arm-none-eabi-objdump -d -M force-thumb build/emerald/src/pokemon.o | less
```

## Límite
Solo compila la versión **USA**. Para la ROM española usamos los nombres portados
([[Portar simbolos entre versiones]]) y Ghidra ([[REA + Ghidra]]).
