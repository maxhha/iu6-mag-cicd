#!/usr/bin/env bash

set -euo pipefail
# set -x

should_show_help=false

NUM_WORKERS=
INPUT_FILE=
LINKS_INDEX=
OUTPUT_FOLDER=
SKIP_HEADER=true
WGET_TIMEOUT=60

while [ $# -gt 0 ]; do
    case "$1" in
        --num_workers ) NUM_WORKERS="$2"; shift 2 ;;
        --input_file ) INPUT_FILE="$2"; shift 2 ;;
        --links_index ) LINKS_INDEX="$2"; shift 2 ;;
        --output_folder ) OUTPUT_FOLDER="$2"; shift 2 ;;
        --timeout | -T ) WGET_TIMEOUT="$2"; shift 2 ;;
        --no_header ) SKIP_HEADER=false; shift ;;
        --help | -h | -\? ) should_show_help=true; shift ;;
        --debug ) set -x; shift ;;
        * ) break ;;
    esac
done

if [ $should_show_help = true ]; then
    echo "run.sh [PARAMS]"
    echo
    echo "Parameters:"
    echo "    --num_workers [NUMBER]"
    echo "    --input_file [PATH]"
    echo "    --links_index [NUMBER]"
    echo "    --output_folder [PATH]"
    echo "    --timeout [NUMBER] (default=60)"
    echo "    --no_header"
    echo
    echo "    --help, -h, -? -- show this help"
    echo
    echo "Made by Alexander Degtyarev (devmaxhha@gmail.com) at sunny sunday"
    echo
    exit 0;
fi



rc=0

if [[ -z "${NUM_WORKERS}" ]]; then
    echo "run.sh: --num_workers required" >&2
    rc=1
fi
if [[ -z "${INPUT_FILE}" ]]; then
    echo "run.sh: --input_file required" >&2
    rc=1
elif [ ! -f "${INPUT_FILE}" ]; then
    echo "run.sh: ${INPUT_FILE}: file is not exist" >&2
    rc=1
fi
if [[ -z "${LINKS_INDEX}" ]]; then
    echo "run.sh: --links_index required" >&2
    rc=1
fi
if [[ -z "${OUTPUT_FOLDER}" ]]; then
    echo "run.sh: --output_folder required" >&2
    rc=1
fi

if [ $rc -ne 0 ]; then
    echo
    echo "Check for usage: run.sh --help"
    exit $rc
fi

mkdir -p "${OUTPUT_FOLDER}"

READ_CMD="cat $INPUT_FILE"

if [ $SKIP_HEADER = true ]; then
    READ_CMD="tail -n +2 $INPUT_FILE"
fi

$READ_CMD | cut -d\; --fields="$LINKS_INDEX" | xargs -t -n 1 --max-procs="$NUM_WORKERS" \
    wget -N -T "${WGET_TIMEOUT}" -P "${OUTPUT_FOLDER}"
