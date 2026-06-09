# -*- coding: utf-8 -*-
"""
SpectralValueExtractor_script.py — Spectral Value Extractor
Author   : Defani Arman Alfitriansyah
Date     : June 09, 2026
Version  : 1.0.0
GitHub   : https://github.com/Defani/Spectral-Value-Extractor-QGIS-Tooolbox
Compatible: QGIS 3.x (Processing Script — class-based)
"""

__author__  = "Defani Arman Alfitriansyah"
__date__    = "2026-06-09"
__version__ = "1.0.0"

import os
import csv

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterField,
    QgsProcessingParameterString,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterFeatureSink,
    QgsWkbTypes,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsFeatureSink,
    QgsCoordinateTransform,
    QgsProject,
    QgsProcessingException,
)


class SpectralValueExtractorAlgorithm(QgsProcessingAlgorithm):

    POINT_LAYER   = "POINT_LAYER"
    ID_FIELD      = "ID_FIELD"
    RASTER_LAYERS = "RASTER_LAYERS"
    BAND_NAMES    = "BAND_NAMES"
    ADD_XY        = "ADD_XY"
    OUTPUT_CSV    = "OUTPUT_CSV"
    OUTPUT_LAYER  = "OUTPUT_LAYER"

    def name(self):
        return "spectralvalueextractor"

    def displayName(self):
        return "Spectral Value Extractor"

    def group(self):
        return "Remote Sensing Tools"

    def groupId(self):
        return "remotesensingtools"

    def shortHelpString(self):
        return (
            "<b>Spectral Value Extractor</b><br>"
            "<i>Author: Defani Arman Alfitriansyah &nbsp;|&nbsp; June 09, 2026</i><br><br>"
            "Extracts raster pixel values (multi-band / vegetation indices) "
            "at field sample point locations.<br><br>"
            "<u>Inputs:</u><br>"
            "• <b>Field Sample Points</b> – point vector layer<br>"
            "• <b>Point ID Field</b> – unique identifier column for each point<br>"
            "• <b>Raster Layers</b> – one or more raster / index layers<br>"
            "• <b>Custom Band Names</b> – optional, comma-separated<br>"
            "• <b>Include XY Coordinates</b> – add X and Y columns to output<br><br>"
            "<u>Outputs:</u><br>"
            "• <b>CSV file</b> containing spectral values per point<br>"
            "• <b>New point layer</b> with spectral values as attributes"
        )

    def createInstance(self):
        return SpectralValueExtractorAlgorithm()

    def tr(self, string):
        return QCoreApplication.translate("SpectralValueExtractor", string)

    def initAlgorithm(self, config=None):

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.POINT_LAYER,
                self.tr("Field Sample Points"),
                [QgsProcessing.TypeVectorPoint],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.ID_FIELD,
                self.tr("Point ID / Label Field"),
                parentLayerParameterName=self.POINT_LAYER,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.RASTER_LAYERS,
                self.tr("Raster / Spectral Index Layers (multiple allowed)"),
                QgsProcessing.TypeRaster,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.BAND_NAMES,
                self.tr(
                    "Custom Band Names (optional, comma-separated)\n"
                    "Example: B2_Blue,B3_Green,B4_Red,NDVI"
                ),
                optional=True,
                multiLine=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ADD_XY,
                self.tr("Include X and Y Coordinate Columns"),
                defaultValue=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_CSV,
                self.tr("Save Output as CSV"),
                fileFilter="CSV Files (*.csv)",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT_LAYER,
                self.tr("Output Layer (with spectral values)"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        point_layer    = self.parameterAsVectorLayer(parameters, self.POINT_LAYER, context)
        id_field       = self.parameterAsString(parameters, self.ID_FIELD, context)
        raster_layers  = self.parameterAsLayerList(parameters, self.RASTER_LAYERS, context)
        band_names_raw = self.parameterAsString(parameters, self.BAND_NAMES, context)
        add_xy         = self.parameterAsBoolean(parameters, self.ADD_XY, context)
        output_csv     = self.parameterAsFileOutput(parameters, self.OUTPUT_CSV, context)

        if not point_layer:
            raise QgsProcessingException("Field sample point layer not found.")
        if not raster_layers:
            raise QgsProcessingException("At least one raster layer must be selected.")

        # Build band list
        custom_names = []
        if band_names_raw and band_names_raw.strip():
            custom_names = [n.strip() for n in band_names_raw.split(",") if n.strip()]

        band_info  = []
        custom_idx = 0

        for rl in raster_layers:
            file_name  = os.path.splitext(os.path.basename(rl.source()))[0]
            band_count = rl.bandCount()
            for b in range(1, band_count + 1):
                if custom_idx < len(custom_names):
                    col = custom_names[custom_idx][:10]
                    custom_idx += 1
                else:
                    if band_count == 1:
                        col = file_name[:10]
                    else:
                        label = rl.bandName(b) if rl.bandName(b) else f"Band{b}"
                        col = f"{file_name[:6]}_{label}"[:10]
                band_info.append({"rl": rl, "band": b, "col": col})

        feedback.pushInfo(f"Total spectral columns to extract: {len(band_info)}")
        for bi in band_info:
            feedback.pushInfo(f"  → {bi['col']}  (band {bi['band']} from {bi['rl'].name()})")

        # Build output fields
        out_fields = QgsFields()
        for f in point_layer.fields():
            out_fields.append(f)
        if add_xy:
            out_fields.append(QgsField("X_Coord", QVariant.Double, "double", 20, 8))
            out_fields.append(QgsField("Y_Coord", QVariant.Double, "double", 20, 8))
        for bi in band_info:
            out_fields.append(QgsField(bi["col"], QVariant.Double, "double", 20, 8))

        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT_LAYER, context,
            out_fields, QgsWkbTypes.Point,
            point_layer.sourceCrs(),
        )

        # CRS transformation per raster
        pt_crs     = point_layer.sourceCrs()
        transforms = {}
        for rl in raster_layers:
            if pt_crs != rl.crs():
                transforms[rl.id()] = QgsCoordinateTransform(
                    pt_crs, rl.crs(), QgsProject.instance()
                )
            else:
                transforms[rl.id()] = None

        # Iterate over points
        features = list(point_layer.getFeatures())
        total    = len(features)
        rows_csv = []

        for i, feat in enumerate(features):
            if feedback.isCanceled():
                break
            feedback.setProgress(int(i / total * 100))

            geom = feat.geometry()
            if not geom or geom.isEmpty():
                feedback.pushWarning(f"Feature ID {feat.id()} has no geometry, skipped.")
                continue

            pt = geom.asPoint()

            out_feat = QgsFeature(out_fields)
            out_feat.setGeometry(feat.geometry())
            for f in point_layer.fields():
                out_feat.setAttribute(f.name(), feat[f.name()])

            row = {}
            if id_field and id_field in [f.name() for f in point_layer.fields()]:
                row["__id__"] = feat[id_field]
            else:
                row["__id__"] = feat.id()

            if add_xy:
                out_feat.setAttribute("X_Coord", pt.x())
                out_feat.setAttribute("Y_Coord", pt.y())
                row["X_Coord"] = pt.x()
                row["Y_Coord"] = pt.y()

            for bi in band_info:
                rl   = bi["rl"]
                tr   = transforms[rl.id()]
                pt_t = tr.transform(pt) if tr else pt
                val, ok = rl.dataProvider().sample(pt_t, bi["band"])
                v = round(val, 6) if ok else None
                out_feat.setAttribute(bi["col"], v)
                row[bi["col"]] = v

            sink.addFeature(out_feat, QgsFeatureSink.FastInsert)
            rows_csv.append(row)

        # Write CSV
        csv_result = None
        if output_csv and rows_csv:
            try:
                header      = list(rows_csv[0].keys())
                disp_header = [id_field if h == "__id__" else h for h in header]
                with open(output_csv, "w", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    w.writerow(disp_header)
                    for r in rows_csv:
                        w.writerow([r[h] for h in header])
                csv_result = output_csv
                feedback.pushInfo(f"✔ CSV saved to: {output_csv}")
            except Exception as e:
                feedback.pushWarning(f"Failed to save CSV: {e}")

        feedback.pushInfo(
            f"✔ Done! {len(rows_csv)} points processed, "
            f"{len(band_info)} spectral values extracted per point."
        )
        return {self.OUTPUT_LAYER: dest_id, self.OUTPUT_CSV: csv_result}
