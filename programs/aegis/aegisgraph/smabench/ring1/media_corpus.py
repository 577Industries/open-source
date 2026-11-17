"""Media corpus generator (Ring 1).

Emits *small, valid* image samples — WebP, JPEG, PNG, GIF — for
harness-validity testing. These are explicitly NOT crash-inducing
inputs. Their purpose is to prove that ReproChain's libwebp harness
(and equivalent JPEG/PNG/GIF harnesses) consume valid input without
false positives.

Crash-triggering bytes are NEVER stored under this directory; they
live under `reprochain/corpora-private/` and are excluded from the
public sanitized export by the safety scanner.

Encoding strategy:

- If PIL is available we render solid-colored 32x32 images via the
  standard Pillow encoders. This is the default — Pillow is a declared
  dependency (`pyproject.toml`).
- If PIL is unavailable we fall back to byte-stable constants, one per
  format (a 1x1 PNG, a 1x1 GIF, a 1x1 JPEG, a 1x1 WebP), so a degraded
  environment still gets a valid item in every format: four items at
  most, whatever `count` asks for. The metadata flags
  `encoding="raw_minimal"` in that case.

Either path is byte-deterministic given (count, seed). The RNG is used
only for color choice — the geometry is fixed.
"""

from __future__ import annotations

import argparse
import io
import random
import struct
import zlib
from pathlib import Path
from typing import Iterator

from ._common import CorpusItem, write_corpus

NAME = "media-corpus"
DEFAULT_COUNT = 16
DEFAULT_SEED = 42


def _try_import_pil():
    try:
        from PIL import Image  # type: ignore[import-untyped]

        return Image
    except Exception:
        return None


def _palette(rng: random.Random) -> tuple[int, int, int]:
    """Pick a deterministic RGB triplet."""

    return (rng.randrange(0, 256), rng.randrange(0, 256), rng.randrange(0, 256))


def _pil_solid_color_png(image_module, color: tuple[int, int, int]) -> bytes:
    img = image_module.new("RGB", (32, 32), color=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def _pil_solid_color_jpeg(image_module, color: tuple[int, int, int]) -> bytes:
    img = image_module.new("RGB", (32, 32), color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85, optimize=True)
    return buf.getvalue()


def _pil_solid_color_gif(image_module, color: tuple[int, int, int]) -> bytes:
    img = image_module.new("P", (32, 32))
    palette = list(color) * 256
    img.putpalette(palette[: 256 * 3])
    buf = io.BytesIO()
    img.save(buf, format="GIF")
    return buf.getvalue()


def _pil_solid_color_webp(image_module, color: tuple[int, int, int]) -> bytes:
    """Try lossless WebP first; if libwebp isn't compiled into Pillow,
    fall back to the lossy encoder."""

    img = image_module.new("RGB", (32, 32), color=color)
    buf = io.BytesIO()
    try:
        img.save(buf, format="WEBP", lossless=True, quality=100, method=6)
    except Exception:
        buf.seek(0)
        buf.truncate(0)
        img.save(buf, format="WEBP", quality=85)
    return buf.getvalue()


# Constant 1x1 fallbacks. Each is a real file structure that decodes to
# a single white pixel; `tests/test_smabench_ring1_real_corpora.py`
# decodes all four.
_RAW_MIN_COLOR = (255, 255, 255)


def _raw_min_png() -> bytes:
    # 1x1, 8-bit RGB, single white pixel.
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)

    def chunk(t: bytes, d: bytes) -> bytes:
        crc = zlib.crc32(t + d) & 0xFFFFFFFF
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", crc)

    raw = b"\x00\xFF\xFF\xFF"  # one filter byte + 3 RGB bytes
    return signature + chunk(b"IHDR", ihdr_data) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def _raw_min_gif() -> bytes:
    # GIF89a, 1x1, single-color
    return (
        b"GIF89a"
        b"\x01\x00\x01\x00\x80\x00\x00"  # 1x1, GCT flag, 1 color
        b"\xFF\xFF\xFF\x00\x00\x00"  # palette
        b"\x21\xF9\x04\x00\x00\x00\x00\x00"  # graphic control ext
        b"\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00"  # image descriptor
        b"\x02\x02\x44\x01\x00"  # LZW data
        b"\x3B"  # trailer
    )


