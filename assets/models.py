# coding:utf-8

from django.db import models
#from accounts.models import UserProfile

# Create your models here.
class Organization(models.Model):
    name = models.CharField(u'名称', max_length=50)
    code = models.CharField(u'编码', max_length=50)
    status_choices = (
        (0, '非活动'),
        (1, '活动')
    )
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='状态') 
    parent_id = models.IntegerField()
    parent_id_left =  models.IntegerField()
    parent_id_right = models.IntegerField()
    deliverymodel_id = models.IntegerField()
    obsolescence_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = u'-拥有者组织'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
        #return '<id:%s name:%s>' % (self.id, self.name)

class Location(models.Model):
    name = models.CharField(u'名称', max_length=50)
    status_choices = (
        (0, '非活动'),
        (1, '活动')
    )
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='状态')
    organization = models.ForeignKey(Organization, verbose_name=u'拥有者组织')

    class Meta:
        verbose_name = u'-位置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
        #return '<id:%s name:%s>' % (self.id, self.name)

class Rack(models.Model):
    name = models.CharField(u'名称', max_length=50)
    status_choices = (
        (0, '非活动'),
        (1, '活动')
    )
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='状态')
    organization = models.ForeignKey(Organization, verbose_name=u'拥有者组织')
    location = models.ForeignKey(Location, verbose_name=u'位置')
    #brand = models.ForeignKey(Location, verbose_name=u'商标')
    #model = models.ForeignKey(型号, verbose_name=u'Model')
    numberUnit = models.IntegerField(null=True, blank=True, verbose_name='容量')
    serialNumber = models.CharField(u'产品编号', max_length=128, unique=True, default=0)
    assetNumber = models.CharField(u'资产编号', max_length=128, unique=True, default=0)
    createDate = models.DateField(u'安装日期', null=True, blank=True)
    purchaseDate = models.DateField(u'购买时间', null=True, blank=True)
    expireData = models.DateField(u'过保修期', null=True, blank=True)

    class Meta:
        verbose_name = u'-机柜'
        verbose_name_plural = verbose_name

    def __str__(self):
        #return '<id:%s name:%s>' % (self.id, self.name)
        return self.id, self.name


class Enclosure(models.Model):
    name = models.CharField(u'名称', max_length=50)
    rack = models.ForeignKey(Rack, verbose_name=u'机柜')
    status_choices = (
        (0, '非活动'),
        (1, '活动')
    )
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='状态')
    #organization = models.ForeignKey(Organization, verbose_name=u'拥有者组织')
    location = models.ForeignKey(Location, verbose_name=u'位置')
    #brand = models.ForeignKey(Location, verbose_name=u'商标')
    #model = models.ForeignKey(型号, verbose_name=u'Model')
    numberUnit = models.IntegerField(null=True, blank=True, verbose_name='容量')
    #serialNumber = models.CharField(u'产品编号', max_length=128, unique=True, default=0)
    #assetNumber = models.CharField(u'资产编号', max_length=128, unique=True, default=0)
    #createDate = models.DateField(u'安装日期', null=True, blank=True)
    #purchaseDate = models.DateField(u'购买时间', null=True, blank=True)
    #expireData = models.DateField(u'过保修期', null=True, blank=True)

    class Meta:
        verbose_name = u'-机柜内位置'
        verbose_name_plural = verbose_name

    def __str__(self):
        #return '<id:%s name:%s>' % (self.id, self.name)
        return self.id, self.name


