# KDP checklist (paperback)

- [ ] Trim size 8.5 × 11 in, interior black & white, white paper.
- [ ] Interior PDF: **export flattened** (Moda `flatten=true`, `pixel_ratio=4`,
      ≈380 dpi). The text-layer export drops the black edge of the outline
      lettering and the words come out white-on-white. No bleed needed for this
      layout; margins ≥ 0.375 in on the gutter side for 24–150 pages (our frame
      starts at 0.5 in).
- [ ] Page count even (add a blank or notes page if odd).
      The Inkscape interior is 34 pages (title, copyright, 32 animals).
- [ ] Check the colored title page in KDP's previewer: a B&W interior prints it
      in grayscale, so the colors must still read as distinct grays. Its
      yellow background runs to the page edge: either turn on interior bleed
      (page 8.625 x 11.25 in, background extended 0.125 in past trim) or accept
      a thin white edge where KDP trims. The title's neon glow is an SVG
      filter: export the PDF at 300 dpi or more so Inkscape rasterizes it cleanly.
- [ ] Title page + copyright page at the front. KDP title: **The Learning Dojo**,
      subtitle **Animals, Volume 1** (series name: The Learning Dojo), author
      **Swan Moon**.
- [ ] Cover: full-wrap PDF from `templates/cover.svg` (sized for 34 pages on white
      paper: spine 34 × 0.002252 = 0.0766 in, document 17.3266 × 11.25 in). If the page count
      changes, re-run KDP's cover calculator and resize the spine. 300 dpi,
      0.125 in bleed, delete the GUIDES layer before export.
- [ ] ISBN: free KDP ISBN or own.
- [ ] Categories: Children's Coloring Books; Foreign Language Study.
- [ ] Keywords: bilingual coloring book, Korean, Japanese, hanja, animals.
