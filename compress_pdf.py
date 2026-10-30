#!/usr/bin/env python3
"""
compress_pdf.py — shrink a PDF so it fits in an email / LinkedIn message.

Setup (once):
    pip install pymupdf

Usage:
    python3 compress_pdf.py my_file.pdf                 # medium compression
    python3 compress_pdf.py my_file.pdf --level high    # smallest file
    python3 compress_pdf.py my_file.pdf --level low     # best quality
    python3 compress_pdf.py my_file.pdf -o small.pdf    # choose output name

Levels (images are what make PDFs heavy):
    low    -> images capped at 200 dpi, JPEG quality 85  (print-ish quality)
    medium -> images capped at 150 dpi, JPEG quality 75  (good on screen)
    high   -> images capped at 100 dpi, JPEG quality 60  (smallest, still readable)

Text and vector graphics stay sharp at every level.
"""
import argparse
import os
import sys

import pymupdf

LEVELS = {
    "low": (200, 85),
    "medium": (150, 75),
    "high": (100, 60),
}


def mb(path):
    return os.path.getsize(path) / (1024 * 1024)


def compress(src, dst, level):
    dpi, quality = LEVELS[level]
    doc = pymupdf.open(src)
    # Downsample + recompress every image above the dpi target
    doc.rewrite_images(
        dpi_threshold=dpi + 10,
        dpi_target=dpi,
        quality=quality,
        lossy=True,
        lossless=True,
        bitonal=True,
        color=True,
        gray=True,
    )
    # Drop unused fonts/objects, metadata junk, and compress streams
    doc.subset_fonts()
    doc.scrub(metadata=False, xml_metadata=True, thumbnails=True, reset_fields=False,
              reset_responses=False, remove_links=False, attached_files=False,
              clean_pages=True, embedded_files=False, hidden_text=False,
              javascript=True, redactions=False, redact_images=0)
    doc.save(dst, garbage=4, deflate=True, deflate_images=True,
             deflate_fonts=True, clean=True, use_objstms=1)
    doc.close()


def main():
    p = argparse.ArgumentParser(description="Compress a PDF.")
    p.add_argument("input", help="PDF to compress")
    p.add_argument("-o", "--output", help="output file (default: <name>_compressed.pdf)")
    p.add_argument("--level", choices=LEVELS, default="medium")
    a = p.parse_args()

    if not os.path.isfile(a.input):
        sys.exit(f"File not found: {a.input}")
    out = a.output or os.path.splitext(a.input)[0] + "_compressed.pdf"

    before = mb(a.input)
    compress(a.input, out, a.level)
    after = mb(out)

    if after >= before:
        print(f"Couldn't make it smaller ({before:.2f} MB) — it's probably mostly text already.")
        os.remove(out)
        return
    print(f"{before:.2f} MB -> {after:.2f} MB  ({100 * (1 - after / before):.0f}% smaller)")
    print(f"Saved: {out}")
    if after > 5:
        print("Tip: LinkedIn/email can be picky above ~5 MB — try --level high.")


if __name__ == "__main__":
    main()
