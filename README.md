# Spectral Value Extractor

> **Author:** Defani Arman Alfitriansyah  
> **Date:** June 09, 2026  
> **Version:** 1.0.0  
> **GitHub:** https://github.com/Defani/Spectral-Value-Extractor-QGIS-Tooolbox

---

## Overview

A QGIS Processing tool that extracts raster pixel values (satellite imagery bands, vegetation indices such as NDVI, NDWI, MNDWI, etc.) at field sample point locations automatically.

Key advantage over the built-in QGIS **Sample Raster Values** tool:
- Supports **multiple raster inputs** in a single run
- Directly exports results to a **CSV file**
- Supports **custom band naming**

---

## Installation

1. Open **QGIS 3.x**
2. Go to **Processing → Toolbox**
3. Click the **Python icon (⚙️)** at the top → select **Add Script to Toolbox...**
4. Browse to and select `SpectralValueExtractor_script.py`
5. The tool will appear under **Remote Sensing Tools → Spectral Value Extractor**

---

## Parameters

| Parameter | Description |
|-----------|-------------|
| **Field Sample Points** | Point vector layer (.shp / .gpkg / etc.) containing field sample locations |
| **Point ID / Label Field** | Select the column that uniquely identifies each point (e.g. `Sample_ID`, `No`, `Name`) |
| **Raster / Spectral Index Layers** | Select one or more raster layers — different CRS and resolutions are handled automatically |
| **Custom Band Names** | Optional. Example: `B2_Blue,B3_Green,B4_Red,NDVI` — if left empty, column names are taken from the raster file names |
| **Include X and Y Coordinate Columns** | Check to append X and Y coordinate columns to the output |
| **Save Output as CSV** | File path for the CSV output |
| **Output Layer** | New point layer in QGIS with spectral values as attributes |

---

## Example

**Scenario:** You have 50 field sample points and want to extract values from:
- Sentinel-2 imagery (10 bands)
- NDVI layer (1 band)
- NDWI layer (1 band)

**Steps:**
1. Load all raster layers into QGIS
2. Open the tool and select the sample point layer
3. Select the ID column, e.g. `Sample_ID`
4. Select all three rasters under Raster Layers (hold Ctrl for multi-select)
5. Optionally fill in custom band names: `B2,B3,B4,B5,B6,B7,B8,B8A,B11,B12,NDVI,NDWI`
6. Check Include X and Y Coordinate Columns
7. Set the CSV output path
8. Click **Run**

**Example CSV output:**
```
Sample_ID, X_Coord, Y_Coord, B2, B3, B4, NDVI, NDWI
T001, 108.5231, -6.8821, 0.0612, 0.0891, 0.1203, 0.4521, 0.1832
T002, 108.5291, -6.8756, 0.0534, 0.0762, 0.0983, 0.5102, 0.2211
```

---

## Notes

- If the point layer and raster layers have **different CRS**, the tool reprojects automatically — no manual reprojection needed.
- For **multi-band rasters** (Sentinel-2, Landsat, etc.), all bands are extracted in a single run.
- Shapefile attribute column names are limited to **10 characters** — use the CSV output for full-length band names.
- If a point falls outside the raster extent, the column value will be `NULL`.

---

## Requirements

- QGIS 3.16 or later
- Python 3.x (included with standard QGIS installation)
- Libraries: `gdal`, `numpy` (included with standard QGIS installation)
