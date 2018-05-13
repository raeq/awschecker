# AWS Checker #

## Features
1. Checks all the certificates single account for AWS Certificate Transparency Logging enabled, and outputs a warning to the console.

Outputs to std.out when it finds problematic certs.

## Python 3
Works with Python3. 

## Work In progress


## Requirements

* AWS CLI configured with working credentials.
* Various python packages which are listed in a <a href="requirements.txt">requirements.txt</a>

## Example Output

```
2018-05-10T14:37:55Z - INFO - certs.py - (check_certs), line 13 - Begin searching for certificates.
2018-05-10T14:38:05Z - WARNING - certs.py - (check_one_cert), line 39 - Cert https://eu-central-1.console.aws.amazon.com/acm/home?region=eu-central-1#/?id=dcbbd604-3141-40ff-9795-6cf6c8eed382 is not issued (EXPIRED).
2018-05-10T14:38:05Z - WARNING - certs.py - (check_one_cert), line 39 - Cert https://eu-central-1.console.aws.amazon.com/acm/home?region=eu-central-1#/?id=f7afee83-1170-4966-9e1e-aa8a3d1aecb7 is not issued (PENDING_VALIDATION).
2018-05-10T14:38:09Z - WARNING - certs.py - (check_one_cert), line 42 - Cert https://us-east-1.console.aws.amazon.com/acm/home?region=us-east-1#/?id=15d766a5-5297-499a-b505-a20e95f6318d certificate transparency logging is enabled.
2018-05-10T14:38:12Z - INFO - certs.py - (check_certs), line 31 - End searching for certificates.
```

