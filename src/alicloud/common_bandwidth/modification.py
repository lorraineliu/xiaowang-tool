#!/usr/bin/env python
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkvpc.request.v20160428.ModifyCommonBandwidthPackageSpecRequest import ModifyCommonBandwidthPackageSpecRequest
from aliyunsdkvpc.request.v20160428.CreateCommonBandwidthPackageRequest import CreateCommonBandwidthPackageRequest
from aliyunsdkvpc.request.v20160428.AddCommonBandwidthPackageIpRequest import AddCommonBandwidthPackageIpRequest
from aliyunsdkvpc.request.v20160428.RemoveCommonBandwidthPackageIpRequest import RemoveCommonBandwidthPackageIpRequest
from aliyunsdkvpc.request.v20160428.DeleteCommonBandwidthPackageRequest import DeleteCommonBandwidthPackageRequest
from aliyunsdkvpc.request.v20160428.DescribeCommonBandwidthPackagesRequest import DescribeCommonBandwidthPackagesRequest


def modify_bandwidth(key_id, key_crt, region_id, instance_id, bandwidth="50"):
    client = AcsClient(key_id, key_crt, region_id)  # 'cn-shanghai'
    request = ModifyCommonBandwidthPackageSpecRequest()
    request.set_accept_format('json')
    request.set_BandwidthPackageId(instance_id)  # "cbwp-uf63jncsq2uxlrv1n11ve"
    request.set_Bandwidth(bandwidth)  # "50"
    response = client.do_action_with_exception(request)
    return response


def create_bandwidth_package(key_id, key_crt, region_id, bandwidth):
    client = AcsClient(key_id, key_crt, region_id)
    request = CreateCommonBandwidthPackageRequest()
    request.set_accept_format('json')
    request.set_Bandwidth(bandwidth)
    request.set_Name("target-%sMbps" % str(bandwidth))
    response = client.do_action_with_exception(request)
    return eval(response).get('BandwidthPackageId', None), response


def add_bandwidth_package_eip(key_id, key_crt, region_id, instance_id, eip_id):
    client = AcsClient(key_id, key_crt, region_id)
    request = AddCommonBandwidthPackageIpRequest()
    request.set_accept_format('json')
    request.set_BandwidthPackageId(instance_id)  # "cbwp-uf6x26z7emiyqfbe2fi0k"
    request.set_IpInstanceId(eip_id)  # "eip-uf63mfnf82x6qb676qt22"
    response = client.do_action_with_exception(request)
    return response


def remove_bandwidth_package_eip(key_id, key_crt, region_id, instance_id, eip_id):
    client = AcsClient(key_id, key_crt, region_id)
    request = RemoveCommonBandwidthPackageIpRequest()
    request.set_accept_format('json')
    request.set_BandwidthPackageId(instance_id)
    request.set_IpInstanceId(eip_id)
    response = client.do_action_with_exception(request)
    return response


def delete_bandwidth_package(key_id, key_crt, region_id, instance_id):
    client = AcsClient(key_id, key_crt, region_id)
    request = DeleteCommonBandwidthPackageRequest()
    request.set_accept_format('json')
    request.set_BandwidthPackageId(instance_id)
    response = client.do_action_with_exception(request)
    return response


def get_common_bandwidth_package_eips(key_id, key_crt, region_id, instance_id):
    client = AcsClient(key_id, key_crt, region_id)
    request = DescribeCommonBandwidthPackagesRequest()
    request.set_accept_format('json')
    request.set_BandwidthPackageId(instance_id)
    response = client.do_action_with_exception(request)
    response = json.loads(response)
    if "RequestId" not in response:
        return False, response
    return True, response["CommonBandwidthPackages"]["CommonBandwidthPackage"][0]["PublicIpAddresses"]["PublicIpAddresse"]

# [{"AllocationId":"eip-uf60emujjhj7uab8zk4ay","IpAddress":"106.14.45.6"},
# {"AllocationId":"eip-uf610adh8kjelhxf9z781","IpAddress":"106.14.18.89"}]
