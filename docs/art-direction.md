# Art direction

## Style

Kawaii / chibi baby animals in the style of the sticker-sheet references:
oversized round head, tiny chubby body, huge glossy round eyes with big
highlights, little round blush cheeks, sweet happy expression. Line art only.

## Rules

- Black outlines on pure white. Every shape is left white inside so a child can
  color it. No shading, no gray tones, no solid black fills — this matters for
  pandas, zebras, raccoons and penguins, whose dark patches must be outlined,
  not filled.
- One deliberate exception: the swan's bill knob and face mask are solid black,
  because without them it reads as a goose.
- No text, letters or watermarks inside the art. The words are live text layers.
- The animal is centered and large. Trinkets are themed to the animal and spread
  toward the edges; the four corners stay mostly empty so the word tags sit
  cleanly over them.
- Portrait 3:4 generation, placed into the 720 × 960 frame.

## Prompt skeleton

```
Full-page children's coloring book illustration, portrait format. In the
center, a large extremely cute kawaii baby <ANIMAL> drawn in the same chibi
baby-animal style as the reference image: <ANIMAL-SPECIFIC FEATURES>, huge
glossy round eyes with big highlights, little round blush cheeks, sweet happy
smile. Around the <ANIMAL>, scattered playful decorations that fill the page:
<TRINKETS>. Keep the decorations spread toward the edges and leave the four
corners of the image mostly empty. Use the reference ONLY for character style
and proportions; do not copy its colors. Output must be black-and-white LINE
ART ONLY: simple thick clean black outlines, every shape left white inside so
a child can color it, no shading, no gray tones, no solid black fills, pure
white background, no text, no letters, no watermark.
```

Model used for Volume 1: NanoBanana 2 Lite via Moda, 1K, with the kawaii
sticker sheet as the style reference.

## Word conventions

- Korean: the everyday native word (호랑이, not 虎); loanwords only when that is
  what Koreans actually say (라쿤, 코알라, 판다).
- Japanese: hiragana for native words (ねこ, うさぎ), katakana for loanwords
  (ペンギン, コアラ, ライオン, フラミンゴ, アライグマ).
- Hanja/Chinese: the modern Chinese word in traditional characters, which is
  also the form Korean hanja uses (貓, 企鵝, 無尾熊, 貓頭鷹).

## Marine Life: East Asian theme (Swan, 2026-10-27)

Same kawaii line-art animal as Volume 1, with East Asian decorations around it:
simple Hokusai-style curling waves, a band of seigaiha wave-scale pattern on the
sea floor, auspicious swirl clouds (Korean and Chinese cloud motif) and floating
cherry blossom petals, plus bubbles, shells and tiny smiling fish. Add one
animal-specific touch where it fits (an octopus pot for the octopus, a full moon
for the sea otter).

- Model: nano-banana-lite via Moda, 3:4, about 10 credits per page on the free
  plan. Style reference: an export of the Volume 1 turtle page.
- Pages are built in Moda first (art frame, four tags, page number, same sizes
  as Volume 1), then the art is generated into the frame. Moda refuses to
  generate into an empty canvas.
- Test pages approved by Swan: shark, octopus, sea otter, clownfish.
- **Clouds only in the sky** (Swan, 2026-10-27: "why are there clouds in the
  water"). Swirl clouds go above the waterline, never underwater. Underwater
  scenes use bubbles, seaweed and swirling water currents instead, and a page
  with clouds must show the sky and the waterline.
