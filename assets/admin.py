# coding:utf-8

from django.contrib import admin
from .models import Organization, Location, Rack, Enclosure, Cinema, Brand, Model, Asset, StorageSystem, CPU, LogicalVolume, IpInterface,OSFamlily, OSVersion, Server, HostGroup, Farm, Hypervisor, VirtualMachine, Software, SoftwareInstance, Tag

# Register your models here.
class RackInline(admin.TabularInline):
    model = Rack
    extra = 0

class EnclosureInline(admin.TabularInline):
    model = Enclosure
    extra = 0

class CPUInline(admin.TabularInline):
    model = CPU
    extra = 0

class IpInterfaceInline(admin.TabularInline):
    model = IpInterface
    fields = ('name', 'macAddr', 'ipaddr_type', 'ipaddr', 'gateway', 'comment')
    extra = 0

class LogicalVolumeInline(admin.TabularInline):
    model = LogicalVolume
    fields = ('volumeName', 'raidLevel', 'size', 'volumeComment')
    extra = 0

class LogicalVolumeServerInline(admin.TabularInline):
    model = LogicalVolume
    fields = ('volumeName', 'super_logicalvolume', 'raidLevel', 'size', 'volumeComment')
    extra = 0

class SoftwareInstanceInline(admin.TabularInline):
    model = SoftwareInstance
    fields = ('name', 'status', 'software', 'path', 'comment')
    extra = 0


class OSFamlilyInline(admin.TabularInline):
    model = OSFamlily
    extra = 0

class OSVersionInline(admin.TabularInline):
    model = OSVersion
    extra = 0

class StorageInline(admin.TabularInline):
    model = StorageSystem
    extra = 0

class AssetInline(admin.TabularInline):
    model = Asset
    extra = 0

class Inline(admin.TabularInline):
    model = Asset
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id','name','code', 'status')
    '''
    fields = ('name','code', 'status')
    
    fieldsets = [
        (None,               {'fields': ['name', 'code', 'status']}),
        ('others', {'fields': ['parent_id']}),
    ]
    '''
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'assetName', 'organization', 'asset_type',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'brandName', 'brandTelephone', 'brandEmail',)

class CPUAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class StorageSystemAdmin(admin.ModelAdmin):
    inlines = [IpInterfaceInline, LogicalVolumeInline]
    list_display = ('id', 'name', 'cinema','status', 'serialNumber', 'assetNumber', 'expireData')
    fieldsets = (
        ['基本信息',{
            'fields':('name','organization', 'cinema', 'status', 'location', 'rack', 'enclosure'),
        }],
        ['更多信息',{
            #'classes': ('collapse',), # CSS            
            'fields': ('brand', 'model', 'serialNumber', 'assetNumber', ),
        }],
        ['日期',{
            #'classes': ('collapse',), # CSS
            'fields': ('purchaseDate', 'expireData'),        }]
    )

    
class ServerAdmin(admin.ModelAdmin):
    inlines = [IpInterfaceInline, LogicalVolumeServerInline, SoftwareInstanceInline]
    list_display = ('id', 'name', 'brand', 'osFamlily', 'organization', 'cinema', 'status', 'location', 'serialNumber', 'assetNumber', 'expireData')
    list_display_links = ('id', 'name')
    fieldsets = (
        ['基本信息',{
            'fields':('name','organization', 'cinema', 'status', 'location', 'rack', 'enclosure', 'tags', 'comment'),
        }],
        ['更多信息',{
            #'classes': ('collapse',), # CSS
            'fields': ('brand', 'model', 'osFamlily', 'osVersion', 'cpu', 'cpuCount', 'memory', 'serialNumber', 'assetNumber', ),
        }],
        ['日期',{
            #'classes': ('collapse',), # CSS
            'fields': ('purchaseDate', 'expireData'),
        }]
    )
    search_fields = ['name','cinema__cinemaName', 'organization__name']
    list_per_page = 10
    list_filter = ['organization', 'cinema', 'brand', 'status', 'location', 'osFamlily', 'purchaseDate', 'expireData']
    choice_fields = ('status')
    fk_fields = ('organization', 'cinema', 'location', 'rack', 'brand', 'model', 'osFamlily',)


class VirtualMachineAdmin(admin.ModelAdmin):
    inlines = [IpInterfaceInline, LogicalVolumeServerInline, SoftwareInstanceInline]
    list_display = ('id', 'name', 'osVersion', 'organization', 'cinema', 'status', 'createDate')
    list_display_links = ('id', 'name')
    fieldsets = (
        ['基本信息',{
            'fields':('name','organization', 'cinema', 'status', 'farm', 'hypervisor'),
        }],
        ['更多信息',{
            #'classes': ('collapse',), # CSS
            'fields': ('osFamlily', 'osVersion', 'cpu', 'cpuCount', 'memory'),
        }],
        ['日期',{
            #'classes': ('collapse',), # CSS
            'fields': ('createDate',),
        }]
    )
    search_fields = ['name','cinema__cinemaName', 'organization__name']
    list_per_page = 10
    list_filter = ['organization', 'cinema', 'status', 'osFamlily', 'createDate']
    choice_fields = ('status')
    fk_fields = ('organization', 'cinema', 'osFamlily',)

'''
class ServervirtualmachineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ipaddr', 'status')
    search_fields = ['name','ipaddr', 'status']
    list_per_page = 10
    list_filter = ['status']
    choice_fields = ('status')
    #fk_fields = ()
'''

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Location)
admin.site.register(Rack)
admin.site.register(Enclosure)
admin.site.register(Cinema)
admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(CPU)
admin.site.register(OSFamlily)
admin.site.register(OSVersion)
admin.site.register(Asset)
admin.site.register(StorageSystem, StorageSystemAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(HostGroup)
admin.site.register(Farm)
admin.site.register(Hypervisor)
admin.site.register(VirtualMachine, VirtualMachineAdmin)
#admin.site.register(Servervirtualmachine, ServervirtualmachineAdmin)
admin.site.register(Software)
admin.site.register(SoftwareInstance)
admin.site.register(Tag)
