# BISDX Data Documentation
Miscellaneous data from Mario & Luigi: Bowser's Inside Story + Bowser Jr.'s Journey. This document's format has been inspired by [Sukus' PiT documentation](https://codeberg.org/sukus/nintil/src/branch/main/nds/pit/files.md).

## Table of contents
* Generic Formats
    * GameDB Tables
    * BG4 Archives
    * MSBT Text Files
* [DB.dat](#dbdat)
    * [Item Data](#item-data)
        * [Item Effects](#item-effects)
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
| 6 | Badge Data |
| 7 | Badge Sort Order |
| 8 | Badge Hash Table |
| 9 | Gear Effect Strings |
| 10 | Badge Combos |
| 11 | Mario's Stats Table |
| 12 | Luigi's Stats Table |
| 13 | Bowser's Stats Table |
| 14 | Monster Data |
| 15 | Monster Hash Table |

### Item Data
Section 0 of DB.dat. Array of the following structure:
```C
struct Item {
    0x00-0x17: str, Item.msbt Label -> Name (Singular)
    0x18-0x2F: str, Item.msbt Label -> Name (Plural)
    0x30-0x47: str, Item.msbt Label -> Description
    0x48-0x5F: str, Item.msbt Label -> Full Inventory Message
    0x60: u32, Sprite ID*
    0x64: u16, Price
    0x66: u16, Effect ID*
    0x68: s16, Effect Parameter
    0x6A-0x6B: bitflags, Usability Flags*
}
```
The Item's ID is defined by the prefix `1xxx` and its position in the list.

Sprites are retrieved from:
* Field: `Obj/FEtc.dat/f_items_all`
* Battle: `Obj/BPCML.dat/b_items_all`
* Menu: `Obj/Language/Menu.dat/m_items_all`

Usability flags:
* `Byte 0, Bit 0/1/2/3`: The first 4 bits are used to define the usability condition type.
The behavior might be slightly difference when used from the menu or in a battle.
    * `00`: No special condition
    * `01`: Missing HP (HP)
    * `02`: Missing BP (BP)
    * `03`: Is KO'd
    * `04`: Affected by negative status
    * `05`: Missing HP or BP (HP & BP)
    * `06`: HP can be increased (HP)
    * `07`: BP can be increased (BP)
    * `08`: POW can be increased (POW)
    * `09`: DEF can be increased (DEF)
    * `10`: SPEED can be increased (SPEED)
    * `11`: STACHE/HORN can be increased (STACHE/HORN)
    * `12`: Unused
    * `13`: All party members can act
* `Byte 0, Bit 4`: ???
* `Byte 0, Bit 5`: Item can be used in menu
* `Byte 0, Bit 6`: Mushroom Pocket in Inventory Menu (useable in battle)
* `Byte 0, Bit 7`: Is Mushroom?
* `Byte 1, Bit 0`: Multi-Target (Bros only)
* `Byte 1, Bit 1`: Exclude Bowser
* `Byte 1, Bit 2`: Exclude Mario & Luigi

### Gear Data
Array of the following structure:
```C
struct Gear {
    0x00-0x17: str, Item.msbt Label -> Name (Singular)
    0x18-0x2F: str, Item.msbt Label -> Name (Plural)
    0x30-0x47: str, Item.msbt Label -> Description
    0x48-0x5F: str, Item.msbt Label -> Full Inventory Message
    0x60: u32, Sprite ID
    0x64: u16, Price
    0x66: u16, Effect ID
    0x68: u8, Effect Parameter 1
    0x69: u8, Effect Parameter 2
    0x6A: u8, Gear Category
    0x6B: u8, User (0=Bros | 1=Bowser)
    0x6C: s16, HP
    0x6E: s16, BP
    0x70: s16, POW
    0x72: s16, DEF
    0x74: s16, SPEED
    0x76: s16, STACHE/HORN
}
```
The Gear's ID is defined by the prefix `2xxx` and its position in the list. For example, the first entry, Thin Wear, would have ID `0x2000`, and Picnic Wear `0x2001`.