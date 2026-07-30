#!/usr/bin/env bash
#
# Stops and removes all HBntory demo containers.
#
# Usage:
#   ./stop_demo.sh

set -euo pipefail

echo "Stopping all HBntory services..."
docker compose down
echo "Done. Data in the postgres_data volume is preserved for next time."
echo "(Use 'docker compose down -v' instead if you also want to wipe the database.)"
