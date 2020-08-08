#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import click
import json
import os
import sys
import datetime

from alicloud.common_bandwidth import modification


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


@cli.command(help='Modify common bandwidth package specific')
@click.argument('access-key-id')
@click.argument('access-key-secret')
@click.argument('region-id')
@click.option('--instance-id', '-i', prompt='Common Bandwidth Instance ID',
              help='Common Bandwidth Instance ID')
@click.option('--bandwidth', '-b', prompt='Common Bandwidth Package Bandwidth Value',
              help='Common Bandwidth Package Bandwidth Value')
def modify_bandwidth(access_key_id, access_key_secret, region_id, instance_id, bandwidth):
    res = eval(modification.modify_bandwidth(access_key_id, access_key_secret, region_id, instance_id, bandwidth))
    if isinstance(res, dict) and 'RequestId' in res:
        click.secho("Done", fg='blue')
    click.secho(str(res), fg='yellow')


@cli.command(help='Transfer eips between common bandwidth package')
@click.argument('access-key-id')
@click.argument('access-key-secret')
@click.argument('region-id')
@click.option('--source-instance-id', '-s', prompt='Source Common Bandwidth Instance ID',
              help='Source Common Bandwidth Instance ID')
@click.option('--target-bandwidth', '-tb', prompt='Target Common Bandwidth Instance Bandwidth',
              help='Target Common Bandwidth Instance Bandwidth')
def transfer_common_bandwidth_eips(access_key_id, access_key_secret, region_id, source_instance_id, target_bandwidth):

    res = modification.create_bandwidth_package(access_key_id, access_key_secret, region_id, target_bandwidth)
    if not res[0]:
        # TODO：发送告警邮件 with res[1]
        pass
    else:
        target_instance_id = res[0]
        status, res = modification.get_common_bandwidth_package_eips(access_key_id, access_key_secret, region_id, source_instance_id)
        if not status:
            # TODO：发送告警邮件 with res
            pass
        else:
            for eip in res:
                eip_id = eip["AllocationId"]
                res = modification.remove_bandwidth_package_eip(access_key_id, access_key_secret, region_id, source_instance_id, eip_id)
                res = json.loads(res)
                if not (isinstance(res, dict) and 'RequestId' in res):
                    # TODO：发送告警邮件 with res
                    break
                else:
                    res = modification.add_bandwidth_package_eip(access_key_id, access_key_secret, region_id, target_instance_id, eip_id)
                    res = json.loads(res)
                    if not (isinstance(res, dict) and 'RequestId' in res):
                        # TODO：发送告警邮件 with res
                        break
            status, res = modification.get_common_bandwidth_package_eips(access_key_id, access_key_secret, region_id, source_instance_id)
            if status and len(res) == 0:
                res = modification.delete_bandwidth_package(access_key_id, access_key_secret, region_id, source_instance_id)
                res = json.loads(res)
                if not (isinstance(res, dict) and 'RequestId' in res):
                    # TODO：发送告警邮件 with res
                    pass
                else:
                    click.secho("Done", fg='blue')


@cli.command(help="Batch run transfer common-bandwidth")
@click.argument('access-key-id')
@click.argument('access-key-secret')
@click.argument('region-id')
@click.argument('bandwidth-setting-dict')  # '{"8::30": "20", "18::25": "10", "1:20": "5"}'
def batch_common_bandwidth_transfer(access_key_id, access_key_secret, region_id, bandwidth_setting_dict):
    os.system('echo Start to run at `date` >> /var/log/cron.log')
    status, instance_list = modification.get_current_common_bandwidth_packages(access_key_id, access_key_secret, region_id)
    if not status:
        os.system('echo Can not get instance id at `date` >> /var/log/cron.log')
        click.secho('Can not get instance id', fg='red')
        sys.exit(0)
    bandwidth_setting_dict = json.loads(bandwidth_setting_dict)
    bandwidth = choose_bandwidth(bandwidth_setting_dict)
    for instance in instance_list:
        instance_id = instance["BandwidthPackageId"]
        if not bandwidth:
            os.system('echo No need to transfer at `date` >> /var/log/cron.log')
            click.secho('No need to transfer', fg='red')
            sys.exit(0)
        res = modification.create_bandwidth_package(access_key_id, access_key_secret, region_id, bandwidth)
        if not res[0]:
            os.system('echo Fail to create target common bandwidth instance at `date` >> /var/log/cron.log')
            click.secho('No need to transfer', fg='red')
            sys.exit(0)
        status, res = modification.transfer_common_bandwidth_eips(access_key_id, access_key_secret, region_id, instance_id, res[0])
        if status:
            os.system('echo Successfully to transfer common-bandwidth at `date` >> /var/log/cron.log')
            msg = 'Successfully to transfer from instance_id: %s to bandwidth: %s' % (instance_id, bandwidth)
            click.secho(msg, fg='blue')
        else:
            os.system('echo Fail to transfer common-bandwidth at `date` >> /var/log/cron.log')
            msg = res
            click.secho(msg, fg='red')


if __name__ == '__main__':
    cli()
