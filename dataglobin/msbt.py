import io
import json
import os
from pathlib import Path
import re
import struct
import traceback
from typing import override
from mnllib.dt import SpecialCharacter
import pymsbmnl
import dataglobin.constants as Constants
import dataglobin.data as Data
from dataglobin.constants import GameID, Language

class PostPJLMSAdapter(pymsbmnl.LMSAdapter):
    def __init__(self) -> None:
        super().__init__()
        self.set_little_endian()

    @override
    def read_char(self, stream: pymsbmnl.BinaryMemoryIO) -> str:
        char = super().read_char(stream)
        try:
            return f"[{SpecialCharacter(char).name}]"
        except ValueError:
            return char

    @override
    def read_tag(self, stream: pymsbmnl.BinaryMemoryIO) -> str:
        group_id, tag_id, args_size = stream.read_u16(), stream.read_u16(), stream.read_u16()
        match group_id, tag_id:
            case 0x0000, 0x0000:
                base_text_len, ruby_text_len = stream.read_u16(), stream.read_u16()
                ruby_text = stream.read(ruby_text_len).decode(self.charset)
                base_text = stream.read(base_text_len).decode(self.charset)
                return f"[Ruby {base_text};{ruby_text}]"
            case 0x0000, 0x0001:
                return f"[Font {stream.read(args_size).hex().upper()}]"
            case 0x0000, 0x0002:
                return f"[Size {stream.read_u16()}%]"
            case 0x0000, 0x0003:
                color = stream.read(args_size)
                if len(color) == 4 and color[3] == 0xFF:
                    color = color[:3]
                return f"[Color #{color.hex().upper()}]"
            case 0x0000, 0x0004:
                return "[Next]"
            case 0x0002, 0x0001:
                return "[Wait]"
            case _:
                return f"[{group_id:04X}:{tag_id:04X}:{stream.read(args_size).hex(' ').upper()}]"

    @override
    def read_closing_tag(self, stream: pymsbmnl.BinaryMemoryIO) -> str:
        return f"[/{stream.read_u16():04X}:{stream.read_u16():04X}]"

    @override
    def write_tag(self, stream: pymsbmnl.BinaryMemoryIO, tag: str) -> None:
        if tag.startswith("/"):
            inner_tag = tag[1:]
            self.write_chars(stream, "\u000f")
            if ":" in inner_tag:
                group_id, tag_id = inner_tag.split(":", 1)
                stream.write_u16(int(group_id, 16))
                stream.write_u16(int(tag_id, 16))
                return
            raise ValueError(f"unknown closing tag '{tag}'")
        try:
            self.write_chars(stream, SpecialCharacter[tag.upper()])
            return
        except KeyError:
            pass
        self.write_chars(stream, "\u000e")
        if ":" in tag:
            sections = tag.split(":")
            stream.write_u16(int(sections[0], 16))
            stream.write_u16(int(sections[1], 16))
            arg_data = bytes.fromhex(sections[2]) if len(sections) >= 3 else b""
            stream.write_u16(len(arg_data))
            stream.write(arg_data)
            return
        tag_type, *raw_args = tag.split(" ")
        pos_args, kw_args = [], {}
        for arg in raw_args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                key = key.casefold()
                if key in kw_args:
                    raise ValueError(f"keyword argument repeated: {key}")
                kw_args[key] = value
            else:
                pos_args.append(arg)
        match tag_type.casefold():
            case "ruby":
                stream.write_u16(0x0000)
                stream.write_u16(0x0000)
                base_text, ruby_text = " ".join(pos_args).split(";", 1)
                encoded_base, encoded_ruby = base_text.encode(self.charset), ruby_text.encode(self.charset)
                stream.write_u16(4 + len(encoded_ruby))
                stream.write_u16(len(encoded_base))
                stream.write_u16(len(encoded_ruby))
                stream.write(encoded_ruby)
                stream.write(encoded_base)
            case "font":
                stream.write_u16(0x0000)
                stream.write_u16(0x0001)
                font = bytes.fromhex(" ".join(pos_args))
                stream.write_u16(len(font))
                stream.write(font)
            case "size":
                stream.write_u16(0x0000)
                stream.write_u16(0x0002)
                stream.write_u16(2)
                stream.write_u16(int(pos_args[0].rstrip("%"), 0))
            case "color" | "colour":
                stream.write_u16(0x0000)
                stream.write_u16(0x0003)
                color = bytes.fromhex(" ".join(pos_args).lstrip("#"))
                if len(color) == 3:
                    color += b"\xff"
                elif len(color) != 4:
                    raise ValueError("color must be RRGGBB or RRGGBBAA")
                stream.write_u16(len(color))
                stream.write(color)
            case "next":
                stream.write_u16(0x0000)
                stream.write_u16(0x0004)
                stream.write_u16(0)
            case "wait":
                stream.write_u16(0x0002)
                stream.write_u16(0x0001)
                stream.write_u16(0)
            case _:
                raise ValueError(f"unknown tag '{tag_type}'")

    @property
    @override
    def supports_attributes(self) -> bool:
        return True

    @property
    @override
    def attributes_size(self) -> int:
        return 4

    @override
    def parse_attributes(self, stream, root_offset, root_size):
        try:
            return {"width": stream.read_u16(), "height": stream.read_u16()}
        except pymsbmnl.EOFException:
            return {"width": 0, "height": 0}

    @override
    def write_attributes(self, stream, attributes):
        stream.write_u16(attributes.get("width", 0))
        stream.write_u16(attributes.get("height", 0))

    @property
    @override
    def supports_styles(self) -> bool:
        return True

    @override
    def create_default_style(self) -> int:
        return 0

