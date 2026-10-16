---
tags: [decomp, moc]
creado: 2026-10-15
---

# 🧩 Decompilaciones — Mapa de contenido

Todo lo que aprendemos haciendo **ingeniería inversa y decompilación** de binarios.
Primer proyecto: Pokémon Esmeralda en español (GBA). Desde 2026-10-15 continúa en su
propio vault, ver [[Pokemon Esmeralda - movido a remake-2.5d]].

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

- [[Pokemon Esmeralda - movido a remake-2.5d]] — la decompilación de la ROM española y el
  port HD-2D viven ahora en el vault **remake-2.5d**.

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
