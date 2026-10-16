# 🧩 Cerebro Virtual — Decompilaciones

Vault de Obsidian con todo lo que voy aprendiendo haciendo **ingeniería inversa y decompilación** de binarios: herramientas, método, conocimiento de cada plataforma, cada función entendida y cada error resuelto. La idea es **aprender, mejorar y optimizar** con cada proyecto: lo que funciona se vuelve método; lo que falla, un gotcha; y cada mejora queda medida.

> Primer proyecto: **Pokémon Esmeralda (ES)** para GBA, analizado con **REA + Ghidra** y comparado con la decomp de [pret/pokeemerald](https://github.com/pret/pokeemerald). Sus notas de proyecto pasaron a un vault propio dedicado a remakes en 2.5D; aquí queda el método general.

<!-- profile-excerpt -->
Vault Obsidian de **ingeniería inversa y decompilación** — método por capas (identidad → mapa de memoria → símbolos → tipos → lógica), **REA + Ghidra** headless, plataforma **GBA** (ARM7TDMI, Thumb, mapa de memoria), patrones del compilador **agbcc** y una **bitácora de optimizaciones** medida. Primer caso de estudio: **Pokémon Esmeralda ES**, con el **81 %** de las funciones nombradas portando los símbolos de pret por coincidencia de bytes.
<!-- /profile-excerpt -->

## 🧭 Por dónde empezar

- **Vista humana / navegación** → [`Decompilaciones - MOC.md`](Decompilaciones%20-%20MOC.md)
- **Entrada densa para IA** → [`_INDEX (IA).md`](_INDEX%20(IA).md)

## 📚 Contenido

| Carpeta | Contenido |
|---|---|
| `00 Metodo/` | Flujo de trabajo y convenciones (estados de una función, direcciones, confianza) |
| `10 Herramientas/` | REA + Ghidra · pret y agbcc · portar símbolos entre versiones · `scripts/` |
| `20 Plataformas/` | GBA: ARM7TDMI y Thumb · mapa de memoria y cabecera |
| `30 Proyectos/` | Notas puente a los proyectos (Esmeralda vive en su propio vault) |
| `40 Aprendizaje/` | Gotchas y errores resueltos · patrones de agbcc · bitácora de optimizaciones |
| `90 Plantillas/` | Plantillas de función, proyecto y lección |

## 🛠️ Scripts

- `port_symbols.py` — porta los nombres de función de un ELF de referencia a otra versión de la ROM, con comodines en *literal pools* y en `BL` Thumb.
- `rea-es.sh` — envoltorio de la CLI de REA con Ghidra para una ROM GBA (`raw-binary`, `0x08000000`, semillas Thumb).
- `rea-thumb-seeds.patch` — parche para REA: las semillas con dirección impar se decodifican en modo Thumb.

> [!warning] Sin binarios con copyright
> Aquí no hay ROMs, volcados ni bases de análisis: solo notas, extractos cortos de pseudocódigo con fines de estudio y scripts propios. Para reproducir el análisis necesitas tu propio volcado de la ROM.

## 🗂️ Cómo usarlo

Abre la carpeta como vault en [Obsidian](https://obsidian.md) para aprovechar los enlaces `[[wiki]]` y el grafo. También se lee bien como Markdown plano en GitHub.

---

📓 Parte de mi colección de *cerebros virtuales* en Obsidian.
