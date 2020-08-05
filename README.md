# xiaowang-tool
 爱学习的小王小主
## 需求一：阿里云（根据时间）更新带宽需求
> 
希望能通过用户AccessKey 调用 在VPS上面部署脚本 之后实现自适应根据时段调节带宽（有点像以前网吧分时段上网计费哈哈）

- 1.每天凌晨1：30带宽自动降低 （比如从100MB 降低到50MB）
- 2.每天早晨8：30带宽自动升高 （比如从50MB提升到200MB）
- 3.每天下午6：30带宽自动降低  （比如从200MB降低到100MB）


我只需要放到ESC里面 暴露三种：1.AccessKey 2.带宽实例ID 3.对应要设置的带宽值 4. region区域

### 使用说明文档
#### 安装运行环境
- 安装docker以获取镜像
> 执行以下cmd启动一键式安装<br>
`docker run -d -e access_key_id=LTAI4G85dGMX71a2U25QvyBQ -e access_key_secret=ZY3yQKZzXvyA5weIESr7ezaYAhS65q -e region_id=cn-shanghai -e instance_id=cbwp-uf63jncsq2uxlrv1n11ve gdapenny/xiaowang-tool:v.0.1.0`


#### cronjob脚本介绍
> 本定时任务延用unix的cronjob，通过python-cronjob控制cronjob的生命周期
> 设置好的cronjob可以用以下cmd来查看全部信息

> 运行以下cmd，请先进入container by `docker exec -it container-name bash` <br>

`(xiaowang-tool) liuchendeMacBook-Pro% crontab -l`

30 1 * * * python /Users/liuchen/src/xiaowang-tool/common-bandwidth.py modify-bandwidth LTAI4G85dGMX71a2U25QvyBQ ZY3yQKZzXvyA5weIESr7ezaYAhS65q cn-shanghai -i cbwp-uf63jncsq2uxlrv1n11ve -b 50 # 1::30::cbwp-uf63jncsq2uxlrv1n11ve

30 8 * * * python /Users/liuchen/src/xiaowang-tool/common-bandwidth.py modify-bandwidth LTAI4G85dGMX71a2U25QvyBQ ZY3yQKZzXvyA5weIESr7ezaYAhS65q cn-shanghai -i cbwp-uf63jncsq2uxlrv1n11ve -b 200 # 8::30::cbwp-uf63jncsq2uxlrv1n11ve

30 18 * * *python /Users/liuchen/src/xiaowang-tool/common-bandwidth.py modify-bandwidth LTAI4G85dGMX71a2U25QvyBQ ZY3yQKZzXvyA5weIESr7ezaYAhS65q cn-shanghai -i cbwp-uf63jncsq2uxlrv1n11ve -b 100 # 18::30::cbwp-uf63jncsq2uxlrv1n11ve


> 每条定时任务是一条python脚本执行命令,如下所示

`(xiaowang-tool) liuchendeMacBook-Pro% python common-bandwidth.py modify-bandwidth --help`

Usage: common-bandwidth.py modify-bandwidth [OPTIONS] ACCESS_KEY_ID
                                            ACCESS_KEY_SECRET REGION_ID<br>

  Modify common bandwidth package specific<br>

Options:<br>
  -i, --instance-id TEXT  Common Bandwidth Instance ID<br>
  -b, --bandwidth TEXT    Common Bandwidth Package Bandwidth Value<br>
  --help                  Show this message and exit.<br>


>定时任务管理脚本的使用说明如下：
>目前提供三个命令，init初始化，set更新带宽阈值，以及remove全部的定时任务

`(xiaowang-tool) liuchendeMacBook-Pro% python cronjob.py --help` 

Usage: cronjob.py [OPTIONS] COMMAND [ARGS]...<br>

Options:<br>
  --help  Show this message and exit.<br>

Commands:
  init-common-bandwidth-cronjob   Init common-bandwidth cronjob for...
  
  remove-common-bandwidth-cronjob Remove common-bandwidth cronjob from...
  
  set-common-bandwidth-cronjob    Add common-bandwidth cronjob for...

