import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASELINE_DIR = "baseline"
TIMECACHE_DIR = "timecache"

TRACES = [
"600.perlbench_s-570B.champsimtrace.xz",
"602.gcc_s-734B.champsimtrace.xz",
"603.bwaves_s-891B.champsimtrace.xz",
"605.mcf_s-472B.champsimtrace.xz",
"607.cactuBSSN_s-2421B.champsimtrace.xz",
"619.lbm_s-2676B.champsimtrace.xz",
"620.omnetpp_s-141B.champsimtrace.xz",
"621.wrf_s-6673B.champsimtrace.xz",
"623.xalancbmk_s-10B.champsimtrace.xz",
"625.x264_s-20B.champsimtrace.xz",
"627.cam4_s-490B.champsimtrace.xz",
"628.pop2_s-17B.champsimtrace.xz",
"649.fotonik3d_s-1176B.champsimtrace.xz",
"654.roms_s-293B.champsimtrace.xz",
"657.xz_s-2302B.champsimtrace.xz",
]

def extract_benchmark(trace):
    return trace.split(".")[1].split("_")[0]

def parse_file(filepath):
    llc_mpki = None
    system_ipc = None

    with open(filepath, "r") as f:
        for line in f:
            if line.startswith("LLC_MPKI"):
                llc_mpki = float(line.split()[1])
            elif line.startswith("SYSTEM_IPC"):
                system_ipc = float(line.split()[1])

    if llc_mpki is None or system_ipc is None:
        raise ValueError(f"Missing data in {filepath}")

    return llc_mpki, system_ipc


rows = []

for trace in TRACES:

    bench = extract_benchmark(trace)
    txt_name = trace.replace(".champsimtrace.xz", "_output.txt")

    base_llc, base_ipc = parse_file(os.path.join(BASELINE_DIR, txt_name))
    time_llc, time_ipc = parse_file(os.path.join(TIMECACHE_DIR, txt_name))

    norm_time = base_ipc / time_ipc

    rows.append({
        "Benchmark": bench,
        "LLC_MPKI_Baseline": base_llc,
        "LLC_MPKI_TimeCache": time_llc,
        "Normalized_Exec_Time": norm_time
    })

df = pd.DataFrame(rows)

print("\n===== RESULTS =====\n")
print(df.to_string(index=False))

df.to_csv("results_exec_time.csv", index=False)

# =====================================================
# 1️⃣ Normalized Execution Time plot
# =====================================================

plt.figure(figsize=(12,5))
plt.bar(df["Benchmark"], df["Normalized_Exec_Time"])
plt.axhline(1.0, linestyle="--")
plt.ylabel("Normalized Execution Time (TimeCache / Baseline)")
plt.xlabel("Benchmark")
plt.title("Normalized Execution Time across SPEC traces")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# =====================================================
# 2️⃣ LLC MPKI grouped bar plot
# =====================================================

x = np.arange(len(df["Benchmark"]))
width = 0.35

plt.figure(figsize=(12,5))

plt.bar(x - width/2, df["LLC_MPKI_Baseline"], width, label="Baseline")
plt.bar(x + width/2, df["LLC_MPKI_TimeCache"], width, label="TimeCache")

plt.xticks(x, df["Benchmark"], rotation=45, ha="right")
plt.ylabel("LLC MPKI")
plt.xlabel("Benchmark")
plt.title("LLC MPKI Comparison (Baseline vs TimeCache)")
plt.legend()
plt.tight_layout()
plt.show()
