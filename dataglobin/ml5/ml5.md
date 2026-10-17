# BISDX Data Documentation
Miscellaneous data from Mario & Luigi: Paper Jam. This document's format has been inspired by [Sukus' PiT documentation](https://codeberg.org/sukus/nintil/src/branch/main/nds/pit/files.md).

## Table of contents
* Generic Formats
    * GameDB Tables
    * BG4 Archives
    * MSBT Text Files
* [DB.dat](#dbdat)
    * [Item Data](#item-data)
    * [Gear Data](#gear-data)

## Pseudo-code
Throughout this document, this type of pseudo-code will be used to define structures:
```C
// Define a structure
struct structName {
    // Offset   type    name
    0x00:       u32,    number
    0x04:       u32,    number_2
}
```

## DB.dat
Stores miscellaneous data tables from the game's main campaign:
| Section | Data |
|-|-|
| 0 | [Item Data](#item-data) |
| 1 | Item Sort Order |
| 2 | Item Hash Table |
| 3 | Gear Data |
| 4 | Gear Sort Order |
| 5 | Gear Hash Table |
| 6 | Card Data |
| 7 | Card Sort Order |
| 8 | Card Hash Table |
| 9 | Monster Data |
| 10 | Monster Hash Table |
| 11 | Mario's Stats Table |
| 12 | Luigi's Stats Table |
| 13 | Paper Mario's Stats Table |

### Item Data
Section 0 of DB.dat. Array of the following structure:
```C
struct Item {
    0x00-0x17: str, Item.msbt Label -> Name (Singular)
    0x18-0x2F: str, Item.msbt Label -> Name (Plural)
    0x30-0x47: str, Item.msbt Label -> Description
    0x48-0x5F: str, Item.msbt Label -> Full Inventory Message
    0x60: u32, Sprite ID*
    0x64: u32, Price
    0x68: u16, Effect ID
    0x6A: u16, Effect Parameter
    0x6C-0x6D: bitflags, Usability Flags*
    0x6E: u16, ???
}
```
The Item's ID is defined by the prefix `1xxx` and its position in the list. For example, the first item, Mushroom, would have ID `0x1000`, and Super Mushroom `0x1001`.

Sprites are retrieved from:
* Field: `Obj/FEtc.dat/f_items_all`
* Battle: `Obj/BPCML.dat/b_items_all`
* Menu: `Obj/Language/Menu.dat/m_items_all`

Usability flags:
* `Byte 0, Bit 0`: Useable in the menu
* `Byte 0, Bit 1`: Useable in battle
* `Byte 0, Bit 2`: Useable in the Battle Ring
* `Byte 0, Bit 3`: Exclude Paper Mario as a target in battle
* `Byte 0, Bit 4`: Exclude Mario & Luigi as a target in battle
* `Byte 0, Bit 5`: Targets enemies
* `Byte 0, Bit 6`: Multi-Target
* `Byte 0, Bit 7`: Targets background enemies
* `Byte 1, Bit 0`: Is a Mushroom
* `Byte 1, Bit 1`: Is a Bean
* `Byte 1, Bit 2/3/4/5`: Usability Condition
    * `00`: No condition (Menu crash)
    * `01`: Missing HP (HP)
    * `02`: Missing BP (BP)
    * `03`: Is KO'd (Menu Crash)
    * `04`: Affected by negative status
    * `05`: Missing HP or BP (HP & BP)
    * `06`: Everyone can act (Menu Crash)
    * `07`: HP can be increased (HP)
    * `08`: BP can be increased (BP)
    * `09`: POW can be increased (POW)
    * `10`: DEF can be increased (DEF)
    * `11`: SPEED can be increased (SPEED)
    * `12`: STACHE can be increased (STACHE)
    * `13`: Background Enemy (Unused, Menu Crash)
* `Byte 1, Bit 6`: ???, Always 0
* `Byte 1, Bit 7`: ???, Always 1

### Gear Data
Array of the following structure:
```C
struct Gear {
    0x00-0x17: str, Item.msbt Label -> Name (Singular)
    0x18-0x2F: str, Item.msbt Label -> Name (Plural)
    0x30-0x47: str, Item.msbt Label -> Description
    0x48-0x5F: str, Item.msbt Label -> Full Inventory Message
    0x60: u32, Sprite ID
    0x64: u32, Price
    0x68: u16, HP
    0x6A: u16, BP
    0x6C: u16, POW
    0x6E: u16, DEF
    0x70: u16, SPEED
    0x72: u16, STACHE
    0x74: u8, Category
    0x75: u8, User
    0x76: u16, Effect ID
    0x78: u32, Effect Param 1
    0x7C: u32, Effect Param 2
}
```
The Gear's ID is defined by the prefix `3xxx` and its position in the list.