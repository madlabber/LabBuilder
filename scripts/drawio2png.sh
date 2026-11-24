#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $(basename "$0") <input.drawio> [output_dir]" >&2
  exit 1
fi

INPUT_FILE="$1"

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "Error: File not found: $INPUT_FILE" >&2
  exit 1
fi

# Default output folder to the input file's directory if not provided
OUT_DIR="${2:-$(dirname "$INPUT_FILE")}"
mkdir -p "$OUT_DIR"

# Strip directory and .drawio extension for the output filename
BASENAME="$(basename "${INPUT_FILE%.drawio}")"
OUTPUT_FILE="${OUT_DIR%/}/${BASENAME}.png"

xvfb-run -a drawio -x -f png -o "$OUTPUT_FILE" "$INPUT_FILE" --no-sandbox
echo "Exported: $OUTPUT_FILE"
