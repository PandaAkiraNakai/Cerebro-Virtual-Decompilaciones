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

## Shell (torre)

> [!bug] La herramienta Bash es zsh
> `--include=*.md` sin comillas da `no matches found`; `head -c 0xc0` no acepta hex.
> Para lógica no trivial, escribe un `.sh` y córrelo con `bash`.
