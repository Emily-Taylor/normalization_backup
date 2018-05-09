## How to upload Mfr mapping to ES
1. Download from Google sheets as tsv
2.  run the following command:

```cd /home/username/projects/sourcingbot/normalization_service/normalization/mfr
cp ~/Downloads/mfr\ names\ 5.2\ -\ Sheet1.tsv  .
pipenv run python normalize_tsv.py convert_tsv --filename mfr\ names\ 5.2\ -\ Sheet1.tsv --output-filename array.json
pipenv run python uploader-to-es.py create_file --filename array.json --output-filename output.jsonl
```
3. for these commands you will need ES credentials
```
./delete_docs_from_es.sh
./bulk_upload.sh```
```