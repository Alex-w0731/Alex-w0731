# The Curiosity Lab — original Killua motion design

A six-second seamless ambient loop for Alex Wang's GitHub profile. The original AI-generated character illustration is animated with authored transforms, molecular orbits, electricity, and bubbles. Character expression and limbs remain part of the original illustration; the animation is motion graphics, not frame-by-frame character acting.

## Reproduce

Requirements: Node.js 22+, FFmpeg / FFprobe on PATH, and HyperFrames 0.8.30. Run from this directory:

```sh
npx --yes hyperframes@0.8.30 check
npx --yes hyperframes@0.8.30 render --fps 24 --quality high --workers 1 --output ../assets/curiosity-lab.mp4
ffmpeg -y -i ../assets/curiosity-lab.mp4 -filter_complex '[0:v]fps=12,scale=880:336:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff:max_colors=192[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle' -loop 0 ../assets/curiosity-lab.gif
ffmpeg -y -ss 1.5 -i ../assets/curiosity-lab.mp4 -frames:v 1 ../assets/curiosity-lab-poster.png
```

The PNG character has a transparent alpha channel. Keep the image, `gsap.min.js`, and `index.html` together. The `DESIGN.md` file specifies colors, typography, visual intent, and movement constraints. The character generation prompt is in `character-prompt.txt`.

The GSAP source file is version 3.14.2, obtained from [jsDelivr](https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js); its license notice is retained in the file. Molecular diagrams are decorative schematics, not quantitative data. Killua remains the property of the original rights holders; this is unofficial personal fan art.
