var AWS = require("aws-sdk"); // must be npm installed to use
var sns = new AWS.SNS({
  endpoint: "http://127.0.0.1:4002",
  region: "eu-central-1",
});
res = sns.publish({
  Message: "hello!",
  MessageStructure: "json",
  TopicArn: "arn: arn:aws:sns:eu-central-1:202439666482:crawler-new-item",
}, () => {
  console.log("ping");
});
console.log(res);
