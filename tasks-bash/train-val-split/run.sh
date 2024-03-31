#!/usr/bin/env bash

set -euo pipefail
# set -x

should_show_help=false

INPUT=
TRAIN_RATIO=
SHUFFLE=false
TRAIN_FILE=
VAL_FILE=
READ_HEADER=true

while [ $# -gt 0 ]; do
    case "$1" in
        --input ) INPUT="$2"; shift 2 ;;
        --train_ratio ) TRAIN_RATIO="$2"; shift 2 ;;
        --shuffle ) SHUFFLE=true; shift ;;
        --train_file ) TRAIN_FILE="$2"; shift 2 ;;
        --val_file ) VAL_FILE="$2"; shift 2 ;;
        --no_header ) READ_HEADER=false; shift ;;
        --help | -h | -\? ) should_show_help=true; shift ;;
        --debug ) set -x; shift ;;
        * ) break ;;
    esac
done

if [ $should_show_help = true ]; then
    echo "run.sh [PARAMS]"
    echo
    echo "Parameters:"
    echo "    --input [PATH]"
    echo "    --train_ratio [PERCENT]"
    echo "    --shuffle"
    echo "    --train_file [PATH]"
    echo "    --val_file [PATH]"
    echo "    --no_header"
    echo
    echo "    --help, -h, -? -- show this help"
    echo
    echo "Made by Alexander Degtyarev (devmaxhha@gmail.com) at sunny sunday"
    echo
    exit 0;
fi



rc=0

if [[ -z "${INPUT}" ]]; then
    echo "run.sh: --input required" >&2
    rc=1
fi
if [ ! -f "${INPUT}" ]; then
    echo "run.sh: ${INPUT}: file is not exist" >&2
    rc=1
fi
if [[ -z "${TRAIN_RATIO}" ]]; then
    echo "run.sh: --train_ratio required" >&2
    rc=1
fi
if [[ -z "${TRAIN_FILE}" ]]; then
    echo "run.sh: --train_file required" >&2
    rc=1
fi
if [[ -z "${VAL_FILE}" ]]; then
    echo "run.sh: --val_file required" >&2
    rc=1
fi
if [[ "${TRAIN_FILE}" = "${VAL_FILE}" ]]; then
    echo "run.sh: --train_file and --val_file must be different" >&2
    rc=1
fi

if [ $rc -ne 0 ]; then
    echo
    echo "Check for usage: run.sh --help"
    exit $rc
fi

TMP_TRAIN_FILE="${TRAIN_FILE}.tmp#$$"
TMP_VAL_FILE="${VAL_FILE}.tmp#$$"

HEADER=

TOTAL_LINES=$(wc -l < "$INPUT")
if [ $READ_HEADER = true ]; then
    TOTAL_LINES=$((TOTAL_LINES - 1))
    HEADER=$(head -n 1 "$INPUT")
fi
TRAIN_LINES=$((TOTAL_LINES * TRAIN_RATIO / 100))

if [ -z "$HEADER" ]; then
    :> "${TMP_TRAIN_FILE}"
    :> "${TMP_VAL_FILE}"
else
    echo "$HEADER" > "${TMP_TRAIN_FILE}"
    echo "$HEADER" > "${TMP_VAL_FILE}"
fi

CURRENT_TRAIN_LINE_I=0

READ_CMD="cat $INPUT"

if [ $READ_HEADER = true ]; then
    READ_CMD="tail -n +2 $INPUT"
fi

if [ $SHUFFLE = true ]; then
    READ_CMD="$READ_CMD | shuf"
fi

eval "$READ_CMD" | while IFS= read -r line
do
    if [ $CURRENT_TRAIN_LINE_I -lt $TRAIN_LINES ]; then
        echo "${line}" >> "$TMP_TRAIN_FILE"
        CURRENT_TRAIN_LINE_I=$((CURRENT_TRAIN_LINE_I+1))
    else
        echo "${line}" >> "$TMP_VAL_FILE"
    fi
done

mv "$TMP_TRAIN_FILE" "$TRAIN_FILE"
mv "$TMP_VAL_FILE" "$VAL_FILE"
