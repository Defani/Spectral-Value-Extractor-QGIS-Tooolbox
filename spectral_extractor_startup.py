# spectral_extractor_startup.py — Spectral Value Extractor
# Penulis  : Defani Arman Alfitriansyah
# Tanggal  : 09 Juni 2026
# GitHub   : https://github.com/Defani/Spectral-Value-Extractor-QGIS-Tooolbox
#
# ── CARA INSTALL ────────────────────────────────────────────────────────────
# 1. Letakkan file INI di folder python QGIS:
#      Windows : C:\Users\<nama>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\
#      Linux   : ~/.local/share/QGIS/QGIS3/profiles/default/python/
#      Mac     : ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/
#
# 2. Buka (atau buat) file startup.py di folder yang SAMA, lalu tambahkan:
#      import spectral_extractor_startup
#
#    Dengan cara ini tidak akan konflik dengan startup.py milik toolbox lain
#    (contoh: MapBiomas, dsb) karena masing-masing punya file terpisah.
#
# 3. Restart QGIS → tombol "Spectral Extractor" muncul di toolbar.
# ────────────────────────────────────────────────────────────────────────────

from qgis.PyQt.QtCore import QTimer


def _add_spectral_extractor_button():
    from qgis.utils import iface
    from qgis.PyQt.QtWidgets import QAction, QMessageBox
    from qgis.PyQt.QtGui import QIcon, QPixmap, QPainter, QColor
    from qgis.core import QgsApplication

    main_win = iface.mainWindow()

    # Hapus tombol lama jika sudah ada (hindari duplikat saat reload)
    existing = getattr(main_win, '_spectral_extractor_btn', None)
    if existing is not None:
        iface.removeToolBarIcon(existing)
        existing.deleteLater()
        main_win._spectral_extractor_btn = None

    def run_tool():
        reg = QgsApplication.processingRegistry()
        target = None
        for alg in reg.algorithms():
            if 'spectralvalueextractor' in alg.id().lower():
                target = alg.id()
                break
        if target:
            import processing
            processing.execAlgorithmDialog(target)
        else:
            QMessageBox.warning(
                main_win,
                'Spectral Value Extractor',
                'Script tidak ditemukan di Processing Toolbox.\n\n'
                'Pastikan SpectralValueExtractor_script.py\n'
                'sudah ditambahkan ke Processing Toolbox:\n\n'
                'Processing Toolbox\n'
                '  → klik ikon Python (⚙)\n'
                '  → Add Script to Toolbox\n'
                '  → pilih SpectralValueExtractor_script.py\n\n'
                'Kemudian restart QGIS.'
            )

    # Ikon: lingkaran hijau dengan titik sampel putih
    def _make_icon():
        px = QPixmap(24, 24)
        px.fill(QColor(0, 0, 0, 0))
        painter = QPainter(px)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(30, 120, 60))
        painter.setPen(QColor(20, 80, 40))
        painter.drawEllipse(1, 1, 22, 22)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QColor(200, 255, 200))
        painter.drawEllipse(8, 8, 8, 8)
        painter.setBrush(QColor(30, 120, 60))
        painter.setPen(QColor(30, 120, 60))
        painter.drawEllipse(10, 10, 4, 4)
        painter.end()
        return QIcon(px)

    action = QAction(_make_icon(), 'Spectral Extractor', main_win)
    action.setToolTip(
        'Spectral Value Extractor\n'
        'Ekstrak nilai piksel raster pada titik lapangan\n'
        '─────────────────────────────\n'
        'Penulis : Defani Arman Alfitriansyah\n'
        'Tanggal : 09 Juni 2026\n'
        'GitHub  : github.com/Defani'
    )
    action.triggered.connect(run_tool)
    iface.addToolBarIcon(action)
    main_win._spectral_extractor_btn = action


QTimer.singleShot(3000, _add_spectral_extractor_button)
