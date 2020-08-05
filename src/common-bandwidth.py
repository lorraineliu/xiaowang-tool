#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function
import click
import json

from alicloud.common_bandwidth import modification


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


if __name__ == '__main__':
    cli()
