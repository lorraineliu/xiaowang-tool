#!/usr/bin/env python
#coding=utf-8

import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkvpc.request.v20160428.ModifyCommonBandwidthPackageSpecRequest import ModifyCommonBandwidthPackageSpecRequest

client = AcsClient(os.environ['ACCESS_KEY_ID'], os.environ['ACCESS_KEY_SECRET'], 'cn-shanghai')

request = ModifyCommonBandwidthPackageSpecRequest()
request.set_accept_format('json')

request.set_BandwidthPackageId("cbwp-uf63jncsq2uxlrv1n11ve")
request.set_Bandwidth("70")

response = client.do_action_with_exception(request)
# python2: print(response)
print(str(response, encoding='utf-8'))