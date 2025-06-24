#!/bin/sh

parentdir="$(dirname `pwd`)"

number_of_years_to_process=1 \
cache_base_dir_prefix="${parentdir}/cache" \
python sejm_etl.py