#!/usr/bin/env bash
set -euo pipefail

function main {
	find . -type d -name __pycache__ -delete
}

$@
