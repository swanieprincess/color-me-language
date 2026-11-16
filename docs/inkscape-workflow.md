# Inkscape workflow

Inkscape takes over two jobs the Moda pipeline does imperfectly: converting the
generated raster line art into real vectors, and producing a print PDF whose
outline lettering is guaranteed to render.

## 1. Vectorize a page's art (Trace Bitmap)

1. Export the page art from Moda as PNG at pixel ratio 4 (≈3,264 × 4,224 px for
   a full page, or just the 720 × 960 art frame at 4× = 2,880 × 3,840).
2. In Inkscape: **File → Import** the PNG, select it, then
   **Path → Trace Bitmap** (Shift+Alt+B).
   - Mode: **Single scan → Brightness cutoff**, threshold ≈ 0.45–0.55.
   - Options: Speckles ≈ 2–4 (removes dust), Smooth corners ≈ 1.0, Optimize ≈ 0.2.
   - Tick **Remove background**. Click **Apply**, then delete the original PNG.
3. The result is one black path. Lines are now crisp at any size and the file
   is tiny. Fix stray marks with the node tool, or thicken thin lines with
   **Path → Outset** (set the outset step in Preferences → Behavior → Steps).
4. For the swan's black bill mask (the one filled area) nothing special is
   needed; the trace keeps filled regions filled.

Batch, from a terminal (Inkscape 1.2+):

```bash
for f in art/*.png; do
  inkscape "$f" --actions="select-all;object-to-path;select-all;\
org.inkscape.filter.trace-bitmap;export-type:svg;export-filename:${f%.png}.svg;export-do"
done
```

(Trace parameters can be set in Preferences → the Trace Bitmap dialog remembers
its last settings; for heavy batching the `potrace` CLI with
`potrace -s -t 4 -a 1.0 --blacklevel 0.5 page.pbm` gives identical results.)

## 2. Lay out pages in Inkscape

Open `templates/page.svg`. It is the same layout as the Moda template:
US Letter, art frame, four corner tags, outline lettering, page number.

- Paste or link the traced SVG art into the **Art** layer inside the frame.
- Edit the four words in the **Words** layer. Fonts: Fredoka, Noto Sans KR,
  Noto Sans JP, Noto Sans TC (all free on Google Fonts; install them locally).
- The words are white-filled text with a black stroke, so they are already
  colorable. Before export, select all text and **Path → Object to Path** so
  the PDF never depends on fonts and the stroke is baked in.
- **Document Properties** supports multiple pages (Inkscape 1.2+): duplicate
  the page for each animal, or keep one SVG per page and combine the PDFs.

## 3. Export for KDP

**File → Save a Copy → PDF**. In the dialog: *Convert text to paths*,
resolution for rasterization 300 dpi (only matters if any raster remains),
no bleed for this layout. Check the PDF in a viewer: every word must show
black outlines on white. Then upload to KDP.

## Why this matters

- Vector lines print perfectly clean at 300 dpi; raster at 4× is close but
  not identical.
- Text as paths cannot suffer the white-on-white bug the Moda text-layer
  export had.
- A vector page is the right master for merch later (stickers, shirts), where
  print sizes vary.
