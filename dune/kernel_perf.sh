#!/bin/bash

jq '{
  total_time: .result.time.total,
  version: .system.build.version,
  action_time: (.result.time.actions
    | with_entries(select(.key | IN("primary-generate","along-step","optical-boundary-init")))),
  kernels: (.system.kernels
  | map(select(.name | IN("primary-generate","optical-rayleigh", "pre-step")))
    | map({key: .name, value: .})
    | from_entries)
}' out.0.json | tee out.filtered.json
