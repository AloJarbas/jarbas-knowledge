# Shared starter part spec

Topic: `freecad-openscad-cadquery`  
Date: 2026-05-07  
Question: What starter part is simple enough to model in all three tools and revealing enough to compare them fairly?

## Decision

Use a **parameterized two-hole L-bracket** as the shared starter part.

Why this part works:

1. it begins as a constrained 2D sketch,
2. it extrudes cleanly,
3. it needs repeated hole placement,
4. one small revision instantly reveals whether the tool's model remains readable.

This is better than a decorative object and better than a complex watch component at the current stage.

## Part definition

### Core geometry
- rectangular base plate,
- vertical flange at 90 degrees,
- two mounting holes on the base,
- one hole or slot on the flange,
- optional edge fillet only if the tool pass stays clean without it.

### Parameters to expose
- base length,
- base width,
- thickness,
- flange height,
- hole diameter,
- hole spacing,
- edge margin.

## Why it compares the tools honestly

### FreeCAD
The bracket stresses sketch constraints and feature-history edits directly.

### OpenSCAD
The bracket tests whether a readable 2D profile plus extrusion and boolean hole logic stays pleasant or becomes verbose.

### CadQuery
The bracket tests workplane-based feature placement and whether a scripted part family stays clearer than either the GUI or raw constructive-geometry approach.

## Comparison task

After modeling the same part in all three tools, compare only these criteria:

1. how easy the first build felt,
2. how readable the model remained after one dimension change,
3. how cleanly the export path works,
4. how much the model invites reuse instead of one-off completion.

## Recommendation

Do **not** start with a watch part yet.  
Start with the bracket, change one or two dimensions, and record which tool makes revision feel most natural.

## Source basis

- FreeCAD Sketcher Workbench: https://reqrefusion.github.io/FreeCAD-Documentation-html/wiki/Sketcher_Workbench.html
- FreeCAD PartDesign Workbench: https://reqrefusion.github.io/FreeCAD-Documentation-html/wiki/PartDesign_Workbench.html
- OpenSCAD 2D Primitives: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_Primitives
- OpenSCAD 2D to 3D Extrusion: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/2D_to_3D_Extrusion
- CadQuery Workplane: https://cadquery.readthedocs.io/en/latest/workplane.html