### 定时任务初始化
>一次性创建3个时段的定时任务，默认值为需求所示

`(xiaowang-tool) liuchendeMacBook-Pro% python cronjob.py init-common-bandwidth-cronjob --help`

Usage: cronjob.py init-common-bandwidth-cronjob [OPTIONS] ACCESS_KEY_ID
                                                ACCESS_KEY_SECRET REGION_ID INSTANCE_ID<br>

  Init common-bandwidth cronjob for scheduler<br>



#### 共享带宽脚本更新定时任务里带宽阈值
> 当要更新某个时段定时任务的带宽阈值，可以使用该命令

`(xiaowang-tool) liuchendeMacBook-Pro% python cronjob.py set-common-bandwidth-cronjob --help`

Usage: cronjob.py set-common-bandwidth-cronjob [OPTIONS] ACCESS_KEY_ID
                                               ACCESS_KEY_SECRET REGION_ID<br>

  Set common-bandwidth cronjob for scheduler<br>

Options: <br>
  -i, --instance-id TEXT  Common Bandwidth Instance ID <br>
  -b, --bandwidth TEXT    Common Bandwidth Package Bandwidth Value <br>
  --help                  Show this message and exit. <br>


#### 删除定时任务
> 清空全部的定时任务

`(xiaowang-tool) liuchendeMacBook-Pro% python cronjob.py remove-common-bandwidth-cronjob --help`

Usage: cronjob.py remove-common-bandwidth-cronjob [OPTIONS]

  Remove common-bandwidth cronjob from scheduler

Options: <br>
  --help  Show this message and exit. <br>

## 需求二：阿里云（根据时间）更替带宽实例
- 通过阿里云SDK实现 在上海区 创建三个共享带宽A和B和C（分别20MB 10MB 5MB 用于测试 后期带宽值可以更改）<br>
- 白天8:30到18:25使用共享带宽A 20Mb（保证在7个多小时 不到8小时 因为切换万一需要时间）
    - 可能出现的坑爹问题EIP解绑后 且已经绑定到A 但是共享带宽C仍然被计费 那么可能需要delete C这个共享带宽 之后在第二天早晨重新创建同等带宽值的共享带宽
- 下午18:25到凌晨1:20使用共享带宽B 10Mb（保证在7个多小时 不到8小时 因为切换万一需要时间）
    - 可能出现的坑爹问题EIP解绑后 且已经绑定到B 但是共享带宽A仍然被计费 那么可能需要delete A这个共享带宽 之后在第二天早晨重新创建同等带宽值的共享带宽
- 凌晨1:20到早晨8:30使用共享带宽C 5Mb （最便宜所以可以超过8小时 因为切换万一需要时间）
    - 可能出现的坑爹问题EIP解绑后 且已经绑定到C 但是共享带宽B仍然被计费 那么可能需要delete B这个共享带宽 之后在第二天早晨重新创建同等带宽值的共享带宽
- Docker容器交付，暴露四种参数以环境变量传参：1.AccessKey 2.region区域 

### 使用说明文档
#### 安装运行环境
- 安装docker以获取镜像
> 执行以下cmd启动一键式安装<br>
`docker run -d -e access_key_id=LTAI4G85dGMX71a2U25QvyBQ -e access_key_secret=ZY3yQKZzXvyA5weIESr7ezaYAhS65q -e region_id=cn-shanghai gdapenny/transfer-common-bandwidth:v.0.1.0`

> 每条定时任务是一条python脚本执行命令,如下所示

`root@5f0dd6e0eb17:/app/src# python common-bandwidth.py transfer-common-bandwidth-eips  --help`

Usage: common-bandwidth.py transfer-common-bandwidth-eips [OPTIONS]
                                                          ACCESS_KEY_ID
                                                          ACCESS_KEY_SECRET
                                                          REGION_ID

  Transfer eips between common bandwidth package

Options:<br>
  -s, --source-instance-id TEXT  Source Common Bandwidth Instance ID<br>
  -tb, --target-bandwidth TEXT   Target Common Bandwidth Instance Bandwidth<br>
  --help                         Show this message and exit.<br>
