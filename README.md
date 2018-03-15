### Installation Instructions
```
git clone https://github.com/sourcingbot/normalization-service/ normalization_service
python3 -m venv env/
source env/bin/activate
pip install -r requirements.txt
python3 setup.py install
```

### Requirements
AWS keys as environment variables or in boto3 config credentials file. The keys are needs access to SQS to fetch incoming json.
See [boto3 manual](http://boto3.readthedocs.io/en/latest/guide/configuration.html)

### Configuration
How to change the URL for the entity service?
 - the URL is defined on the `handlers.py` as `URL`.
How to change the SQS queue?
- it's located at on `routes.py` on on the `SQSRoute` function as the first parameter.

### Running the service
from outside the directory (directory above the repo) run `python -m normalization_service &`
errors will appear in the terminal in which you are running the code. if you push to master, it will be deployed to heroku.
 - logs can be found [here](https://dashboard.heroku.com/apps/normalization-service/logs)