def remove_tags(text: str) -> str:
    return re.sub(r"\[/?[^\]]*\]", "", text)

# Dumb patch until it's fully supported by mnllib
def fix_msbt_data(raw_data: bytes) -> bytes:
    if len(raw_data) < 0x16 or raw_data[:8] != b"MsgStdBn":
        raise ValueError("Invalid MSBT header")
    bom = raw_data[0x08:0x0A]
    if bom == b"\xfe\xff":
        endian = ">"
    elif bom == b"\xff\xfe":
        endian = "<"
    else:
        raise ValueError(f"Invalid MSBT BOM: {bom.hex().upper()}")
    declared_size = struct.unpack_from(f"{endian}I", raw_data, 0x12)[0]
    actual_size = len(raw_data)
    if declared_size == actual_size:
        return raw_data
    if declared_size > actual_size:
        missing = declared_size - actual_size
        print(f"Size mismatch: declared {declared_size}, actual {actual_size}, adding {missing} zero bytes")
        return raw_data + b"\x00" * missing
    raise ValueError(f"MSBT declares size {declared_size}, but actual file is larger at {actual_size} bytes")

def parse_msbt_bytes(raw_data: bytes, filename: str) -> dict:
    raw_data = fix_msbt_data(raw_data)
    document = pymsbmnl.msbt_from_buffer(PostPJLMSAdapter, raw_data)
    return {"filename": filename, "data": [{"key": msg.label, "value": remove_tags(msg.text)} for msg in document.messages]}

def parse_msbt(path: str) -> dict:
    with open(path, "rb") as f:
        raw_data = f.read()
    return parse_msbt_bytes(raw_data, os.path.splitext(os.path.basename(path))[0])

