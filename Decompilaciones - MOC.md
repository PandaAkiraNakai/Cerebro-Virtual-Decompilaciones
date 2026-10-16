---
tags: [decomp, moc]
creado: 2026-10-15
---

# 🧩 Decompilaciones — Mapa de contenido

Todo lo que aprendemos haciendo **ingeniería inversa y decompilación** de binarios.
Primer proyecto: [[Proyecto Esmeralda ES]] (Pokémon Esmeralda en español, GBA).

> [!abstract] Índice maestro
> Para una visión densa y enrutada (ideal para IA), empieza por [[_INDEX (IA)]].

## 🧭 Método (léelo antes de cada sesión)

1. [[Flujo de trabajo]] — de la ROM al pseudocódigo con nombres, paso a paso.
2. [[Convenciones]] — cómo nombramos notas, funciones, direcciones y estados.

## 🛠️ Herramientas

- [[REA + Ghidra]] — el motor: Ghidra headless controlado por REA (CLI y MCP).
- [[pret y agbcc]] — decomp de referencia de la comunidad y su compilador.
- [[Portar simbolos entre versiones]] — llevar nombres de una ROM a otra por bytes.

## 🕹️ Plataformas

- [[GBA - ARM7TDMI y Thumb]] — CPU, modos ARM/Thumb, convención de llamada.
- [[GBA - Mapa de memoria y cabecera]] — dónde vive cada cosa y cómo leer el header.

## 🗂️ Proyectos

- [[Proyecto Esmeralda ES]] — estado, identidad de la ROM, funciones estudiadas.
  - [[Diferencias ES vs USA]] — qué código cambió en la versión española.
  - [[CalculateBaseDamage]] — primera función analizada a fondo.
- [[Analisis del port HD-2D]] — port nativo a Linux con gráficos 2.5D estilo Octopath: radiografía del código, punteros de 64 bits, mapas → 3D, prueba de concepto y hoja de ruta.
  - [[Villa Raiz HD-2D]] — primer mapa acabado: prefabs por metatile, casas de dos niveles, árboles 3D.
  - [[Musica remasterizada]] — MIDI originales (SC-88Pro) → GM de alta calidad + PSG limpio, bucles sin clics.

## 📈 Aprendizaje y mejora continua

- [[Gotchas y errores resueltos]] — muros que ya rompimos.
- [[Patrones de agbcc]] — cómo se ve el C de 2002 en pseudocódigo de Ghidra.
- [[Bitacora de optimizaciones]] — cada mejora medida (antes → después).
- [[Recursos y enlaces]] — docs, repos, wikis.

---

> [!tip] Filosofía
> Una decompilación se hace **por capas**: identidad del binario → mapa de memoria
> → nombres (símbolos) → tipos (structs) → lógica. Cada capa que añadimos hace que
> la siguiente sea más fácil. Medimos el avance con números (funciones con
> nombre, funciones entendidas) y anotamos qué técnica nos hizo avanzar.
