---
tags: [decomp, esmeralda, funcion, combate]
creado: 2026-10-15
estado: entendida
dir_es: "0x0806957c"
dir_usa: "0x0806957c"
tamano: 2160
modo: thumb
archivo: src/pokemon.c:3106
---

# ⚔️ CalculateBaseDamage

Calcula el **daño base** de un movimiento en combate (fórmula de la Gen III), antes de
aplicar críticos, STAB, efectividad de tipos y el factor aleatorio.

| | |
|---|---|
| Dirección ES / USA | `0x0806957c` / `0x0806957c` (delta 0: no se movió) |
| Tamaño | 2160 B, Thumb |
| Fuente de referencia | `pokeemerald/src/pokemon.c:3106` |
| Obtenido con | `rea-es.sh decompile --procedure CalculateBaseDamage` |

## Firma
```c
// Ghidra
undefined8 CalculateBaseDamage(ushort *param_1, ushort *param_2, int param_3, uint param_4,
                               short param_5, byte param_6, uint param_7, uint param_8);
// pret
s32 CalculateBaseDamage(struct BattlePokemon *attacker, struct BattlePokemon *defender,
                        u32 move, u16 sideStatus, u16 powerOverride, u8 typeOverride,
                        u8 battlerIdAtk, u8 battlerIdDef);
```
| Ghidra | Real | Cómo se deduce |
|---|---|---|
| `param_1`, `param_2` | `attacker`, `defender` | Se indexan como `struct BattlePokemon` |
| `param_3` | `move` | `param_3 * 0xc + DAT_…` → tabla de 12 B = `gBattleMoves` |
| `param_5` | `powerOverride` | Si es 0 se usa `gBattleMoves[move].power` |
| `param_6` | `typeOverride` | `& 0x3f` = `DYNAMIC_TYPE_MASK` |
| `param_7`, `param_8` | `battlerIdAtk`, `battlerIdDef` | Índices de `gEnigmaBerries` (struct de 0x1c B) |
| retorno `undefined8` | `s32` | Ghidra no infiere bien el retorno (ver [[Patrones de agbcc]]) |

## Offsets de `struct BattlePokemon` que aparecen
Ghidra lo ve como `ushort *`, así que el índice ×2 = offset en bytes.

| Pseudocódigo | Offset | Campo |
|---|---|---|
| `param_1[1]` | `0x02` | `attack` |
| `param_2[2]` | `0x04` | `defense` |
| `param_1[4]` | `0x08` | `spAttack` |
| `param_2[5]` | `0x0A` | `spDefense` |
| `(char)param_1[0x10]` | `0x20` | `ability` (byte bajo) |
| `param_1[0x17]` | `0x2E` | `item` |

## Constantes traducidas
| Pseudocódigo | Constante |
|---|---|
| `0xaf` | `ITEM_ENIGMA_BERRY` (175) |
| `'%'` / `'J'` | `ABILITY_HUGE_POWER` (37) / `ABILITY_PURE_POWER` (74) → ataque ×2 |
| `* 0x6e / 100` | ×1,1 por medalla (`ShouldGetStatBadgeBoost`) |
| `'\x1d'` | `HOLD_EFFECT_CHOICE_BAND` (29) → ataque ×1,5 (`0x96`/100) |
| `'"'` | `HOLD_EFFECT_SOUL_DEW` (34), solo Latios/Latias y fuera del Frente Batalla |
| `'#'` / `'$'` | `DEEP_SEA_TOOTH` / `DEEP_SEA_SCALE` (35/36), solo Clamperl |
| `'-'` + especie `0x19` | `HOLD_EFFECT_LIGHT_BALL` (45) + Pikachu (25) |
| `'@'` + especie `0x84` | `HOLD_EFFECT_METAL_POWDER` (64) + Ditto (132) |
| bucle `< 0x11` sobre `DAT_08069770` | `sHoldEffectToType[17][2]` (objetos que potencian un tipo) |
| `param_6 < 9` | `IS_TYPE_PHYSICAL`: en Gen III **el tipo** decide físico/especial (`TYPE_MYSTERY` = 9) |

## Comparación de un fragmento
```c
// Ghidra (ES)
if (param_1[0x17] == 0xaf) {
    iVar6 = param_7 * 0x1c + DAT_08069630;
    cVar4 = *(char *)(iVar6 + 7);
    uVar7 = (uint)*(byte *)(iVar6 + 0x1a);
} else {
    cVar4 = GetItemHoldEffect(param_1[0x17]);
    uVar7 = GetItemHoldEffectParam(param_1[0x17]);
}
```
```c
// pret
if (attacker->item == ITEM_ENIGMA_BERRY) {
    attackerHoldEffect = gEnigmaBerries[battlerIdAtk].holdEffect;
    attackerHoldEffectParam = gEnigmaBerries[battlerIdAtk].holdEffectParam;
} else {
    attackerHoldEffect = GetItemHoldEffect(attacker->item);
    attackerHoldEffectParam = GetItemHoldEffectParam(attacker->item);
}
```

## Lecciones
- Los nombres portados (`GetItemHoldEffect`, `ShouldGetStatBadgeBoost`) hacen que una
  función de 2 KB se lea en minutos: **los nombres de los callees son la mitad del trabajo**.
- Ghidra pierde los tipos de struct; recuperarlos es la siguiente capa → mejora pendiente:
  importar los tipos de los headers de pret en Ghidra.
- Las constantes ASCII (`'%'`, `'J'`, `'"'`) son números pequeños que Ghidra pinta como
  `char`: tradúcelos siempre a decimal.