def decompress_bg4(data: bytes) -> bytes:
    if len(data) < 8:
        return data
    footer = data[-8:]
    buffer_top_and_bottom, _ = struct.unpack("<ii", footer)
    footer_len = (buffer_top_and_bottom >> 24) & 0xFF
    if footer_len == 0 or (buffer_top_and_bottom & 0xFFFFFF) == 0:
        return data
    try:
        compressed_len = len(data) - footer_len
        compressed = data[:compressed_len][::-1]
        in_stream = io.BytesIO(compressed)
        out_stream = io.BytesIO()
        circular = bytearray(0x1002)
        pos = 0
        end_position = (buffer_top_and_bottom & 0xFFFFFF) - footer_len
        code_block = in_stream.read(1)[0]
        code_pos = 8
        while in_stream.tell() < end_position:
            if code_pos == 0:
                code_block = in_stream.read(1)[0]
                code_pos = 8
            flag = (code_block >> (code_pos - 1)) & 1
            code_pos -= 1
            if flag == 0:
                b = in_stream.read(1)
                if not b:
                    break
                out_stream.write(b)
                circular[pos % len(circular)] = b[0]
                pos += 1
            else:
                pair = in_stream.read(2)
                if len(pair) < 2:
                    break
                b1, b2 = pair
                length = (b1 >> 4) + 3
                displacement = ((b1 & 0xF) << 8 | b2) + 3
                start = pos - displacement
                for _ in range(length):
                    val = circular[start % len(circular)]
                    out_stream.write(bytes([val]))
                    circular[pos % len(circular)] = val
                    start += 1
                    pos += 1
        while in_stream.tell() < len(compressed):
            out_stream.write(in_stream.read(1))
        return out_stream.getvalue()[::-1]
    except Exception:
        return data

def load_bg4(path: str) -> dict[str, bytes]:
    files = {}
    with open(path, "rb") as f:
        magic = f.read(4)
        if magic != b"BG4\x00":
            raise ValueError(f"{path} has invalid BG4 magic")
        version = struct.unpack("<H", f.read(2))[0]
        if version not in {0x0105, 0x0104, 0x0305}:
            raise ValueError(f"{path} has unsupported version {version:#04x}")
        file_count = struct.unpack("<H", f.read(2))[0]
        f.read(4)
        f.read(2)
        f.read(2)
        entries = []
        for _ in range(file_count):
            file_offset = struct.unpack("<I", f.read(4))[0] & 0x7FFFFFFF
            file_size = struct.unpack("<I", f.read(4))[0] & 0x7FFFFFFF
            f.read(4)
            name_offset = struct.unpack("<H", f.read(2))[0]
            entries.append((file_offset, file_size, name_offset))
        names_origin = f.tell()
        names = []
        for _, _, name_offset in entries:
            f.seek(names_origin + name_offset)
            name_bytes = bytearray()
            while (c := f.read(1)) != b"\0":
                name_bytes.append(c[0])
            names.append(name_bytes.decode("ascii"))
        for i, (file_offset, file_size, _) in enumerate(entries):
            name = names[i]
            if not name or name.lower() == "(invalid)":
                continue
            f.seek(file_offset)
            raw = f.read(file_size)
            files[name] = decompress_bg4(raw)
    return files

def parse_archive_file(path: str, filename: str) -> dict:
    archive = load_bg4(path)
    for name, data in archive.items():
        if name.lower() == filename.lower():
            return parse_msbt_bytes(data, filename)
    raise FileNotFoundError(f"'{filename}' was not found inside {path}")

def load_msbt(version: GameID, romfs_directory: Path):
    msg_folder = os.path.join(romfs_directory, "Msg")
    try:
        if not os.path.isdir(msg_folder):
            raise FileNotFoundError(f"Msg folder does not exist:\n{msg_folder}")
        result = {}
        if version in (GameID.ML3R, GameID.ML1R, GameID.ML5):
            for language in Data.LANGUAGES_ML5:
                folder = os.path.join(msg_folder, language)
                if not os.path.isdir(folder):
                    continue
                language_enum = Language(language)
                language_data = {}
                item_path = os.path.join(folder, "Item.msbt")
                if os.path.isfile(item_path):
                    print(f"Parsing: {item_path}")
                    try:
                        language_data["Item.msbt"] = parse_msbt(item_path)
                    except Exception:
                        print(f"Error parsing {item_path}:\n" f"{traceback.format_exc()}")
                bmsg_path = os.path.join(folder, "BMsg.dat")
                if os.path.isfile(bmsg_path):
                    print(f"Parsing: {bmsg_path} -> b_sys")
                    try:
                        language_data["b_sys"] = parse_archive_file(bmsg_path, "b_sys")
                    except Exception:
                        print(f"Error parsing {bmsg_path}:\n"f"{traceback.format_exc()}")

                result[language_enum] = language_data
        return result
    except Exception:
        print("Fatal error:\n", traceback.format_exc())
        return {}