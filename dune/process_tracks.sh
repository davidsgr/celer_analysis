#!/usr/bin/env bash
set -euo pipefail

output="steps.out.txt"
for device in cpu gpu; do
    for mode in track trackslot; do
        for rng in xorwow ranlux; do
            dir="${device}_${mode}_${rng}"

            if [[ ! -d "$dir" ]]; then
                echo "Warning: directory '$dir' does not exist" >&2
                continue
            fi

            # CPU has only i=0; GPU has i=0 through 9.
            if [[ "$device" == "cpu" ]]; then
                indices=(0)
            else
                indices=({0..9})
            fi

            for i in "${indices[@]}"; do
		input="out-${device}.${i}.json"

                if [[ -f "${dir}/run_${i}/${input}" ]]; then
                    jq '.result.counters.steps' "${dir}/run_${i}/${input}" >> "${output}"
                    echo "Wrote ${output}"
                else
                    echo "Warning: ${dir}/run_${i}/${input} does not exist" >&2
                fi
            done
        done
    done
done

