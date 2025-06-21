#!/bin/sh

# print empty lines to mark start of new checks run
echo ""
echo ""
echo ""
echo "********************************************************"
echo ""

PYTHONPATH=. pytest
