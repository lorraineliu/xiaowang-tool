#!/usr/bin/env python
# coding=utf-8
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
    request.set_Name("target-%sMbps" % (str(bandwidth)))
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


def get_current_common_bandwidth_packages(key_id, key_crt, region_id):
    client = AcsClient(key_id, key_crt, region_id)
    request = DescribeCommonBandwidthPackagesRequest()
    request.set_accept_format('json')
    response = client.do_action_with_exception(request)
    response = json.loads(response)
    if "RequestId" not in response:
        return False, response
    return True, response["CommonBandwidthPackages"]["CommonBandwidthPackage"]

# [{"Status":"Available","Description":"","ResourceGroupId":"rg-acfns72zfysjtdq","InstanceChargeType":"PostPaid","ISP":"BGP","HasReservationData":false,"DeletionProtection":false,"BusinessStatus":"Normal","Name":"target-10Mbps","InternetChargeType":"PayByBandwidth","Bandwidth":"10","ExpiredTime":"","CreationTime":"2020-08-05T15:10:06Z","BandwidthPackageId":"cbwp-uf65bg3d0kn2g42cqgyql","PublicIpAddresses":{"PublicIpAddresse":[{"AllocationId":"eip-uf60emujjhj7uab8zk4ay","IpAddress":"106.14.45.6"},{"AllocationId":"eip-uf60ud51x5vbtpimc62w8","IpAddress":"101.132.108.79"},{"AllocationId":"eip-uf610adh8kjelhxf9z781","IpAddress":"106.14.18.89"},{"AllocationId":"eip-uf63mfnf82x6qb676qt22","IpAddress":"101.132.151.157"}]},"Ratio":100,"RegionId":"cn-shanghai"}]


def transfer_common_bandwidth_eips(access_key_id, access_key_secret, region_id, source_instance_id, target_instance_id):
    status, res = get_common_bandwidth_package_eips(access_key_id, access_key_secret, region_id, source_instance_id)
    if not status:
        # TODO：发送告警邮件 with res
        return False, res
    else:
        for eip in res:
            eip_id = eip["AllocationId"]
            res = remove_bandwidth_package_eip(access_key_id, access_key_secret, region_id, source_instance_id, eip_id)
            res = json.loads(res)
            if not (isinstance(res, dict) and 'RequestId' in res):
                # TODO：发送告警邮件 with res
                return False, res
            else:
                res = add_bandwidth_package_eip(access_key_id, access_key_secret, region_id, target_instance_id, eip_id)
                res = json.loads(res)
                if not (isinstance(res, dict) and 'RequestId' in res):
                    # TODO：发送告警邮件 with res
                    return False, res
        status, res = get_common_bandwidth_package_eips(access_key_id, access_key_secret, region_id, source_instance_id)
        if status and len(res) == 0:
            res = delete_bandwidth_package(access_key_id, access_key_secret, region_id, source_instance_id)
            res = json.loads(res)
            if not (isinstance(res, dict) and 'RequestId' in res):
                # TODO：发送告警邮件 with res
                return False, res
            else:
                return True, "OK"
