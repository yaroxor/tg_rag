# Data Exploration for Telegram Chat Export Format

## Purpose
This directory contains exploratory analysis of Telegram's chat export format, as no official specification was available.

## Methods
- Separated messages by type ("service" and "message") to handle their structural differences
- Generated distinct JSON schemas for each message type using genson

## Files
- `generate_json_schema.py` - Schema generation script
- `message_schema.json` - Schema for regular messages

## Notes
Includes initial exploration scripts (`explore.py`, `explore.jq`) and performance comparison results. The preliminary performance test unexpectedly showed JQ processing was slower than Python for this specific workload.
