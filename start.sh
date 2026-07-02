#!/bin/sh
set -e
python ingest.py
exec python web.py
