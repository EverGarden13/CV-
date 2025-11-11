# Report Figures and Tables Placement Guide

This guide explains where to insert the generated figures and tables in the final Word/PDF version of the COMP5523 Project Report.

## Generated Files Location

All figures and tables are located in: `docs/report_figures/`

## Placement Instructions

### Section 6.1 - Performance Metrics

**After the paragraph ending with "...well below the 1GB limit."**

Insert:
1. **Table 1** (`table1_performance_summary.csv` or `.txt`)
   - Caption: "Table 1: System Performance Summary - Comparison of target and achieved metrics across all performance categories"
   - Format as a professional table with borders
   - Use the CSV file to create the table in Word

2. **Figure 4** (`figure1_performance_comparison.png`)
   - Caption: "Figure 4: Performance Metrics Comparison - Visual comparison between target and achieved performance across key metrics"
   - Insert as image, centered
   - Recommended width: 6 inches

### Section 6.2 - Detection Accuracy Assessment

**After the paragraph starting with "Person detection achieves..."**

Insert:
1. **Table 2** (`table2_detection_accuracy.csv` or `.txt`)
   - Caption: "Table 2: Object Detection Accuracy by Class - Detailed precision, recall, and F1-scores for each target object class"
   - Format as a professional table

2. **Figure 5** (`figure2_detection_accuracy.png`)
   - Caption: "Figure 5: Detection Accuracy by Object Class - Comparison of precision and recall across the four target classes"
   - Insert as image, centered
   - Recommended width: 6 inches

### Section 6.3 - OCR Performance Analysis

**After the paragraph ending with "...in challenging lighting conditions."**

Insert:
1. **Figure 6** (`figure3_ocr_accuracy.png`)
   - Caption: "Figure 6: OCR Performance by Text Type - Word accuracy percentages across different text types and conditions"
   - Insert as image, centered
   - Recommended width: 6 inches

### Section 6.4 - Processing Latency Analysis

**After the paragraph starting with "Detection latency distribution..."**

Insert:
1. **Figure 7** (`figure4_latency_distribution.png`)
   - Caption: "Figure 7: Detection Latency Distribution - Histogram showing distribution of detection latencies across 100 test runs with target and average thresholds"
   - Insert as image, centered
   - Recommended width: 6 inches

### Section 6.5 - Manual Testing Scenarios

**After the paragraph starting with "Five comprehensive testing scenarios..."**

Insert:
1. **Table 3** (`table3_testing_scenarios.csv` or `.txt`)
   - Caption: "Table 3: Manual Testing Scenarios Results - Comprehensive testing results across eight distinct scenarios with success rates and notes"
   - Format as a professional table
   - This table is wider, so you may need to adjust font size to 10pt or use landscape orientation for this page

## Mermaid Diagrams

The report includes three Mermaid diagrams that need to be rendered:

### Figure 1 - System Architecture (Section 4.1)
- Located in the markdown after "Figure 1 illustrates the system architecture..."
- Use a Mermaid renderer (mermaid.live, VS Code extension, or online tool)
- Export as PNG at high resolution (300 DPI)
- Insert as image, centered
- Recommended width: 6.5 inches (full page width)

### Figure 2 - Object Detection Pipeline (Section 4.2)
- Located in the markdown after "The system processes every third frame..."
- Render and export as PNG
- Insert as image, centered
- Recommended width: 6 inches

### Figure 3 - OCR Processing Pipeline (Section 4.4)
- Located in the markdown after "The preprocessing pipeline includes..."
- Render and export as PNG
- Insert as image, centered
- Recommended width: 6 inches

## Rendering Mermaid Diagrams

### Option 1: Using mermaid.live (Recommended)
1. Go to https://mermaid.live/
2. Copy the mermaid code from the markdown (between ```mermaid and ```)
3. Paste into the editor
4. Click "Actions" → "PNG" to download
5. Use high quality settings (300 DPI)

### Option 2: Using VS Code
1. Install "Markdown Preview Mermaid Support" extension
2. Open the markdown file
3. Right-click on the diagram in preview
4. Select "Copy Image" or use screenshot tool
5. Paste into Word document

### Option 3: Using Command Line
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Convert each diagram
mmdc -i diagram.mmd -o diagram.png -w 2000 -H 1500
```

## Formatting Tips for Word/Google Docs

1. **Tables:**
   - Use "Table Grid" style or similar professional table format
   - Header row should be bold with light gray background
   - Alternate row shading for better readability
   - Center-align numeric columns
   - Left-align text columns

2. **Figures:**
   - Center all images
   - Add 6pt spacing before and after
   - Ensure captions are in italic, 11pt font
   - Number figures sequentially (Figure 1, Figure 2, etc.)

3. **Captions:**
   - Place table captions ABOVE the table
   - Place figure captions BELOW the figure
   - Use format: "Table X: Title" or "Figure X: Title"
   - Add brief description after the title

4. **Page Layout:**
   - If a figure/table doesn't fit on the current page, move it to the next page
   - Keep caption with its figure/table (use "Keep with next" paragraph setting)
   - Ensure text flows naturally around insertions

## Final Checklist

- [ ] All 4 generated PNG figures inserted
- [ ] All 3 tables formatted and inserted
- [ ] All 3 Mermaid diagrams rendered and inserted
- [ ] All captions properly formatted and numbered
- [ ] Page count still within 8 pages (excluding references)
- [ ] All figures are high resolution (300 DPI minimum)
- [ ] Tables are readable and professionally formatted
- [ ] Text flows naturally around figures and tables

## Notes

- The report is designed to fit within 8 pages with all figures and tables
- If space is tight, you can reduce figure sizes slightly (minimum 5 inches width)
- Table 3 is the largest - consider landscape orientation for that page if needed
- Ensure all figures are legible when printed in black and white
- The color schemes used are colorblind-friendly

## Questions?

If you need to regenerate any figures with different parameters, edit `scripts/generate_report_figures.py` and run:
```bash
python3 scripts/generate_report_figures.py
```
