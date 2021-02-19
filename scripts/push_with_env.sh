#!/usr/bin/env bash

grep -v '^#' .env | sed 's/^/--env /' | xargs balena push "$1"
