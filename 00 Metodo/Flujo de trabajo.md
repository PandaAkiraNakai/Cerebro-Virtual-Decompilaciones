---
tags: [decomp, metodo]
creado: 2026-10-15
---

# 🔁 Flujo de trabajo

El orden que seguimos con cualquier binario nuevo. Cada paso deja una nota o un
número en el vault; si un paso nos enseña algo, va a [[Gotchas y errores resueltos]]
o a [[Bitacora de optimizaciones]].

## 1. Identidad del binario
- `sha1sum`/`sha256sum` y cabecera (en GBA: título, código de juego y versión, ver
  [[GBA - Mapa de memoria y cabecera]]).
- Anotar los hashes en la nota del proyecto: sin hash no se puede comparar nada después.

## 2. ¿Existe ya una referencia?
- Buscar una decomp de la comunidad (pret, zeldaret, etc.) u otra versión con símbolos.
- Si existe, compilarla **hasta que coincida** con su hash: así sabemos que los
  símbolos y el `.map` son fiables ([[pret y agbcc]]).

## 3. Portar nombres
- Llevar los símbolos de la referencia al binario objetivo
  ([[Portar simbolos entre versiones]]). Medir el % portado y anotarlo.

## 4. Analizar con REA + Ghidra
- Formato, arquitectura y dirección de carga correctos (GBA: `raw-binary`, `arm`,
  `0x08000000`), semillas Thumb y heap suficiente ([[REA + Ghidra]]).
- Revisar en las `limitations` del resultado el informe de semillas: creadas / fallidas.

## 5. Estudiar una función
1. Copiar [[Plantilla - Funcion]] a `30 Proyectos/<proyecto>/Funciones/`.
2. Sacar el pseudocódigo y, si hay referencia, el C original.
3. Renombrar mentalmente `param_N` → argumentos reales; offsets → campos de struct;
   `DAT_xxxxxxxx` → variables globales o tablas; constantes → `#define`.
4. Anotar los patrones del compilador que aparezcan ([[Patrones de agbcc]]).

## 6. Cerrar la sesión
- Actualizar el **estado** de la nota del proyecto (números).
- Si algo se hizo más rápido o mejor que la vez anterior → [[Bitacora de optimizaciones]].
