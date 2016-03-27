# check_domain_expiration Nagios plugin

A plugin to check domain expiration fact. 

## Requirements

* python 2x
* python-whois
```
    pip install python-whois
```

## Important
Don't forget about whois-service requests limit. Its really enough to run plugin once a day per domain. Otherwise you may be banned.