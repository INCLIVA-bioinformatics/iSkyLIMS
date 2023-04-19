from django.contrib import admin
from iSkyLIMS_drylab.models import *
from django_mptt_admin.admin import DjangoMpttAdmin

class ResolutionStatesAdmin(admin.ModelAdmin):
    list_display = ["state_value"]

class ServiceStateAdmin(admin.ModelAdmin):
    list_display = ["state_value", "state_display", "description", "show_in_stats"]


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "serviceRequestNumber",
        "serviceSeqCenter",
        "serviceUserId",
        "service_state",
        "serviceCreatedOnDate",
        "serviceOnDeliveredDate",
    )
    list_filter = ["serviceCreatedOnDate"]
    search_fields = ["serviceRequestNumber__icontains"]


class RequestedSamplesInServicesAdmin(admin.ModelAdmin):
    list_display = ["samplesInService", "sampleName", "projectName", "runName"]


class UploadServiceFileAdmin(admin.ModelAdmin):
    list_display = ["uploadService", "uploadFile", "uploadFileName"]
    search_fields = (
        "uploadService__serviceRequestNumber__icontains",
        "uploadFileName__icontains",
    )


class AvailableServiceAdmin(DjangoMpttAdmin):
    list_display = ["avail_service_description", "serviceId", "inUse"]


class ResolutionAdmin(admin.ModelAdmin):
    list_display = (
        "resolutionServiceID",
        "resolutionNumber",
        "resolutionState",
        "resolutionDate",
        "resolutionEstimatedDate",
        "resolutionFullNumber",
        "resolutionAsignedUser",
    )
    list_filter = ["resolutionDate"]
    search_fields = [
        "resolutionNumber__icontains",
        "resolutionAsignedUser__username__icontains",
    ]


class ResolutionParametersAdmin(admin.ModelAdmin):
    list_display = [
        "resolution",
        "resolutionParameter",
        "resolutionParamValue",
        "resolutionParamNotes",
    ]


class DeliveryAdmin(admin.ModelAdmin):
    list_display = [
        "deliveryResolutionID",
        "deliveryDate",
        "executionStartDate",
        "executionEndDate",
        "executionTime",
        "permanentUsedSpace",
        "temporaryUsedSpace",
        "deliveryNotes",
    ]


class PipelinesManager(admin.ModelAdmin):
    list_display = ["pipelineName", "pipelineVersion", "pipelineInUse", "pipelineFile"]


class ParameterPipelineManager(admin.ModelAdmin):
    list_display = ["parameterPipeline", "parameterName", "parameterValue"]


class ConfigSettingAdmin(admin.ModelAdmin):
    list_display = ["configurationName", "configurationValue"]


admin.site.register(ServiceState, ServiceStateAdmin)
admin.site.register(ResolutionStates, ResolutionStatesAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(UploadServiceFile, UploadServiceFileAdmin)
admin.site.register(ResolutionParameters, ResolutionParametersAdmin)
admin.site.register(RequestedSamplesInServices, RequestedSamplesInServicesAdmin)
admin.site.register(AvailableService, AvailableServiceAdmin)
admin.site.register(Resolution, ResolutionAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Pipelines, PipelinesManager)
admin.site.register(ParameterPipeline, ParameterPipelineManager)
admin.site.register(ConfigSetting, ConfigSettingAdmin)
