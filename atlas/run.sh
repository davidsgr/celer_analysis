rm -rf stdout.json stderr exception.json
CELER_LOG=debug CELER_LOG_LOCAL=debug celer-sim run.json 1> stdout.json 2> stderr
jq '.["result"]["exception"]' stdout.json > exception.json
