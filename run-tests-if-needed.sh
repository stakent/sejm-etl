#!/bin/sh

find . -type f \( -name "*.py" -o -name "*.html" \) | entr ./run-tests.sh