class Cinema(models.Model):
    cinemaName = models.CharField(u'影城名称', max_length=50)
    #cinemaAddress = models.CharField(u'影城地址', max_length=120, null=True, blank=True)
    city = models.CharField(u'城市', max_length=10)
    province = models.CharField(u'省份', max_length=18)
    #country = models.CharField(u'国家', max_length=12, default='中国')
    cinemaCode = models.CharField(u'影城编码', max_length=8, null=True, blank=True)
    serviceIp = models.GenericIPAddressField(u'业务 IP', blank=True, null=True)
    projectionIp = models.GenericIPAddressField(u'放映 IP', blank=True, null=True)
    officeIp = models.GenericIPAddressField(u'办公 IP', blank=True, null=True)
    openDate = models.DateField(u'开业时间', null=True, blank=True)
    cinema_type_choices = (
        ('wanda', u'广场店'),
        ('acquisition', u'收购店'),
        ('unwanda', u'非万店'),
        ('others', u'其他'),
    )
    cinema_type = models.CharField(u'影城类型',choices=cinema_type_choices, max_length=12, default='广场店')
    cinema_status_choices = (
        ('new', u'新建影城'),
        ('openup', u'营业'),
        ('closedown', u'停业'),
        ('others', u'其他'),
    )
    cinema_status = models.CharField(u'影城状态',choices=cinema_status_choices, max_length=12, default='新建影城')
    service_level_choices = (
        ('all', u'全面服务'),
        ('part', u'部分'),
        ('pause', u'暂停'),
        ('others', u'其他'),
    )
    service_level = models.CharField(u'服务级别',choices=service_level_choices, max_length=12, default='全面服务')
    virtualization_choices = (
        ('all', u'虚拟化'),
        ('part', u'TMS虚拟化'),
        ('pause', u'未虚拟化'),
    )
    virtualization = models.CharField(u'虚拟化',choices=virtualization_choices, max_length=10, default='虚拟化')
    comment = models.TextField(u'备注', null=True, blank=True)

    #This for Django 1.6.11
    #def __unicode__(self):
    #  return self.cinemaName
    class Meta:
        verbose_name = u'-影城'
        verbose_name_plural = verbose_name

    def __str__(self):
        #return '<id:%s name:%s>' % (self.id, self.cinemaName)
        return self.cinemaName

class Brand(models.Model):
    brandName = models.CharField(u'厂商', max_length=30)
    brandTelephone = models.CharField(u'联系电话', max_length=11, null=True, blank=True)
    brandEmail = models.EmailField(u'E-Mail', null=True, blank=True)

    def __str__(self):
      return self.brandName
    class Meta:
        verbose_name = u'-厂商'
        verbose_name_plural = verbose_name

class Model(models.Model):
    brand = models.ForeignKey(Brand)
    modelName = models.CharField(u'类号', max_length=30)

    def __str__(self):
      return self.modelName
    class Meta:
        verbose_name = u'-设备类号'
        verbose_name_plural = verbose_name

class CPU(models.Model):
    name = models.CharField(u'名称', max_length=128, blank=True)

    class Meta:
        verbose_name = '-CPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OSFamlily(models.Model):
    name = models.CharField(u'操作系统', max_length=30)
    telephone = models.CharField(u'联系电话', max_length=11, null=True, blank=True)
    email = models.EmailField(u'E-Mail', null=True, blank=True)

    def __str__(self):
      return self.name

    class Meta:
        verbose_name = u'-操作系统'
        verbose_name_plural = verbose_name

class OSVersion(models.Model):
    osFamlily = models.ForeignKey(OSFamlily, verbose_name=u'操作系统')
    name = models.CharField(u'操作系统版本', max_length=30)

    def __str__(self):
      return self.name

    class Meta:
        verbose_name = u'-操作系统版本'
        verbose_name_plural = verbose_name

class Server(models.Model):
    name = models.CharField(u'名称', max_length=100)
    organization = models.ForeignKey(Organization, verbose_name=u'组织')
    cinema = models.ForeignKey(Cinema, verbose_name=u'影城', blank=True, null=True)
    status_choices = (('production', u'生产'),
                      ('implementation', u'上线'),
                      ('obsolete', u'下线'),
                      ('stock', u'空闲'),
                      )
    status = models.CharField(u'状态',choices=status_choices, default='implementation', max_length=15)
    tags = models.ManyToManyField('Tag', blank=True)
    location = models.ForeignKey(Location, verbose_name=u'位置', blank=True, null=True)
    rack = models.ForeignKey(Rack, verbose_name=u'机架', blank=True, null=True)
    enclosure = models.ForeignKey(Enclosure, verbose_name=u'机架位置', blank=True, null=True)
    brand = models.ForeignKey(Brand, verbose_name=u'品牌')
    model = models.ForeignKey(Model, verbose_name=u'型号')
    #hosted_on = models.ForeignKey('self', related_name='hosted_on_server', blank=True, null=True)  # for vitural server
    cpu = models.ForeignKey(CPU, verbose_name=u'CPU 型号', null=True, blank=True)
    cpuCount = models.SmallIntegerField(u'CPU 数量', null=True, blank=True)
    memory = models.SmallIntegerField(u'内存大小 /G', null=True, blank=True)
    osFamlily = models.ForeignKey(OSFamlily, verbose_name=u'操作系统', null=True, blank=True)
    osVersion = models.ForeignKey(OSVersion, verbose_name=u'操作系统版本', null=True, blank=True)
    serialNumber = models.CharField(u'产品序列号', max_length=128, unique=True, null=True, blank=True)
    assetNumber = models.CharField(u'资产编号', max_length=128, unique=True, null=True, blank=True)
    #createDate = models.DateField(u'安装日期', null=True, blank=True)
    purchaseDate = models.DateField(u'购买时间', null=True, blank=True)
    expireData = models.DateField(u'过保修期', null=True, blank=True)
    comment = models.TextField(u'备注', max_length=255, null=True, blank=True)


    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name
        # together = ["sn", "asset"]

    def __str__(self):
        return self.name


