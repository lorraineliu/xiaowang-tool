#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import os
import sys
import click
import time
import datetime
import json
from crontab import CronTab

from alicloud.common_bandwidth import modification


def make_cmd(access_key_id, access_key_secret, region_id, instance_id, bandwidth):
    dir_path = os.path.abspath(os.path.dirname("common-bandwidth.py"))
    path = os.path.join(dir_path, "common-bandwidth.py")
    return 'python %s modify-bandwidth %s %s %s -i %s -b %s >> /var/log/cron.log' % (path, access_key_id, access_key_secret, region_id, instance_id, bandwidth)


def make_common_bandwidth_cmd(access_key_id, access_key_secret, region_id, source_instance_id, target_bandwidth, cmd='transfer-common-bandwidth-eips'):
    dir_path = os.path.abspath(os.path.dirname("common-bandwidth.py"))
    path = os.path.join(dir_path, "common-bandwidth.py")
    return 'python %s %s %s %s %s -s %s -tb %s >> /var/log/cron.log' % (path, cmd, access_key_id, access_key_secret, region_id, source_instance_id, target_bandwidth)


def make_batch_common_bandwidth_cmd(access_key_id, access_key_secret, region_id, bandwidth_setting_dict, cmd='batch-common-bandwidth-transfer'):
    dir_path = os.path.abspath(os.path.dirname("cronjob.py"))
    path = os.path.join(dir_path, "cronjob.py")
    return "python %s %s %s %s %s \'%s\' >> /var/log/cron.log" % (path, cmd, access_key_id, access_key_secret, region_id, bandwidth_setting_dict)


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


def make_comment_times_transfer_common_bandwidth(instance_id):
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
    my_cron = CronTab(user="root")
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


def set_cronjob_by_5min(cmd, comment="transfer-common-bandwidth-packages"):
    my_cron = CronTab(user="root")
    for job in my_cron:
        if job.comment == comment:
            my_cron.remove(job)
            break
    job_new = my_cron.new(
        command=cmd,
        comment=comment
    )
    job_new.minute.every(5)
    my_cron.write()


def choose_bandwidth(bandwidth_setting_dict):
    # 定时时间换算成北京时间，容器默认时区是UTC-格林尼治时区
    now = datetime.datetime.now()
    for k, v in bandwidth_setting_dict.items():
        hour = int(str(k.split('::')[0]))
        minute = int(str(k.split('::')[1]))
        if hour >= 8:
            hour = hour - 8
        else:
            hour = 16 + hour
        if now.hour == hour and now.minute == minute:
            return v
    return None


@click.group()
def cli():
    pass


@cli.command(help="Init common-bandwidth cronjob for scheduler")
@click.argument('access-key-id')
@click.argument('access-key-secret')
@click.argument('region-id')
@click.argument('instance_id')
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


@cli.command(help="Enable common-bandwidth cronjob from scheduler")
def enable_common_bandwidth_cronjob():
    my_cron = CronTab(user=os.environ.get("LOGNAME"))
    if len(my_cron) == 0:
        click.secho("No job!", fg="yellow")
        sys.exit(0)
    for job in my_cron:
        if job.is_enabled():
            job.enable()
            my_cron.write()
            click.secho("enable job!", fg="green")


@cli.command(help="Batch run transfer common-bandwidth")
@click.argument('access-key-id')
@click.argument('access-key-secret')
@click.argument('region-id')
@click.argument('bandwidth-setting-dict')  # '{"8::30": "20", "18::25": "10", "1:20": "5"}'
def batch_common_bandwidth_transfer(access_key_id, access_key_secret, region_id, bandwidth_setting_dict):
    status, instance_list = modification.get_current_common_bandwidth_packages(access_key_id, access_key_secret, region_id)
    if not status:
        os.system('echo `date` >> /var/log/cron.log')
        click.secho('Can not get instance id', fg='red')
        sys.exit(0)
    for instance in instance_list:
        instance_id = instance["BandwidthPackageId"]
        bandwidth_setting_dict = json.loads(bandwidth_setting_dict)
        bandwidth = choose_bandwidth(bandwidth_setting_dict)
        if not bandwidth:
            os.system('echo `date` >> /var/log/cron.log')
            click.secho('No need to transfer', fg='yellow')
            sys.exit(0)
        status = modification.transfer_common_bandwidth_eips(access_key_id, access_key_secret, region_id, instance_id, bandwidth)
        if status:
            os.system('echo `date` >> /var/log/cron.log')
            msg = 'Successfully to transfer from instance_id: %s to bandwidth: %s' % (instance_id, bandwidth)
        click.secho(msg, fg='blue')


@cli.command(help="Init transfer common-bandwidth cronjob")
@click.argument('access-key-id')
@click.argument('access-key-secret')
@click.argument('region-id')
@click.argument('bandwidth-setting-dict')  # '{"8::30": "20", "18::25": "10", "1::20": "5"}'
def init_transfer_common_bandwidth_cronjob(access_key_id, access_key_secret, region_id, bandwidth_setting_dict):
    cmd = make_batch_common_bandwidth_cmd(access_key_id, access_key_secret, region_id, bandwidth_setting_dict)
    set_cronjob_by_5min(cmd)
    click.secho('Done', fg='blue')


if __name__ == '__main__':
    cli()
