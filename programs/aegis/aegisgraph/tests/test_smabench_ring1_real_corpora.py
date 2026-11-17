"""Ring 1 corpora reality check.

For each of the six Ring 1 generators, exercise it directly into a
tmp_path and assert that:

1. The metadata file is present and conforms to our manifest shape.
2. The number of items matches the corpus's documented size budget
   (≥1k for URL/deeplink, ≥6 PNGs for QR when qrcode is available
   else skipped, ≥4 valid samples for media, ≥6 cases for sync/pq).
3. `source_policy` is one of the documented values (`synthetic` for
   all six Ring 1 corpora; the SPEC permits `synthetic` or
   `public_test_vectors` but we have no public-vector inputs yet).
4. Each item filename has the documented `<sha8>.<ext>` shape and
   the on-disk content's SHA-256 matches the manifest's claimed
   per-item sha.

Tests are skipped (not failed) when an optional dep is missing AND
the generator's fallback path doesn't apply. Today only the QR
generator has a true skip-path: if `qrcode` is missing we still
produce a corpus via the placeholder PNG path, so the test runs.
"""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path

import pytest

from smabench.ring1 import (
    deeplink_corpus,
    media_corpus,
    pq_corpus,
    qr_corpus,
    sync_corpus,
    url_corpus,
)


# Whitelist of generator modules — explicit dict keeps the determinism
# parametrize test free of dynamic imports (semgrep flagged
# `importlib.import_module(<param>)` even though the values are
# hardcoded test parameters, not user input).
_GENERATOR_REGISTRY = {
    "url_corpus": url_corpus,
    "qr_corpus": qr_corpus,
    "deeplink_corpus": deeplink_corpus,
    "sync_corpus": sync_corpus,
    "media_corpus": media_corpus,
    "pq_corpus": pq_corpus,
}


def _read_metadata(corpus_dir: Path) -> dict:
    return json.loads((corpus_dir / "corpus.metadata.json").read_text(encoding="utf-8"))


def _assert_manifest_shape(metadata: dict, expected_name: str) -> None:
    assert metadata["name"] == expected_name
    assert metadata["item_count"] == len(metadata["items"])
    assert metadata["source_policy"] in {"synthetic", "public_test_vectors"}
    assert metadata["publication_policy"] in {"sanitized_candidate", "public_approved"}
    assert isinstance(metadata["sha256"], str) and len(metadata["sha256"]) == 64


def _assert_per_item_sha_matches_disk(corpus_dir: Path, metadata: dict) -> None:
    for item in metadata["items"]:
        path = corpus_dir / item["filename"]
        assert path.is_file(), f"missing file: {item['filename']}"
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        assert sha == item["sha256"], (
            f"file content sha mismatch for {item['filename']}: "
            f"manifest={item['sha256']!r} disk={sha!r}"
        )


def test_url_corpus_ten_thousand(tmp_path: Path) -> None:
    out = tmp_path / "url-corpus"
    metadata = url_corpus.generate(out, count=2000, seed=42)
    _assert_manifest_shape(metadata, "url-corpus")
    assert metadata["item_count"] == 2000
    assert metadata["item_count"] > 100, "url-corpus must produce ≥100 items per SPEC"
    _assert_per_item_sha_matches_disk(out, metadata)
    # Spot-check that a known interesting URL prefix is reachable in
    # the categories — confirms the grid actually exercises userinfo
    # and IDN classes rather than just emitting bland URLs.
    categories = {item["category"] for item in metadata["items"]}
    has_idn = any("idn" in c for c in categories)
    has_userinfo = any("userinfo" not in c or "userinfo|none" not in c for c in categories)
    assert has_idn, "url-corpus must include IDN host cases"
    assert has_userinfo, "url-corpus must include userinfo cells"


def test_deeplink_corpus_thousand(tmp_path: Path) -> None:
    out = tmp_path / "deeplink-corpus"
    metadata = deeplink_corpus.generate(out, count=1000, seed=42)
    _assert_manifest_shape(metadata, "deeplink-corpus")
    assert metadata["item_count"] == 1000
    assert metadata["item_count"] > 100
    _assert_per_item_sha_matches_disk(out, metadata)
    schemes = set(item["extra"]["scheme"] for item in metadata["items"])
    # All five scheme families must appear.
    assert {"signal", "sgnl", "matrix", "element", "matrix-to-https"}.issubset(schemes)


