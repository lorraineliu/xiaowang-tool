#!/usr/bin/env python
from __future__ import print_function
import click

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
        click.secho("Done", fg='green')
    else:
        click.secho(res, fg='red')


if __name__ == '__main__':
    cli()
