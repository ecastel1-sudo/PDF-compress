# compress your pdf

A small Python script that shrinks PDFs so they're light enough to send by email or LinkedIn.

PDFs are usually heavy because of the images inside them. This script downsamples and recompresses those images. It also cleans out unused data and subsets the fonts. Text and vector graphics stay sharp.

## Example

| Level    | Before   | After   |
|----------|----------|---------|
| `low`    | 25.8 MB  | 5.2 MB  |
| `medium` | 25.8 MB  | 0.3 MB  |
| `high`   | 25.8 MB  | 0.2 MB  |

*(Test file: 3 pages with large photos. Your results depend on how much of your PDF is images.)*

## Installation

You need Python 3.9 or newer.

```bash
git clone https://github.com/<your-username>/compress-pdf.git
cd compress-pdf
pip install -r requirements.txt
```

## Usage

```bash
python3 compress_pdf.py my_file.pdf
```

This writes `my_file_compressed.pdf` next to the original and prints how much smaller it got.

### Options

| Option | What it does |
|--------|--------------|
| `--level low` | Best quality: images capped at 200 dpi, JPEG quality 85 |
| `--level medium` | Default, looks good on screen: 150 dpi, quality 75 |
| `--level high` | Smallest file: 100 dpi, quality 60 |
| `-o NAME.pdf` | Choose the output file name |

```bash
python3 compress_pdf.py deck.pdf --level high -o deck_small.pdf
```

## Notes

- Your original file is never modified.
- A PDF that is mostly text is already small and won't shrink much. If the output would come out larger, the script says so and doesn't save it.
- LinkedIn and many email providers cap attachments at a few MB. If the file is still over about 5 MB, try `--level high`.

## How it works

The script uses [PyMuPDF](https://pymupdf.readthedocs.io/). It:
1. Downsamples every image above the target dpi and re-encodes it as JPEG
2. Subsets embedded fonts so only the characters that are used are kept
3. Removes thumbnails, XML metadata and JavaScript
4. Saves with garbage collection, stream compression and object streams

## License

MIT
