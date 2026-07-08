CUDA_VISIBLE_DEVICES=1 TMPDIR=$HOME/tmp/ncu ncu --set full --kernel-name launch_action_impl --replay-mode application --launch-skip 261 --launch-count 1 -o dune-rayleigh-profiling \
/scratch/gqe/install/make-ranlux-32-bit-c1405-profiling/bin/celer-optical run-gpu.json
