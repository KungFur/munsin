#!/usr/bin/env bash
set -euo pipefail

function main {
	local pycache_directories=($(find . -type d -name __pycache__))
	if [ ${#pycache_directories[@]} -ne 0 ]; then
		rm -rf ${pycache_directories[@]}
	fi
}

$@
