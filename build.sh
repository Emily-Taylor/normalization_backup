#!/usr/bin/env bash
if [ -n "$1" ]              # Tested variable is quoted.
then
 echo "branch is #1 is $1";  # Need quotes to escape #;
fi 
mkdir -p temp/
cd temp/
aws s3 cp s3://artifacts-1/common-artifacts-$1.tar.gz .
tar -xzvf common-artifacts-$1.tar.gz
cp array.json  ../normalization/mfr/array.json
cp mapping.yml ../mapping.yml
cp categories.yml ../normalization/categories.yml
cd ..
rm -rf temp/




