#!/bin/bash

# -------- Paths --------
cd ../dramsim3
DRAMSIM3_PATH=$(pwd)

cd ../champsim
export LD_LIBRARY_PATH=$DRAMSIM3_PATH:$LD_LIBRARY_PATH

MAX_JOBS=8
cd bin/MOP_GS8

TRACE_DIR="../../../pythia/traces"
OUT_DIR="../../../results"

mkdir -p $OUT_DIR

# -------- Trace list --------
TRACES=(
600.perlbench_s-570B.champsimtrace.xz
602.gcc_s-734B.champsimtrace.xz
603.bwaves_s-891B.champsimtrace.xz
605.mcf_s-472B.champsimtrace.xz
607.cactuBSSN_s-2421B.champsimtrace.xz
619.lbm_s-2676B.champsimtrace.xz
620.omnetpp_s-141B.champsimtrace.xz
621.wrf_s-6673B.champsimtrace.xz
623.xalancbmk_s-10B.champsimtrace.xz
625.x264_s-20B.champsimtrace.xz
627.cam4_s-490B.champsimtrace.xz
628.pop2_s-17B.champsimtrace.xz
649.fotonik3d_s-1176B.champsimtrace.xz
654.roms_s-293B.champsimtrace.xz
657.xz_s-2302B.champsimtrace.xz
)

run_trace() {
    TRACE="$1"
    NAME=$(basename "$TRACE" .champsimtrace.xz)
    OUTPUT_FILE="$OUT_DIR/${NAME}_output.txt"

    echo "Starting $NAME"

    ./baseline \
      --simulation_instruction=10000000 \
      --warmup_instructions=10000000 \
      --cs_traces nnnnnnnn \
      -traces \
      $TRACE_DIR/$TRACE \
      $TRACE_DIR/$TRACE \
      $TRACE_DIR/$TRACE \
      $TRACE_DIR/$TRACE \
      $TRACE_DIR/$TRACE \
      $TRACE_DIR/$TRACE \
      $TRACE_DIR/$TRACE \
      $TRACE_DIR/$TRACE \
      > "$OUTPUT_FILE" 2>&1

    if grep -q "ChampSim completed all CPUs" "$OUTPUT_FILE"; then
        echo "✔ Finished $NAME"
    else
        echo "❌ Error in $NAME"
    fi
}

export -f run_trace

JOB_COUNT=0

for TRACE in "${TRACES[@]}"; do
    run_trace "$TRACE" &

    ((JOB_COUNT++))

    if [[ $JOB_COUNT -ge $MAX_JOBS ]]; then
        wait -n   # wait until one job finishes
        ((JOB_COUNT--))
    fi
done

wait
echo "All parallel simulations completed."
