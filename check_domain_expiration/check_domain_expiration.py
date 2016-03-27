#!/usr/bin/env python

import datetime
import whois
import argparse
import sys


def get_params():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-domain', action='store',
                        dest='domain_name',
                        help='Domain Name',
                        required=True)

    parser.add_argument('-w', action='store',
                        dest='warning_days',
                        help='Days for warning alert',
                        type=int,
                        default='14')

    parser.add_argument('-c', action='store',
                        dest='critical_days',
                        help='Days for critical alert',
                        type=int,
                        default='3')

    return parser.parse_args()


def get_days_till_exp(domain_name):
    try:
        domain = whois.whois(domain_name)
    except:
        return {'status': 'failure', 'output': 'unable to retrieve information for %s' % domain_name}

    if not 'expiration_date' in domain.keys():
        return {'status': 'failure', 'output': 'no expiration_date info for %s' % domain_name}

    if type(domain['expiration_date']) is datetime.datetime:
        days_delta = (domain['expiration_date'] - datetime.datetime.now()).days

    elif type(domain['expiration_date']) is list:
        days_delta = (domain['expiration_date'][0] - datetime.datetime.now()).days

    else:
        return {'status': 'failure', 'output': 'unknown expiration_date record type for %s' % domain_name}

    return {'status': 'success', 'output': days_delta}


def main():
    args = get_params()
    if args.warning_days < args.critical_days:
        print "CRITICAL value should be bigger than WARNING"
        sys.exit(2)

    result = get_days_till_exp(args.domain_name)

    if result['status'] is 'failure':
        print result['output']
        sys.exit(2)

    elif result['status'] is 'success':
        if result['output'] <= args.critical_days:
            print "Domain %s CRITICAL: will expire in %s days" % (args.domain_name, result['output'])
            sys.exit(2)
        elif result['output'] <= args.warning_days:
            print "Domain %s WARNING: will expire in %s days" % (args.domain_name, result['output'])
            sys.exit(1)
        else:
            print "Domain %s OK: will expire in %s days" % (args.domain_name, result['output'])
            sys.exit(0)


if __name__ == "__main__":
    main()
