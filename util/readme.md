## Want to test normalization

1. You'll need a data file from the crawler in ndjson format.
2. run this script `python3 batch_test_norm.py process_file --input-filename /home/username/projects/sourcingbot/normalization_service/data/100inductors.ndjson.gz  --output-filename inductors.json.gz`
3. look at the errors message that are printed into the terminal windows. if need, aggregate them using `sort|uniq -c|sort -k1nr`.
