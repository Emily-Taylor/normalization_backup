#!/usr/bin/env bash
set branch = $argv[1]
mkdir -p temp/
cd temp/
aws s3 cp s3://artifacts-1/common-artifacts-$branch.tar.gz .
tar -xzvf common-artifacts-$branch.tar.gz
cp array.json  ../normalization/mfr/array.json
cp mapping.yml ../mapping.yml
cp categories.yml ../normalization/mapping.yml
cd ..
rm -rf temp/
