---
title: Klipper Tweaks
---

# Klipper Tweaks

Advanced experimental tweaks for Klipper configuration. These settings can **only** be configured via the [Firmware Configuration](firmware_config.md) web interface under **Settings → Tweaks**.

> **Warning**: These are experimental features. Use with caution and monitor your printer carefully after enabling.

## Cancel Individual Objects

Enables the Klipper `[exclude_object]` module so you can cancel individual objects during a multi-object print directly from the Fluidd or Mainsail web interface — without cancelling the entire print.

**What it does:**
- Activates Klipper's built-in exclude_object module
- Adds a per-object cancel button to the Fluidd/Mainsail print status panel
- Requires no Moonraker-side processing (no file upload delay)

**Slicer setup required:**
Your slicer must be configured to label objects in the gcode output. Enable the relevant option before slicing:

| Slicer | Setting location | Option name |
|---|---|---|
| OrcaSlicer | Print Settings → Others | **Label objects** |
| Bambu Studio | Print Settings → Others | **Label objects** |
| PrusaSlicer | Print Settings → Output options | **Label objects** |
| Cura | Marketplace plugin | **Exclude Objects** plugin |

Prints sliced without object labels will still print normally — the cancel buttons simply won't appear.

**Recommendation:**
- **Use this instead of** the "Object Processing for Adaptive Mesh" tweak unless you also need adaptive mesh — this approach has zero upload-time overhead
- Safe to enable permanently; no downside for prints that don't use it

**Configuration:**
This feature can **only** be configured via Firmware Configuration web interface. Manual configuration is not supported.

## TMC AutoTune

Applies optimized stepper motor driver settings for TMC2240 drivers.

**What it does:**
- Optimizes PWM settings for quieter operation
- Configures StallGuard and CoolStep parameters
- Adjusts timing parameters for better heat management
- Fine-tunes driver parameters for improved performance

**Risks:**
- May cause motors to overheat if cooling is insufficient
- Could result in reduced torque or skipped steps under heavy load
- Incorrect settings may affect print quality
- Changes low-level driver parameters that override defaults

**Recommendation:**
- Monitor motor temperatures during first use
- Test with simple prints before production work
- Revert to disabled if you experience issues

**Configuration:**
This feature can **only** be configured via Firmware Configuration web interface. Manual configuration is not supported.

## TMC Reduced Current

Lowers the stepper motor run current from 1.2A to 1.0A for X and Y axes.

**What it does:**
- Reduces X and Y axis motor current to 1.0A
- Lowers motor heat generation
- Results in quieter motor operation

**Risks:**
- May cause skipped steps under heavy load or fast movements
- Could result in layer shifts on demanding prints
- May reduce positioning accuracy under high acceleration

**Recommendation:**
- Monitor print quality after enabling
- Watch for layer shifts or positioning issues
- Disable if you experience motion problems

**Configuration:**
This feature can **only** be configured via Firmware Configuration web interface. Manual configuration is not supported.

## Object Processing for Adaptive Mesh

Enables object processing in Moonraker's file manager to support adaptive mesh features.

**What it does:**
- Processes gcode files to extract object information
- Generates boundaries for adaptive mesh leveling
- Allows per-object print settings and controls

**Risks:**
- Can cause very long processing times for large gcode files (> 100MB)
- May result in extended delays when uploading files
- Snapmaker Orca may stay at 100% for a long time when sending prints
- High memory usage during file processing
- Can cause delays before prints can start

**Important:**
- Enabling this setting alone is not enough to use adaptive mesh
- You must also update your slicer start gcode to use: `BED_MESH_CALIBRATE ADAPTIVE=1`
- This tells Klipper to only mesh the area where objects will be printed

**Recommendation:**
- **Preferred approach:** Enable `Exclude Object` in your slicer settings instead of this option
- Slicer-generated object labels are more reliable and don't require server-side processing
- Only enable Moonraker object processing if your slicer doesn't support exclude object
- Disable if you frequently print large gcode files
- Monitor file upload times after enabling
- Consider splitting large models into smaller prints if processing is too slow

**Configuration:**
This feature can **only** be configured via Firmware Configuration web interface. Manual configuration is not supported.

## How to Configure

1. Open the printer's web interface (Fluidd or Mainsail)
2. Navigate to **Firmware Config** in the menu
3. Go to **Settings → Tweaks**
4. Select the desired option for each tweak
5. Confirm the warning dialog
6. Klipper will automatically restart to apply changes

Changes take effect immediately after Klipper restarts (no reboot required).

## Technical Details

These tweaks work by adding or removing configuration files from `/oem/printer_data/config/extended/`:
- `klipper/exclude_object.cfg` - Cancel Individual Objects (`[exclude_object]`)
- `klipper/tmc_autotune.cfg` - TMC AutoTune parameters
- `klipper/tmc_current.cfg` - Reduced current settings
- `moonraker/object_processing.cfg` - Moonraker object processing settings

These files are automatically included by the main printer configuration if present. Manual editing of these files is not recommended as they will be overwritten by the Firmware Configuration interface.
