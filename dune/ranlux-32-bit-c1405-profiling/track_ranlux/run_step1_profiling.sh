CUDA_VISIBLE_DEVICES=1 CELER_ENABLE_PROFILING=1 nsys profile \
    --trace=cuda,nvtx,osrt \
    --osrt-backtrace-stack-size=16384 \
    --backtrace=fp \
    -o dune-zwires-case1 \
    -f true \
    /scratch/gqe/install/make-ranlux-32-bit-c1405-profiling/bin/celer-optical run-gpu.json
