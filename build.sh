#!/usr/bin/env bash
mkdir -p temp/
cd temp/
aws s3 cp s3://artifacts-1/common-artifacts.tar.gz .
tar -xzvf common-artifacts.tar.gz
cp array.json  ../normalization/mfr/array.json
cp mapping.yml ../mapping.yml
cp categories.yml ../normalization/mapping.yml
cd ..
rm -rf temp/
