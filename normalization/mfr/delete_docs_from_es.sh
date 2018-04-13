#!/usr/bin/fish

curl --user elastic -XPOST 'https://ac6a49a0fc0a9f82b7570362557d464b.eu-central-1.aws.cloud.es.io:9243/mfr/_delete_by_query?pretty' -H 'Content-Type: application/json' -d'
{
  "query": { 
    "match_all": {
    }
  }
}
'

