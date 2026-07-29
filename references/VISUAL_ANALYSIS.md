# Direct Visual Analysis Policy

## No OCR engines

Do not invoke Tesseract, PaddleOCR, cloud OCR services, or an OCR library. Native text extraction from PDF, EPUB, or DOCX is allowed because it is not OCR.

## Required workflow

1. Read the native text layer when available.
2. Identify pages that contain charts, tables, diagrams, annotations, or scanned content.
3. Render those pages to images using tools available in the host environment.
4. Inspect the page images directly with the host agent's multimodal capabilities.
5. Connect each visual interpretation to its page, figure, caption, and surrounding text.
6. Record inspected and unresolved figures in `reports/visual-coverage.yaml`.

## Visual elements to capture

- candlesticks and bar relationships;
- volume bars and volume-price relationships;
- moving averages and trend lines;
- support, resistance, breakout, and pullback annotations;
- arrows, labels, entry/exit marks, and figure captions;
- wave or swing segmentation;
- tables and formula diagrams;
- differences between an idealized diagram and a historical example.

## Prohibited shortcuts

- Do not treat screenshot pixel angles as financial trend angles.
- Do not infer exact numeric thresholds from a sketch unless the source defines them.
- Do not silently skip image-only pages.
- Do not claim full visual coverage when some relevant pages were not inspected.
- Do not convert an author's visual explanation into a guaranteed buy or sell instruction.

## Capability failure

When image inspection is unavailable, set `host_visual_capability: unavailable`, list the blocked pages, keep image-dependent candidates out of `installable/`, and explain the limitation in the generation report.
