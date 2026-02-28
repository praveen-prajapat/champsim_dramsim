## Compilation Steps

The expected directory structure is:

```
impress_micro2024
|-dramsim3
|-champsim
|-pythia
```

* `git clone https://github.com/praveen-prajapat/champsim_dramsim.git`
* `cd champsim_dramsim/champsim_timecache`

### Build DRAMSim3

* `cd dramsim3`
* `mkdir build && cd build && cmake ..`
* `make -j8`
* `cd ..`

### Setup ChampSim Build Environment

* `cd champsim`
*  `./set_paths.sh`

### Compile One Configuration for Testing

* `./config.py configs/MOP_GS8/baseline.json`
* `make -j8`
* `cd ..`

Ensure that the compilation completes without error. 

**Common Error**: The compiler may not be able to link the dramsim3 library. If so, check that the path is correctly set in `config.py` (search for LDLIBS). 

### Download Traces
```
pythia/traces/
|-602.gcc_s-1850B.champsimtrace.xz
|-603.bwaves_s-2931B.champsimtrace.xz
|- and so-on...
```

### Update LD_LIBARY_PATH

DRAMSim3 is loaded as a dynamically linked library and requires updating `LD_LIBRARY_PATH` variable. We recommend exporting the updated variable to the job-files used to launch experiments.

- Update `LD_LIBRARY_PATH` in current terminal session: `export LD_LIBRARY_PATH=<path-to-dramsim3-directory>:$LD_LIBRARY_PATH`
- Optional (not recommended): Append updated variable to bashrc: `echo "export LD_LIBRARY_PATH=<path-to-dramsim3-directory>:$LD_LIBRARY_PATH" >> ~/.bashrc`

### Test Setup with Dummy Run

* `cd champsim`
* `./test_setup.sh`
