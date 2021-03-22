#!/usr/bin/env bash

grep -v -E '^#|^[[:space:]]*$' .env/lan | sed 's/^/--env /' | xargs balena push "$1"
