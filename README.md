# python-traffic-generator

code to spam a target url with GET or POST methods, and track the targets HTTP responses, like an AWS ALB while testing a zero-downtime EKS deployment.

configurable with these environment variables and their defaults:

'AWS_REGION', "us-east-2"
'LOG_GROUP', "stress-tester"
'LOG_STREAM', "stress-tester-default"
'METHOD', 1
'TARGET_URL', "https://1.1.1.1"
'PROCESS_COUNT', os.cpu_count()

- For METHOD, 1 will spam GET requests, while 2 will do a POST... with the json payload being a random farm animal.

- PROCESS_COUNT sets how many Python instances to spawn, using multiprocessing. Since its waiting on the network this might have been better built with threading, so TODO.

- In the included ECS task definition, PROCESS_COUNT is set to 100

Right now, this runs well with a 1vcpu 2gb on Fargate, with CPU close to 100% and MEM +50%. 10 tasks can be run before Cloudwatch starts to throttle the logging, which is unhandled and causes the container to crash.

* Finally, in cloudwatch log insights use this query to graph the responses by the target that were not HTTP 200 OK:

fields @timestamp, @message, @logStream, @log
| filter @message not like '200'
