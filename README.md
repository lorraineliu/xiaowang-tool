# xiaowang-tool
 爱学习的小王小主
## 阿里云（根据时间）更新带宽需求
> 
希望能通过用户AccessKey 调用 在VPS上面部署脚本 之后实现自适应根据时段调节带宽（有点像以前网吧分时段上网计费哈哈）

- 1.每天凌晨1：30带宽自动降低 （比如从100MB 降低到50MB）
- 2.每天早晨8：30带宽自动升高 （比如从50MB提升到200MB）
- 3.每天下午6：30带宽自动降低  （比如从200MB降低到100MB）


我只需要放到ESC里面 暴露三种：1.AccessKey 2.带宽实例ID 3.对应要设置的带宽值 4. region区域

## 使用说明文档
### 安装运行环境
- 安装git获取代码
- 安装pipenv一键部署运行环境
### 定时任务初始化
`(xiaowang-tool) liuchendeMacBook-Pro% crontab -l`

30 1 * * * python common-bandwidth.py modify-bandwidth LTAI4G85dGMX71a2U25QvyBQ ZY3yQKZzXvyA5weIESr7ezaYAhS65q cn-shanghai -i cbwp-uf63jncsq2uxlrv1n11ve -b 50 # 1::30::cbwp-uf63jncsq2uxlrv1n11ve

30 8 * * * python common-bandwidth.py modify-bandwidth LTAI4G85dGMX71a2U25QvyBQ ZY3yQKZzXvyA5weIESr7ezaYAhS65q cn-shanghai -i cbwp-uf63jncsq2uxlrv1n11ve -b 200 # 8::30::cbwp-uf63jncsq2uxlrv1n11ve

30 18 * * * python common-bandwidth.py modify-bandwidth LTAI4G85dGMX71a2U25QvyBQ ZY3yQKZzXvyA5weIESr7ezaYAhS65q cn-shanghai -i cbwp-uf63jncsq2uxlrv1n11ve -b 100 # 18::30::cbwp-uf63jncsq2uxlrv1n11ve

`(xiaowang-tool) liuchendeMacBook-Pro% python cronjob.py --help` 

Usage: cronjob.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  init-common-bandwidth-cronjob   Init common-bandwidth cronjob for...
  remove-common-bandwidth-cronjob
                                  Remove common-bandwidth cronjob from...
  set-common-bandwidth-cronjob    Add common-bandwidth cronjob for...

### 共享带宽脚本更新定时任务里带宽阈值

### 删除定时任务
