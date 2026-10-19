# ECE blueprint-paper design

Reference: [AI Engineering from Scratch](https://aiengineeringfromscratch.com/). Captured on 20 October 2026 (local time) at 1440 × 1050 and 390 × 844. The screenshots and computed styles are in [research/ui](research/ui). The [web-ui-copy](https://github.com/koppx/web-ui-copy) mirror and style-snapshot scripts were used to inspect the source. This is a same-style adaptation with original ECE content, not a pixel-identical reproduction.

## Tokens and type

| Token | Light value | Purpose |
|---|---|---|
| Paper | `#fafaf5` | Main background |
| Ink | `#1a1a1a` | Body text |
| Muted | `#4a4a4a` | Secondary text |
| Faint | `#7a7a78` | Small annotations |
| Blueprint | `#3553ff` | Titles, links, diagrams |
| Surface | `#f3f1e8` | Terminal and inset panels |
| Rule | `rgba(26,26,26,.16)` | Thin boundaries |

The paper has a 16px dotted grid. Panels have square corners, fine borders, and no shadows. VT323 supplies the pixel display headings; Source Serif 4 supplies reading text; JetBrains Mono supplies labels and controls. Fonts are served locally with their OFL licenses.

The desktop hero uses a 128px uppercase display title, 0.86 line height and 0.02em tracking. Body text is 18px with 1.62 line height. The header is 64px tall; the content width is capped around 1240px. Controls use compact monospaced labels and outlined rectangles.

## Layout and behavior

The wide homepage pairs its title, introduction, four actions and terminal example with a thought experiment and a three-plate figure carousel. Below it: two-column introduction, interactive workbench entry, four learning paths, progress bars, 24 expandable module rows, and colophon. At narrower widths the figure sidebar is hidden, content becomes one column, and the header offers a menu and search button.

The ECE adaptation adds locally stored dark-paper preference, preserves the lesson reader and numerical workbench, and replaces the reference's illustrations with Hairline phone, hub, and dish figures. These are conceptual illustrations, not circuit simulators. Autonomous playback is disabled; the engine supports reduced motion. A static original SVG fallback remains available if the ES module cannot load.

## Verification

Browser tests cover repeated carousel replacement, one mounted SVG per active figure, remounting after navigation, theme persistence, menu dismissal, search focus, reduced-motion rendering, and horizontal overflow on seven mobile routes. Screenshots in [artifacts](artifacts) document the implemented UI. Source and local page geometry differ because the course text, navigation, and figures differ; exact visual identity is not claimed.
