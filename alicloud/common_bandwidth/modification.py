#!/usr/bin/env python
from aliyunsdkcore.client import AcsClient
from aliyunsdkvpc.request.v20160428.ModifyCommonBandwidthPackageSpecRequest import ModifyCommonBandwidthPackageSpecRequest


def modify_bandwidth(key_id, key_crt, region_id, instance_id, bandwidth="50"):
    client = AcsClient(key_id, key_crt, region_id)  # 'cn-shanghai'
    request = ModifyCommonBandwidthPackageSpecRequest()
    request.set_accept_format('json')

    request.set_BandwidthPackageId(instance_id)  # "cbwp-uf63jncsq2uxlrv1n11ve"
    request.set_Bandwidth(bandwidth)  # "50"

    response = client.do_action_with_exception(request)
    return response
