# BISDX Data Documentation
Miscellaneous data from Mario & Luigi: Superstar Saga + Bowser's Minions. This document's format has been inspired by [Sukus' PiT documentation](https://codeberg.org/sukus/nintil/src/branch/main/nds/pit/files.md).

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
| 3 | Wear Data |
| 4 | Wear Sort Order |
| 5 | Wear Hash Table |
| 6 | Badge Data |
| 7 | Badge Sort Order |
| 8 | Badge Hash Table |
| 9 | Accessory Data |
| 10 | Accessory Sort Order |
| 11 | Accessory Hash Table |
| 12 | Key Item Data |
| 13 | Key Item Sort Order |
| 14 | Key Item Hash Table |
| 15 | Bean Data |
| 16 | Bean Sort Order |
| 17 | Bean Hash Table |
| 18 | Wear Effects Strings |
| 19 | Badge Effects Strings |
| 20 | Accessory Effects Strings |
| 21 | Mario's Stats Table |
| 22 | Luigi's Stats Table |
| 23 | Monster Data |
| 24 | Monster Hash Table |

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
    0x6B: u8, ??? Only has value on mushroom items
    0x6B: bitflags, Usability Flags*
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
    * `12`: Any stat can be increased
    * `13`: All party members can act
* `Byte 0, Bit 4`: ???
* `Byte 0, Bit 5`: Item can be used in menu
* `Byte 0, Bit 6`: Mushroom Pocket in Inventory Menu (useable in battle)
* `Byte 0, Bit 7`: Multi-Target

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
    0x68: s16, Effect Parameter
    0x6A: s16, HP
    0x6B: s16, BP
    0x6C: s16, POW
    0x6D: s16, DEF
    0x6E: s16, SPEED
    0x6F: s16, STACHE/HORN
    0x70-0x71: bitflags, User
    0x72-0x73: ???
}
```
The Wear's ID is defined by the prefix `2xxx` and its position in the list.

### Badge Data
Array of the following structure:
```C
struct Badge {
    0x00-0x17: str, Item.msbt Label -> Name (Singular)
    0x18-0x2F: str, Item.msbt Label -> Name (Plural)
    0x30-0x47: str, Item.msbt Label -> Description
    0x48-0x5F: str, Item.msbt Label -> Full Inventory Message
    0x60: u32, Sprite ID
    0x64: u16, Price
    0x66: u16, Effect ID
    0x68: s16, Effect Parameter
    0x6A: s16, HP
    0x6B: s16, BP
    0x6C: s16, POW
    0x6D: s16, DEF
    0x6E: s16, SPEED
    0x6F: s16, STACHE/HORN
}
```
The Badge's ID is defined by the prefix `3xxx` and its position in the list.

### Accessory Data
Array of the following structure:
```C
struct Accessory {
    0x00-0x17: str, Item.msbt Label -> Name (Singular)
    0x18-0x2F: str, Item.msbt Label -> Name (Plural)
    0x30-0x47: str, Item.msbt Label -> Description
    0x48-0x5F: str, Item.msbt Label -> Full Inventory Message
    0x60: u32, Sprite ID
    0x64: u16, Effect ID
    0x66: s16, Effect Parameter
}
```
The Accesory's ID is defined by the prefix `4xxx` and its position in the list.

### Key Item Data
Array of the following structure:
```C
struct Accessory {
    0x00-0x17: str, Item.msbt Label -> Name (Singular)
    0x18-0x2F: str, Item.msbt Label -> Name (Plural)
    0x30-0x47: str, Item.msbt Label -> Description
    0x48-0x5F: str, Item.msbt Label -> Full Inventory Message
    0x60: u32, Sprite ID
}
```
The Key Item's ID is defined by the prefix `5xxx` and its position in the list.

### Bean Data
Array of the following structure:
```C
struct Accessory {
    0x00-0x17: str, Item.msbt Label -> Name (Singular)
    0x18-0x2F: str, Item.msbt Label -> Name (Plural)
    0x30-0x47: str, Item.msbt Label -> Description
    0x48-0x5F: str, Item.msbt Label -> Full Inventory Message
    0x60: u32, Sprite ID
}
```
The Bean's ID is defined by the prefix `6xxx` and its position in the list.
