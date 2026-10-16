#!/usr/bin/env python3
"""Porta los símbolos de función de pokeemerald (USA, BPEE) a otra ROM de Esmeralda.

Para cada función del ELF de pret toma sus bytes en la ROM USA, pone comodines
en las palabras alineadas que parecen punteros absolutos (EWRAM, IWRAM, ROM,
E/S) y busca el patrón en la ROM destino. Primero busca cerca del desplazamiento
local actual y, si no aparece ahí, en toda la ROM. Solo acepta coincidencias únicas.

Salida: TSV de semillas para REA (address<TAB>function<TAB>name), con la
dirección en formato Thumb (bit 0 = 1) cuando la función es Thumb.

Uso: port_symbols.py <pokeemerald.elf> <pokeemerald.gba> <rom_destino.gba> <salida.tsv>
"""
import re
import subprocess
import sys

ROM_BASE = 0x08000000
MIN_LEN = 12          # bytes mínimos para que un patrón sea fiable
WINDOW = 0x20000      # ventana de búsqueda alrededor del desplazamiento actual
OUTLIER = 0x1000      # salto de delta que se considera coincidencia falsa
POINTER_HIGH = {0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09}


def functions(elf):
    out = subprocess.run(["arm-none-eabi-readelf", "-sW", elf],
                         check=True, capture_output=True, text=True).stdout
    seen = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 8 or parts[3] != "FUNC":
            continue
        value, size, name = int(parts[1], 16), int(parts[2]), parts[7]
        addr = value & ~1
        if size == 0 or not (ROM_BASE <= addr < ROM_BASE + 0x02000000):
            continue
        # Un mismo address puede tener alias; nos quedamos con el primero.
        seen.setdefault(addr, (addr, size, bool(value & 1), name))
    return sorted(seen.values())


def pattern(code, start):
    """Regex de los bytes con comodines en palabras que parecen punteros."""
    pieces = []
    i = 0
    while i < len(code):
        if (start + i) % 4 == 0 and i + 4 <= len(code) and code[i + 3] in POINTER_HIGH:
            pieces.append(b".{4}")
            i += 4
        elif (i % 2 == 0 and i + 4 <= len(code)
              and code[i + 1] & 0xF8 == 0xF0 and code[i + 3] & 0xF8 == 0xF8):
            # BL Thumb (par de medias palabras): el desplazamiento es relativo
            # y cambia si la función llamada se movió; se conserva el opcode.
            pieces.append(b".[\xf0-\xf7].[\xf8-\xff]")
            i += 4
        else:
            pieces.append(re.escape(code[i:i + 1]))
            i += 1
    return re.compile(b"".join(pieces), re.DOTALL)


def unique(rx, rom, lo, hi):
    matches = []
    for m in rx.finditer(rom, max(lo, 0), min(hi, len(rom))):
        matches.append(m.start())
        if len(matches) > 1:
            break
    return matches[0] if len(matches) == 1 else None


def main(elf, src_path, dst_path, out_path):
    src = open(src_path, "rb").read()
    dst = open(dst_path, "rb").read()
    funcs = functions(elf)
    delta = 0
    found = local = global_ = short = missing = outliers = 0
    rows = []
    for addr, size, thumb, name in funcs:
        off = addr - ROM_BASE
        code = src[off:off + size]
        if len(code) < MIN_LEN:
            short += 1
            continue
        rx = pattern(code, off)
        hit = unique(rx, dst, off + delta - WINDOW, off + delta + WINDOW + size)
        if hit is not None:
            local += 1
        else:
            hit = unique(rx, dst, 0, len(dst))
            if hit is None:
                missing += 1
                continue
            global_ += 1
        # El patrón debe respetar la alineación original (4 bytes por los comodines).
        if hit % 4 != off % 4:
            missing += 1
            continue
        delta = hit - off
        rows.append((off, hit, thumb, name))

    # Filtro de atípicos: el código se desplaza por tramos, así que una función
    # cuyo delta se aleja mucho del de sus dos vecinas (que coinciden entre sí)
    # es casi seguro una coincidencia falsa de una función genérica.
    keep = []
    for i, (off, hit, thumb, name) in enumerate(rows):
        if 0 < i < len(rows) - 1:
            d = hit - off
            dp = rows[i - 1][1] - rows[i - 1][0]
            dn = rows[i + 1][1] - rows[i + 1][0]
            if abs(dp - dn) < OUTLIER and abs(d - dp) >= OUTLIER:
                outliers += 1
                continue
        keep.append((ROM_BASE + hit + (1 if thumb else 0), name))
    found = len(keep)
    rows = keep

    with open(out_path, "w") as fh:
        fh.write("# Símbolos portados de pret/pokeemerald (BPEE) a la ROM destino\n")
        for a, name in sorted(rows):
            fh.write(f"0x{a:x}\tfunction\t{name}\n")
    total = len(funcs)
    print(f"funciones en el ELF: {total}")
    print(f"portadas: {found} ({100 * found / total:.1f} %) "
          f"[cerca: {local}, búsqueda global: {global_}]")
    print(f"demasiado cortas (<{MIN_LEN} B): {short}   sin coincidencia única: {missing}"
          f"   descartadas por atípicas: {outliers}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])