def _raw_min_jpeg() -> bytes:
    # Baseline JFIF, 1x1, three components: the bytes libjpeg-turbo
    # writes for one white pixel at quality 85 with optimized Huffman
    # tables (the settings of `_pil_solid_color_jpeg`). Frozen here, one
    # segment per line, so this path needs no encoder.
    return bytes.fromhex(
        "ffd8"  # SOI
        "ffe000104a46494600010100000100010000"  # APP0: JFIF 1.1
        "ffdb004300"  # DQT 0, followed by its 64 entries
        "0503040404030504040405050506070c08070707070f0b0b090c110f1212110f"
        "111113161c1713141a1511111821181a1d1d1f1f1f13172224221e241c1e1f1e"
        "ffdb004301"  # DQT 1, followed by its 64 entries
        "0505050706070e08080e1e1411141e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e"
        "1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e1e"
        "ffc00011080001000103012200021101031101"  # SOF0: 8-bit, 1x1, 3 components
        "ffc4001500010100000000000000000000000000000008"  # DHT: DC table 0
        "ffc40014100100000000000000000000000000000000"  # DHT: AC table 0
        "ffc40014010100000000000000000000000000000000"  # DHT: DC table 1
        "ffc40014110100000000000000000000000000000000"  # DHT: AC table 1
        "ffda000c03010002110311003f00"  # SOS
        "b2c007"  # entropy-coded data
        "ffd9"  # EOI
    )


def _raw_min_webp() -> bytes:
    # Lossless WebP (VP8L) for a 1x1 white pixel. The payload is the one
    # libwebp writes, frozen here so this path needs no encoder: a
    # signature byte, 14 bits each for width and height minus one, the
    # alpha flag, three version bits (zero), then the bitstream. Only
    # the RIFF container is built by hand: ASCII "RIFF" + size + "WEBP"
    # + "VP8L" + chunk size + payload.
    vp8l_payload = bytes.fromhex("2f0000000045ff23fa1f")
    vp8l_chunk = b"VP8L" + struct.pack("<I", len(vp8l_payload)) + vp8l_payload
    if len(vp8l_payload) % 2 == 1:
        vp8l_chunk += b"\x00"  # RIFF padding to even byte boundary
    riff_payload = b"WEBP" + vp8l_chunk
    return b"RIFF" + struct.pack("<I", len(riff_payload)) + riff_payload


_FORMATS = ["png", "jpeg", "gif", "webp"]


def _items(rng: random.Random, count: int) -> Iterator[CorpusItem]:
    image_module = _try_import_pil()
    encoding = "pil" if image_module is not None else "raw_minimal"
    rounds = (count // len(_FORMATS)) + 1
    if image_module is None:
        # The fallback samples are constants: a second round would repeat
        # the first, and `write_corpus` rejects repeated content.
        rounds = 1
    yielded = 0
    for round_idx in range(rounds):
        for fmt in _FORMATS:
            if yielded >= count:
                return
            color = _palette(rng)
            if image_module is not None:
                if fmt == "png":
                    payload = _pil_solid_color_png(image_module, color)
                elif fmt == "jpeg":
                    payload = _pil_solid_color_jpeg(image_module, color)
                elif fmt == "gif":
                    payload = _pil_solid_color_gif(image_module, color)
                else:
                    payload = _pil_solid_color_webp(image_module, color)
            else:
                color = _RAW_MIN_COLOR  # what the constants actually hold
                if fmt == "png":
                    payload = _raw_min_png()
                elif fmt == "jpeg":
                    payload = _raw_min_jpeg()
                elif fmt == "gif":
                    payload = _raw_min_gif()
                else:
                    payload = _raw_min_webp()
            yield CorpusItem(
                payload=payload,
                extension=fmt if fmt != "jpeg" else "jpg",
                category=f"valid-{fmt}",
                extra={
                    "format": fmt,
                    "encoding": encoding,
                    "color_rgb": list(color),
                    "round": round_idx,
                    "purpose": "harness-false-positive-baseline",
                },
            )
            yielded += 1


def generate(corpus_dir: Path, *, count: int = DEFAULT_COUNT, seed: int = DEFAULT_SEED) -> dict:
    rng = random.Random(seed)
    items = list(_items(rng, count))
    pil_present = _try_import_pil() is not None
    return write_corpus(
        corpus_dir,
        items,
        name=NAME,
        source_policy="synthetic",
        publication_policy="sanitized_candidate",
        seed=seed,
        count=count,
        generator_extra={
            "module": "smabench.ring1.media_corpus",
            "encoder": "pil" if pil_present else "raw_minimal",
            "pil_available": pil_present,
            "formats": _FORMATS,
            "purpose": (
                "Valid baseline samples to confirm reprochain harnesses do not "
                "false-positive on legal input. Crash-inducing bytes belong under "
                "reprochain/corpora-private only."
            ),
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the SMABench Ring 1 media corpus.")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)
    out = args.out or (Path(__file__).resolve().parents[2] / "smabench" / "ring1" / "media-corpus")
    md = generate(out, count=args.count, seed=args.seed)
    print(f"media-corpus: {md['item_count']} items, sha256={md['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
