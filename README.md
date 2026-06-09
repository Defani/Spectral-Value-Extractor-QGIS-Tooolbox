# Spectral Value Extractor — Panduan Penggunaan

> **Penulis:** Defani Arman Alfitriansyah  
> **Tanggal Pembuatan:** 09 Juni 2026  
> **Versi:** 1.0.0  
> **GitHub:** https://github.com/Defani/Spectral-Value-Extractor-QGIS-Tooolbox

## Apa itu?
Tool QGIS untuk **mengekstrak nilai piksel raster** (citra satelit, band, atau indeks seperti NDVI/NDWI) 
pada lokasi titik lapangan (ground truth / field samples).

---

## File yang Disertakan

| File | Keterangan |
|------|-----------|
| `SpectralValueExtractor.pyt` | Toolbox lengkap (plugin-style, QGIS 3.x) |
| `SpectralValueExtractor_script.py` | Script sederhana, langsung load ke Processing Toolbox |

---

## Cara Load ke QGIS

### Opsi A — Script Sederhana (Rekomendasi pemula)
1. Buka **QGIS 3.x**
2. Buka **Processing → Toolbox**
3. Klik ikon **Python** (⚙️) di bagian atas Toolbox → **Add Script to Toolbox...**
4. Pilih file `SpectralValueExtractor_script.py`
5. Tool akan muncul di grup **"Spectral Value Extractor"**

### Opsi B — File .pyt (Toolbox style)
1. Salin `SpectralValueExtractor.pyt` ke folder:
   - Windows: `C:\Users\<nama>\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\scripts\`
   - Linux/Mac: `~/.local/share/QGIS/QGIS3/profiles/default/processing/scripts/`
2. Restart QGIS
3. Cari di Processing Toolbox → **Remote Sensing Tools → Spectral Value Extractor**

---

## Parameter Input

| Parameter | Keterangan |
|-----------|-----------|
| **Titik Lapangan** | Layer vektor titik (.shp / .gpkg / dll) — titik sampel lapangan |
| **Kolom ID Titik** | Pilih kolom yang menjadi label/ID unik tiap titik (misal: `No_Titik`, `ID`, `nama`) |
| **Raster / Indeks Spektral** | Pilih satu atau lebih raster (bisa berbeda resolusi/CRS — otomatis ditransformasi) |
| **Nama Band Kustom** | Opsional. Misal: `B2_Blue,B3_Green,B4_Red,NDVI` — jika kosong, nama diambil dari nama file raster |
| **Sertakan XY** | Centang untuk menambahkan kolom koordinat X dan Y pada output |
| **Simpan ke CSV** | Path file CSV output |
| **Layer Output** | Layer titik baru di QGIS dengan nilai spektral sebagai atribut |

---

## Contoh Penggunaan

**Skenario:** Punya 50 titik sampel lapangan, mau ekstrak nilai dari:
- Citra Sentinel-2 (10 band)
- Layer NDVI (1 band)
- Layer NDWI (1 band)

**Langkah:**
1. Load semua raster ke QGIS
2. Buka tool, pilih layer titik
3. Pilih kolom ID (misal `No_Sampel`)
4. Pilih 3 raster di kotak Raster Layers (tahan Ctrl untuk multi-select)
5. Isi nama kustom: `B1,B2,B3,B4,B5,B6,B7,B8,B8A,B11,NDVI,NDWI` (opsional)
6. Centang Sertakan XY
7. Tentukan path CSV output
8. Klik Run

**Output CSV contoh:**
```
No_Sampel, X_coord, Y_coord, B2_Blue, B3_Green, B4_Red, NDVI, NDWI
T001, 108.5231, -6.8821, 0.0612, 0.0891, 0.1203, 0.4521, 0.1832
T002, 108.5291, -6.8756, 0.0534, 0.0762, 0.0983, 0.5102, 0.2211
...
```

---

## Tips
- Jika raster dan titik **CRS-nya berbeda**, tool otomatis melakukan transformasi — tidak perlu reproject manual.
- Untuk raster **multi-band** (Sentinel, Landsat), semua band akan diekstrak sekaligus.
- Nama kolom di shapefile dibatasi **10 karakter** — gunakan CSV untuk nama lengkap.
- Jika nilai titik berada di luar cakupan raster, kolom akan terisi `NULL`.

---

## Syarat
- QGIS 3.16 atau lebih baru
- Python libraries: `gdal`, `numpy` (sudah termasuk dalam instalasi QGIS standar)
