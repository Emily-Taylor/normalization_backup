#!/usr/bin/env bash
git clone git@github.com:sourcingbot/common.git temp
cp temp/array.json  normalization/mfr/array.json
cp temp/mapping.yml mapping.yml
cp temp/categories.yml  normalization/mapping.yml
rm -rf temp/
