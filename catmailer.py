#/usr/bin/env python

import datetime
import random
import sys
import time
from subprocess import check_output


def read_facts(facts_file):
    """Reads the facts text file and returns a list of them"""
    facts = []
    with open(facts_file, 'r') as f:
        for line in f:
            facts.append(line.strip())
    return facts


def add_new_subscribers(subs_file, existing_subs):
    """Add any new subscribers in the subscriber text file"""
    with open(subs_file, 'r') as f:
        for line in f:
            number = line.strip()
            if number not in existing_subs:
                existing_subs.add(number)
                log('{0} added to subscribers'.format(number))


def sleep_until(hour):
    """Sleep until a certain hour of the day"""
    time.sleep(1)
    t = datetime.datetime.today()
    future = datetime.datetime(t.year, t.month, t.day, hour, 0)
    if t.hour >= hour:
        future += datetime.timedelta(days=1)
    log('Sleeping until {0}'.format(future))
    time.sleep((future-t).seconds)


def log(msg):
    """Log message with current datetime"""
    print '{0}: {1}'.format(datetime.datetime.now(),
                            msg)


if __name__ == '__main__':
    facts_file = sys.argv[1]
    subs_file = sys.argv[2]

    facts = read_facts(facts_file)
    random.shuffle(facts)

    subs = set([])
    add_new_subscribers(subs_file, subs)

    # Send facts while they exist
    while facts:
        sleep_until(10)
        add_new_subscribers(subs_file, subs)
        fact = facts.pop()
        command = 'echo "{0}" | mail {1}'
        log('Sending "{0}" to subscribers'.format(fact))
        for s in subs:
            check_output(command.format(fact, s),
                         shell=True)
