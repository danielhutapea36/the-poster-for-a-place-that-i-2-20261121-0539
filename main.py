#!/usr/bin/env python3
"""Velmara -- The Poster for a Place That Isn't There.

Entry program for the make.fun
the-poster-for-a-place-that-i-2-20261121-0539 bounty. It copies the bundled
image (entry.png) byte-for-byte into the output directory after checking
that it really is a PNG file.

The image is a travel poster for Velmara, a place that does not exist: a
valley of floating islands where the waterfalls fall upward into a violet
and amber sky, with lantern-lit houses and sailboats on the lake below.

Standard library only. No network, no randomness, no timestamps, so two
runs always write the same bytes.
"""

import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(here, SOURCE_NAME)

    with open(source_path, "rb") as handle:
        magic = handle.read(8)
    if magic != PNG_MAGIC:
        print(f"error: {SOURCE_NAME} is not a PNG file", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, SOURCE_NAME)

    shutil.copyfile(source_path, destination)

    with open(destination, "rb") as handle:
        data = handle.read()
    if data[:8] != PNG_MAGIC:
        print(f"error: {destination} is not a PNG file", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {destination} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