class HostGroup(models.Model):
    name = models.CharField(u"名称", max_length=30, unique=True)
    desc = models.CharField(u"描述", max_length=100, blank=True)
    servers = models.ManyToManyField('Server', verbose_name=u"服务器", blank=True)
    virtualmachine = models.ManyToManyField('VirtualMachine', verbose_name=u"虚拟机", blank=True)

    #def __unicode__(self):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '-HostGroup'
        verbose_name_plural = verbose_name


class Farm(models.Model):
    name = models.CharField(u'名称', max_length=50)
    organization = models.ForeignKey(Organization, verbose_name=u'拥有者组织')
    status_choices = (('production', u'生产'),
                      ('implementation', u'上线'),
                      ('obsolete', u'下线'),
                      ('stock', u'空闲'),
                      )
    status = models.CharField(u'状态',choices=status_choices, default='implementation', max_length=15)
    createDate = models.DateField(u'创建日期', null=True, blank=True)
    comment = models.CharField(u'备注', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = u'-VM虚拟集群'
        verbose_name_plural = verbose_name

    def __str__(self):
        #return '<id:%s name:%s>' % (self.id, self.name)
        return self.name


class Hypervisor(models.Model):
    name = models.CharField(u'名称', max_length=50)
    organization = models.ForeignKey(Organization, verbose_name=u'拥有者组织')
    farm = models.ForeignKey(Farm, verbose_name=u'集群')
    sever = models.ForeignKey(Server, verbose_name=u'服务器')
    status_choices = (('production', u'生产'),
                      ('implementation', u'上线'),
                      ('obsolete', u'下线'),
                      ('stock', u'空闲'),
                      )
    status = models.CharField(u'状态',choices=status_choices, default='implementation', max_length=15)
    createDate = models.DateField(u'创建日期', null=True, blank=True)
    comment = models.CharField(u'备注', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = u'-VM虚拟主机'
        verbose_name_plural = verbose_name

    def __str__(self):
        #return '<id:%s name:%s>' % (self.id, self.name)
        return self.name


class VirtualMachine(models.Model):
    name = models.CharField(u'名称', max_length=100)
    organization = models.ForeignKey(Organization, verbose_name=u'组织')
    cinema = models.ForeignKey(Cinema, verbose_name=u'影城', blank=True, null=True)
    status_choices = (('production', u'生产'),
                      ('implementation', u'上线'),
                      ('obsolete', u'下线'),
                      ('stock', u'空闲'),
                      )
    status = models.CharField(u'状态',choices=status_choices, default='implementation', max_length=15)
    farm = models.ForeignKey(Farm, verbose_name=u'集群', null=True, blank=True)
    hypervisor = models.ForeignKey(Hypervisor, verbose_name=u'虚拟主机', blank=True, null=True)
    cpu = models.ForeignKey(CPU, verbose_name=u'CPU 型号', null=True, blank=True)
    cpuCount = models.SmallIntegerField(u'CPU 数量', null=True, blank=True)
    memory = models.SmallIntegerField(u'内存大小 /G', null=True, blank=True)
    osFamlily = models.ForeignKey(OSFamlily, verbose_name=u'操作系统', null=True, blank=True)
    osVersion = models.ForeignKey(OSVersion, verbose_name=u'操作系统版本', null=True, blank=True)
    createDate = models.DateField(u'创建日期', null=True, blank=True)

    class Meta:
        verbose_name = '虚拟机'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

'''
class Servervirtualmachine(models.Model):
    name = models.CharField(u'名称', max_length=100)
    ipaddr = models.GenericIPAddressField(u'IP', blank=True, null=True)
    #organization = models.ForeignKey(Organization, verbose_name=u'组织')
    #cinema = models.ForeignKey(Cinema, verbose_name=u'影城', blank=True, null=True)
    status_choices = (('production', u'生产'),
                      ('implementation', u'上线'),
                      ('obsolete', u'下线'),
                      ('stock', u'空闲'),
                      )
    status = models.CharField(u'状态',choices=status_choices, default='implementation', max_length=15)
    #cpu = models.ForeignKey(CPU, verbose_name=u'CPU 型号', null=True, blank=True)
    #cpuCount = models.SmallIntegerField(u'CPU 数量', null=True, blank=True)
    #memory = models.SmallIntegerField(u'内存大小 /G', null=True, blank=True)
    #osFamlily = models.ForeignKey(OSFamlily, verbose_name=u'操作系统', null=True, blank=True)
    #osVersion = models.ForeignKey(OSVersion, verbose_name=u'操作系统版本', null=True, blank=True)

    class Meta:
        verbose_name = 'Servervirtualmachine'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
'''
'''
class deployGroup(models.Model):
    name = models.CharField(u"名称", max_length=30, unique=True)
    desc = models.CharField(u"描述", max_length=100, blank=True)
    servervirtualmachine = models.ManyToManyField(' Servervirtualmachine', verbose_name=u"所在服务器", blank=True)

    #def __unicode__(self):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '-服务器组'
        verbose_name_plural = verbose_name
'''

class StorageSystem(models.Model):
    name = models.CharField(u'名称', max_length=100, null=True)
    organization = models.ForeignKey(Organization, verbose_name=u'组织')
    cinema = models.ForeignKey(Cinema, verbose_name=u'影城')
    location = models.ForeignKey(Location, verbose_name=u'位置', blank=True, null=True)
    status_choices = (('production', u'生产'),
                      ('implementation', u'上线'),
                      ('obsolete', u'下线'),
                      ('stock', u'空闲'),
                      )
    status = models.CharField(u'状态',choices=status_choices, default='implementation', max_length=15)
    #managementIp = models.GenericIPAddressField(u'管理 IP', blank=True, null=True)
    rack = models.ForeignKey(Rack, verbose_name=u'机架', blank=True, null=True)
    enclosure = models.ForeignKey(Enclosure, verbose_name=u'机架位置', blank=True, null=True)
    brand = models.ForeignKey(Brand, verbose_name=u'品牌')
    model = models.ForeignKey(Model, verbose_name=u'型号')
    serialNumber = models.CharField(u'产品序列号', max_length=128, unique=True, default=0)
    assetNumber = models.CharField(u'资产编号', max_length=128, unique=True, default=0)
    #createDate = models.DateField(u'安装日期', null=True, blank=True)
    purchaseDate = models.DateField(u'购买时间', null=True, blank=True)
    expireData = models.DateField(u'过保修期', null=True, blank=True)
 
    def __str__(self):
      return self.name

    class Meta:
        verbose_name = u'存储系统'
        verbose_name_plural = verbose_name


class Asset(models.Model):
    storageSystem = models.ForeignKey(StorageSystem, verbose_name=u'存储系统')
    assetName = models.CharField(u'名称', max_length=60)
    organization = models.ForeignKey(Organization, verbose_name=u'组织')
    cinema = models.ForeignKey(Cinema, verbose_name=u'影城')
    asset_type_choices = (
        ('rack', u'机架'),
        ('server', u'服务器'),
        ('networkdevice', u'网络设备'),
        ('storagedevice', u'存储设备'),
        ('securitydevice', u'安全设备'),
    )
    asset_type = models.CharField(u'类型',choices=asset_type_choices, max_length=64, default='server')
    brand = models.ForeignKey(Brand, verbose_name=u'商标')
    model = models.ForeignKey(Model, verbose_name=u'型号')
    status_choices = ((0, '在线'),
                      (1, '下线'),
                      (2, '未知'),
                      (3, '故障'),
                      (4, '备用'),
                      )
    status = models.SmallIntegerField(u'状态',choices=status_choices, default=0)
    managementIp = models.GenericIPAddressField(u'管理 IP', blank=True, null=True)
    serialNumber = models.CharField(u'产品编号', max_length=128, unique=True, default=0)
    assetNumber = models.CharField(u'资产编号', max_length=128, unique=True, default=0)
    createDate = models.DateField(u'安装日期', null=True, blank=True)
    purchaseDate = models.DateField(u'购买时间', null=True, blank=True)
    expireData = models.DateField(u'过保修期', null=True, blank=True)

    def __str__(self):
      return self.assetName

    class Meta:
        verbose_name = u'设备清单'
        verbose_name_plural = verbose_name


class LogicalVolume(models.Model):
    volumeName = models.CharField(u'名称', max_length=100)
    #asset = models.ForeignKey(Asset, default=1)
    storageSystem = models.ForeignKey(StorageSystem, verbose_name=u'存储系统', null=True, blank=True)
    super_logicalvolume = models.ForeignKey('self', verbose_name=u'卷', null=True, blank=True)
    server = models.ForeignKey(Server, null=True, blank=True)
    virtualMachine = models.ForeignKey(VirtualMachine, verbose_name=u'Virtual Machine', null=True, blank=True)
    #lunID = models.ForeignKey(LunID, default=1)
    raidLevel = models.CharField(u'RAID 级别', max_length=30, blank=True, null=True)
    size = models.CharField(u'容量 /G', max_length=10, null=True, blank=True)
    volumeComment = models.CharField(u'备注', max_length=30, null=True, blank=True)

    def __str__(self):
      return self.volumeName

    class Meta:
        verbose_name = u'-逻辑卷'
        verbose_name_plural = verbose_name

class IpInterface(models.Model):
    name = models.CharField(u'名称', max_length=20)
    storageSystem = models.ForeignKey(StorageSystem, verbose_name=u'存储系统', null=True, blank=True)
    server = models.ForeignKey(Server, verbose_name=u'服务器', null=True, blank=True)
    virtualMachine = models.ForeignKey(VirtualMachine, verbose_name=u'Virtual Machine', null=True, blank=True)
    macAddr = models.CharField(u'MAC 地址', max_length=18, null=True, blank=True)
    ipaddr_type_choices = (
        ('service', u'业务IP'),
        ('manage', u'管理IP'),
    )
    ipaddr_type = models.CharField(u'类型',choices=ipaddr_type_choices, max_length=10, default='manage')
    ipaddr = models.GenericIPAddressField(u'IP', blank=True, null=True)
    netmask = models.GenericIPAddressField(u'子网掩码', blank=True, null=True)
    gateway = models.GenericIPAddressField(u'网关', blank=True, null=True)
    comment = models.CharField(u'备注', max_length=255, null=True, blank=True)
 

    class Meta:
        verbose_name = u'-IP'
        verbose_name_plural = verbose_name


    def __str__(self):
       return self.name


class Software(models.Model):
    name = models.CharField(u'名称', max_length=20)
    version = models.CharField(u'版本', max_length=18)
    vendor = models.CharField(u'厂商', max_length=30)
    software_type_choices = (
        ('middleware', u'中间件'),
        ('db', u'数据库'),
        ('web', u'web 服务'),
        ('other', u'其他'),
    )
    type = models.CharField(u'类型',choices=software_type_choices, max_length=12, default='middleware')
    
    class Meta:
        verbose_name = u'-软件'
        verbose_name_plural = verbose_name

    def __str__(self):
       return '%s %s' % (self.name, self.version)
       #return self.name


class SoftwareInstance(models.Model):
    name = models.CharField(u'名称', max_length=20)
    server = models.ForeignKey(Server, verbose_name=u'服务器', null=True, blank=True)
    virtualMachine = models.ForeignKey(VirtualMachine, verbose_name=u'Virtual Machine', null=True, blank=True)
    status_choices = (
        (0, '非活动'),
        (1, '活动')
    )
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='状态')
    software = models.ForeignKey(Software, verbose_name=u'软件')
    path = models.CharField(u'路径', max_length=20)
    createDate = models.DateField(u'创建日期', null=True, blank=True)
    comment = models.CharField(u'备注', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = u'-软件服务'
        verbose_name_plural = verbose_name

    def __str__(self):
       return self.name


#资产标签
class Tag(models.Model):
    name = models.CharField('Tag name', max_length=32, unique=True)
    #creator = models.ForeignKey('UserProfile')
    #create_date = models.DateField(auto_now_add=True)

    def __str__(self):
       return self.name

    class Meta:
        verbose_name = '-标签'
        verbose_name_plural = verbose_name