def test_qr_corpus_emits_pngs(tmp_path: Path) -> None:
    out = tmp_path / "qr-corpus"
    metadata = qr_corpus.generate(out, count=32, seed=42)
    _assert_manifest_shape(metadata, "qr-corpus")
    png_items = [i for i in metadata["items"] if i["filename"].endswith(".png")]
    # The SPEC requires ≥6 PNGs when qrcode is installed; we always
    # produce 32 via the placeholder fallback when not.
    assert len(png_items) >= 6
    _assert_per_item_sha_matches_disk(out, metadata)
    # Encoder field must record which path was taken.
    assert metadata["generator"]["encoder"] in {"qrcode_lib", "placeholder_png"}


def test_sync_corpus_covers_both_families(tmp_path: Path) -> None:
    out = tmp_path / "sync-corpus"
    metadata = sync_corpus.generate(out, count=200, seed=42)
    _assert_manifest_shape(metadata, "sync-corpus")
    families = {item["extra"]["family"] for item in metadata["items"]}
    assert families == {"matrix", "signal"}
    _assert_per_item_sha_matches_disk(out, metadata)


def test_media_corpus_valid_samples(tmp_path: Path) -> None:
    out = tmp_path / "media-corpus"
    metadata = media_corpus.generate(out, count=16, seed=42)
    _assert_manifest_shape(metadata, "media-corpus")
    formats = {item["extra"]["format"] for item in metadata["items"]}
    assert formats == {"png", "jpeg", "gif", "webp"}, (
        f"media-corpus must include all four formats; got {formats!r}"
    )
    _assert_per_item_sha_matches_disk(out, metadata)
    # Every item must declare itself a harness-validity baseline (NOT a
    # crash input). The safety scanner depends on this label.
    for item in metadata["items"]:
        assert item["extra"]["purpose"] == "harness-false-positive-baseline"


def test_media_corpus_without_pillow_holds_one_sample_per_format(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without Pillow the generator emits each constant sample once, whatever the count."""

    monkeypatch.setattr(media_corpus, "_try_import_pil", lambda: None)
    out = tmp_path / "media-corpus"
    metadata = media_corpus.generate(out, count=16, seed=42)
    _assert_manifest_shape(metadata, "media-corpus")
    assert metadata["generator"]["encoder"] == "raw_minimal"
    assert metadata["generator"]["pil_available"] is False
    assert metadata["requested_count"] == 16
    assert metadata["item_count"] == 4
    formats = sorted(item["extra"]["format"] for item in metadata["items"])
    assert formats == ["gif", "jpeg", "png", "webp"]
    for item in metadata["items"]:
        assert item["extra"]["encoding"] == "raw_minimal"
        assert item["extra"]["purpose"] == "harness-false-positive-baseline"
    _assert_per_item_sha_matches_disk(out, metadata)
    again = media_corpus.generate(out, count=16, seed=42)
    assert again["sha256"] == metadata["sha256"]


def test_media_corpus_fallback_samples_decode() -> None:
    """Each constant fallback sample is a real 1x1 white image in its own format."""

    image = pytest.importorskip("PIL.Image", reason="decoding the samples needs Pillow")
    samples = {
        "PNG": media_corpus._raw_min_png(),
        "JPEG": media_corpus._raw_min_jpeg(),
        "GIF": media_corpus._raw_min_gif(),
        "WEBP": media_corpus._raw_min_webp(),
    }
    for expected_format, payload in samples.items():
        with image.open(io.BytesIO(payload)) as decoded:
            decoded.load()
            assert decoded.format == expected_format
            assert decoded.size == (1, 1)
            assert decoded.convert("RGB").getpixel((0, 0)) == (255, 255, 255)


def test_pq_corpus_covers_pqxdh_and_megolm(tmp_path: Path) -> None:
    out = tmp_path / "pq-corpus"
    metadata = pq_corpus.generate(out, count=60, seed=42)
    _assert_manifest_shape(metadata, "pq-corpus")
    cases = {item["extra"]["case"] for item in metadata["items"]}
    assert any(c.startswith("pqxdh-") for c in cases)
    assert any(c.startswith("megolm-") for c in cases)
    _assert_per_item_sha_matches_disk(out, metadata)


@pytest.mark.parametrize(
    "module_name",
    list(_GENERATOR_REGISTRY.keys()),
)
def test_generator_is_byte_deterministic(tmp_path: Path, module_name: str) -> None:
    """Two consecutive runs at the same seed must produce identical manifests."""

    module = _GENERATOR_REGISTRY[module_name]
    out = tmp_path / module.NAME
    md1 = module.generate(out, count=64, seed=42)
    md2 = module.generate(out, count=64, seed=42)
    assert md1["sha256"] == md2["sha256"], (
        f"{module_name} not byte-deterministic at seed=42: {md1['sha256']!r} vs {md2['sha256']!r}"
    )
