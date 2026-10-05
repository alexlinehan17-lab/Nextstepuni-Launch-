import type { CrewId } from './catalogue';

// Each image is centred by its visible bounds, then fitted inside the native
// hex's front/side edges with seven units of breathing room.
export const wonderLayout: Record<CrewId, { size:number; offsetX:number; offsetY:number }> = {
  "luma": {
    "size": 202,
    "offsetX": -106.48,
    "offsetY": -147.68
  },
  "aster": {
    "size": 202,
    "offsetX": -100.76,
    "offsetY": -146.96
  },
  "wisp": {
    "size": 202,
    "offsetX": -105.59,
    "offsetY": -147.44
  },
  "sola": {
    "size": 202,
    "offsetX": -113.08,
    "offsetY": -139.95
  },
  "moss": {
    "size": 202,
    "offsetX": -111.63,
    "offsetY": -158.48
  },
  "tavi": {
    "size": 191.23,
    "offsetX": -98.74,
    "offsetY": -135.34
  },
  "orio": {
    "size": 202,
    "offsetX": -100.84,
    "offsetY": -135.23
  },
  "nori": {
    "size": 202,
    "offsetX": -102.93,
    "offsetY": -153.11
  },
  "pip": {
    "size": 202,
    "offsetX": -102.93,
    "offsetY": -147.42
  },
  "vega": {
    "size": 202,
    "offsetX": -120.65,
    "offsetY": -149.78
  },
  "nyx": {
    "size": 202,
    "offsetX": -104.46,
    "offsetY": -143.53
  },
  "echo": {
    "size": 202,
    "offsetX": -104.38,
    "offsetY": -129.43
  }
};
