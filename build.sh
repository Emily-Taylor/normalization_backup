#!/usr/bin/env bash
if [ -n "$1" ]              # Tested variable is quoted.
then
 echo "branch is #1 is $1";  # Need quotes to escape #;
fi 
mkdir -p temp/
cd temp/
aws s3 cp s3://artifacts-1/common-artifacts-$1.tar.gz .
tar -xzvf common-artifacts-$1.tar.gz
if cp mfr-mapping.json  ../normalization/mfr/mfr-mapping.json
  then 
    echo copy successful
else
    exit $?
fi

if cp key-mapping.yml ../key-mapping.yml
  then 
    echo copy successful
else
    exit $?
fi

if cp mpn_mapping.json ../mpn_mapping.json
  then 
    echo copy successful
else
    exit $?
fi

if cp categories.yml ../normalization/categories.yml
  then 
    echo copy successful
else
    exit $?
fi
cd ..
rm -rf temp/




