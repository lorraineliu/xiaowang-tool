#!/usr/bin/env python
from __future__ import print_function
import os
import click
import time
import datetime
from crontab import CronTab


def make_cmd(access_key_id, access_key_secret, region_id, instance_id, bandwidth):
    dir_path = os.path.abspath(os.path.dirname("common-bandwidth.py"))
    path = os.path.join(dir_path, "common-bandwidth.py")
    return 'pipenv run python %s modify-bandwidth %s %s %s -i %s -b %s' % (path, access_key_id, access_key_secret, region_id, instance_id, bandwidth)


def make_comment_times(instance_id):
    now = datetime.datetime.now()
    now_timestamp = time.mktime(now.timetuple())
    time_130 = datetime.datetime(now.year, now.month, now.day, 1, 30)
    time_130_timestamp = time.mktime(time_130.timetuple())
    time_830 = datetime.datetime(now.year, now.month, now.day, 8, 30)
    time_830_timestamp = time.mktime(time_830.timetuple())
    time_1830 = datetime.datetime(now.year, now.month, now.day, 18, 30)
    time_1830_timestamp = time.mktime(time_1830.timetuple())

    if time_130_timestamp <= now_timestamp < time_830_timestamp:
        return '1::30::%s' % instance_id
    elif time_830_timestamp <= now_timestamp < time_1830_timestamp:
        return '8::30::%s' % instance_id
    else:
        return '18::30::%s' % instance_id


def set_cronjob(cmd, comment):
    my_cron = CronTab(user=os.environ.get("LOGNAME"))
    for job in my_cron:
        if job.comment == comment:
            my_cron.remove(job)
            break
    job_new = my_cron.new(
        command=cmd,
        comment=comment)
    times = comment.split("::")
    job_new.setall(int(times[1]), int(times[0]), None, None, None)
    my_cron.write()


@click.group()
def cli():
    pass


@cli.command(help="Init common-bandwidth cronjob for scheduler")
@click.argument('access-key-id')
@click.argument('access-key-secret')
@click.argument('region-id')
@click.option('--instance-id', '-i', prompt='Common Bandwidth Instance ID',
              help='Common Bandwidth Instance ID')
def init_common_bandwidth_cronjob(access_key_id, access_key_secret, region_id, instance_id):
    bandwidths = [50, 200, 100]
    for bandwidth in bandwidths:
        cmd = make_cmd(access_key_id, access_key_secret, region_id, instance_id, bandwidth)
        if bandwidth == 50:
            comment = '1::30::%s' % instance_id
        elif bandwidth == 200:
            comment = '8::30::%s' % instance_id
        else:
            comment = '18::30::%s' % instance_id
        set_cronjob(cmd, comment)
    click.secho('Init Done', fg='blue')


@cli.command(help="Set common-bandwidth cronjob for scheduler")
@click.argument('access-key-id')
@click.argument('access-key-secret')
@click.argument('region-id')
@click.option('--instance-id', '-i', prompt='Common Bandwidth Instance ID',
              help='Common Bandwidth Instance ID')
@click.option('--bandwidth', '-b', prompt='Common Bandwidth Package Bandwidth Value',
              help='Common Bandwidth Package Bandwidth Value')
def set_common_bandwidth_cronjob(access_key_id, access_key_secret, region_id, instance_id, bandwidth):
    cmd = make_cmd(access_key_id, access_key_secret, region_id, instance_id, bandwidth)
    comment = make_comment_times(instance_id)
    set_cronjob(cmd, comment)
    click.secho('Done', fg='blue')


@cli.command(help="Remove common-bandwidth cronjob from scheduler")
def remove_common_bandwidth_cronjob():
    my_cron = CronTab(user=os.environ.get("LOGNAME"))
    my_cron.remove_all()
    my_cron.write()


if __name__ == '__main__':
    cli()
