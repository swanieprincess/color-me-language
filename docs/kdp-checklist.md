# KDP checklist (paperback)

- [ ] Trim size 8.5 × 11 in, interior black & white, white paper.
- [ ] Interior PDF: **export flattened** (Moda `flatten=true`, `pixel_ratio=4`,
      ≈380 dpi). The text-layer export drops the black edge of the outline
      lettering and the words come out white-on-white. No bleed needed for this
      layout; margins ≥ 0.375 in on the gutter side for 24–150 pages (our frame
      starts at 0.5 in).
- [ ] Page count even (add a blank or notes page if odd).
      The Inkscape interior is 34 pages (title, copyright, 32 animals); the cover
      spine for 34 white pages is 34 × 0.002252 = 0.0766 in, so widen the spine in
      `templates/cover.svg` from 0.0721 in before exporting the cover.
- [ ] Title page + copyright page at the front. KDP title: **The Learning Dojo**,
      subtitle **Animals, Volume 1** (series name: The Learning Dojo), author
      **Swan Moon**.
- [ ] Cover: full-wrap PDF from `templates/cover.svg` (sized for 32 pages on white
      paper: spine 0.0721 in, document 17.3221 × 11.25 in). If the page count
      changes, re-run KDP's cover calculator and resize the spine. 300 dpi,
      0.125 in bleed, delete the GUIDES layer before export.
- [ ] ISBN: free KDP ISBN or own.
- [ ] Categories: Children's Coloring Books; Foreign Language Study.
- [ ] Keywords: bilingual coloring book, Korean, Japanese, hanja, animals.
