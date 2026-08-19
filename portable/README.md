# Portable mode

Export a compact prompt for clients without native Agent Skills support:

```bash
python scripts/export_portable_prompt.py --subject cie-0607-mathematics --output dist/cie0607-portable-prompt.md
```

Give the exported prompt and one six-section feedback record to the model. Save its structured paper JSON, then run `validate_pack.py` and `render_pdfs.py` locally. The model does not lay out PDFs.
