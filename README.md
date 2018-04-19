# Serverless Python based normalization service


## What's needed?
This template includes a few of my favorite things for working with Python &
Serverless:

 *  [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements)
 *  [pipenv](https://docs.pipenv.org)


## Getting started
```
$ # if you don't have them installed, ensure you have serverless & pipenv
$ npm i -g serverless ; pip install pipenv
```
$ # Clone the template using the
```
$ pipenv install
```
To activate this project's virtualenv, run the following:
``` 
$ pipenv shell
```

### Test the sample lambda locally (sls is an included alias for serverless)
```
$ pipenv run sls invoke local -f norm -p data.json
```
$ # Deploy to AWS!
```
$ sls deploy
```
