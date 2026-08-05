#!/usr/bin/env python3
"""Pack a compiled guide into the SuuntoPlus archive suuntool uploads.

suuntool is byte-transparent — `guides upload` sends whatever zip bytes it is handed and
never opens or validates the archive. So everything the format requires has to be correct
before it gets there, and this script is the last place that can be true.

The archive is a plain zip with exactly three flat entries, no directories, no nesting:
    manifest.json   small metadata block
    guide.json      the workout (see compile_guide.py)
    icon.png        exactly 300x300

Determinism is the point. JSON is serialised with a stable two-space indent and the zip uses a
fixed fake mtime rather than the real clock, so identical guide content always produces
byte-identical archive bytes. That is what makes "has this session changed since it was
published" a sha256 comparison instead of a fuzzy one — which is exactly what
rules/publishing.md's `published.suunto` idempotency check assumes it can do.

Determinism is for *our* diffing, not for the API: the server accepts any valid zip and does not
care how it was produced. So don't chase byte-compatibility with some other packer — the only
property worth preserving here is that the same input gives the same output.

Usage:
    python3 scripts/pack_guide.py endurance/2026-08-04-easy-strides.md --out guide.zip
    python3 scripts/pack_guide.py endurance/2026-08-04-easy-strides.md --base64
    python3 scripts/pack_guide.py --all --outdir build/     # every publishable session
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import struct
import sys
import zlib
import zipfile
from pathlib import Path

from compile_guide import ROOT, OWNER, CompileError, compile_session, load_zones

ICON_SIZE = 300
ICON_RGB = (32, 84, 122)     # solid placeholder; a real icon can be dropped in unchanged
# A fixed timestamp, not the clock. The zip epoch's own floor is 1980-01-01, which is the
# conventional choice for reproducible archives.
FIXED_MTIME = (1980, 1, 1, 0, 0, 0)


def solid_icon_png(size: int = ICON_SIZE, rgb: tuple[int, int, int] = ICON_RGB) -> bytes:
    """A minimal solid-colour PNG, built by hand so the repo keeps its zero-dependency rule.

    Each scanline is prefixed with filter byte 0 (None), which is what makes this encodable
    without a real image library. zlib.compress is deterministic at a fixed level, so the
    bytes are stable across runs and machines.
    """
    raw = b"".join(b"\x00" + bytes(rgb) * size for _ in range(size))

    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))  # 8-bit RGB
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def dumps(value: dict) -> bytes:
    """Stable JSON bytes: two-space indent, no trailing whitespace, unicode left raw rather than
    \\u-escaped. Fixed so the same guide always packs to the same archive."""
    return json.dumps(value, indent=2, ensure_ascii=False).encode("utf-8")


def build_manifest(guide: dict) -> dict:
    # `owner` must be identical here and in guide.json — a mismatch is rejected. The value
    # itself is ignored (the server rewrites it to "Suunto"), but the key must be present:
    # omitting it fails deserialisation server-side with an opaque HTTP 400.
    return {
        "name": guide["name"],
        "type": "sequence",
        "owner": OWNER,
        "description": guide["description"],
    }


def pack(guide: dict) -> bytes:
    if guide.get("owner") != OWNER:
        raise CompileError(
            f"manifest/guide owner mismatch ({guide.get('owner')!r} vs {OWNER!r}) — "
            f"rejected before upload")

    entries = [
        ("manifest.json", dumps(build_manifest(guide))),
        ("guide.json", dumps(guide)),
        ("icon.png", solid_icon_png()),
    ]

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in entries:
            info = zipfile.ZipInfo(name, date_time=FIXED_MTIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data, compresslevel=9)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("session", nargs="?", type=Path)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--outdir", type=Path)
    ap.add_argument("--base64", action="store_true", help="print base64 for suuntool guides_upload")
    args = ap.parse_args()

    if args.all:
        zones, failed = load_zones(), 0
        if args.outdir:
            args.outdir.mkdir(parents=True, exist_ok=True)
        for f in sorted((ROOT / "endurance").glob("*.md")):
            try:
                blob = pack(compile_session(f, zones))
            except CompileError as e:
                if "not a watch guide" not in str(e):
                    print(f"  FAIL  {e}")
                    failed += 1
                continue
            digest = hashlib.sha256(blob).hexdigest()[:12]
            if args.outdir:
                (args.outdir / f"{f.stem}.zip").write_bytes(blob)
            print(f"  {f.stem}.zip  {len(blob):>5} bytes  sha256:{digest}")
        return 1 if failed else 0

    if not args.session:
        ap.error("give a session path or --all")
    try:
        blob = pack(compile_session(args.session))
    except CompileError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.base64:
        print(base64.b64encode(blob).decode())
    elif args.out:
        args.out.write_bytes(blob)
        print(f"{args.out}  {len(blob)} bytes  sha256:{hashlib.sha256(blob).hexdigest()[:12]}")
    else:
        print(f"{len(blob)} bytes  sha256:{hashlib.sha256(blob).hexdigest()[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
