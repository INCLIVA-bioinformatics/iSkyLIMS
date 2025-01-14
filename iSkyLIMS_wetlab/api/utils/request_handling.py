from datetime import datetime

from iSkyLIMS_core.models import (
    SampleProjects,
    SampleProjectsFields,
    Samples,
    PatientCore,
    LabRequest,
    SampleType,
    Species,
    StatesForSample,
)
from iSkyLIMS_core.utils.handling_samples import increase_unique_value


def get_sample_project_obj(project_name):
    """Check if sampleProyect is defined in database"""
    if SampleProjects.objects.filter(sampleProjectName__exact=project_name).exists():
        return SampleProjects.objects.filter(
            sampleProjectName__exact=project_name
        ).last()
    return False


def get_project_fields_id_and_name(p_obj):
    """Fetch the fields defined for project"""
    fields = []
    if SampleProjectsFields.objects.filter(sampleProjects_id=p_obj).exists():
        p_field_objs = SampleProjectsFields.objects.filter(sampleProjects_id=p_obj)
        for p_field_obj in p_field_objs:
            fields.append([p_field_obj.get_field_id(), p_field_obj.get_field_name()])
    return fields


def get_patient_obj(patient):
    """Get the patient instance"""
    if PatientCore.objects.filter(patientCode__iexact=patient).exists():
        return PatientCore.objects.filter(patientCode__iexact=patient).last()
    return False


def split_sample_data(data):
    """Split the json data in 2 dictionaries, for having data to create the
    sample and data to create the project related info
    """
    split_data = {"s_data": {}, "p_data": []}
    sample_fields = [
        "patientCore",
        "sampleName",
        "labRequest",
        "sampleType",
        "species",
        "project",
        "sampleEntryDate",
        "sampleCollectionDate",
        "sampleLocation",
        "onlyRecorded",
    ]
    for sample_field in sample_fields:
        try:
            if "date" in sample_field.lower():
                split_data["s_data"][sample_field] = datetime.strptime(
                    data[sample_field], "%Y/%m/%d"
                )
            else:
                split_data["s_data"][sample_field] = data[sample_field]
        except KeyError as e:
            return str(str(e) + " is not defined in your query")
    # fetch project fields
    project_obj = get_sample_project_obj(data["project"])
    if not project_obj:
        return "Project is not defined"
    project_fields = get_project_fields_id_and_name(project_obj)
    # check fields that are linked to other table
    if len(project_fields) > 0:
        for p_field in project_fields:
            try:
                split_data["p_data"].append(
                    {
                        "sampleProjecttField_id": p_field[0],
                        "sampleProjectFieldValue": data[p_field[1]],
                    }
                )
            except KeyError as e:
                return str(str(e) + " is not defined in your query")
    return split_data


def include_instances_in_sample(data):
    """Fecth the patient instance"""
    if data["patientCore"] == "" or data["patientCore"].lower() == "null":
        data["patientCore"] = None
    else:
        try:
            data["patientCore"] = get_patient_obj(data["patientCore"]).get_patient_id()
        except AttributeError:
            return str(
                "patientCore " + data["patientCore"] + " is not defined in database"
            )
    if LabRequest.objects.filter(labName__exact=data["labRequest"]).exists():
        data["labRequest"] = (
            LabRequest.objects.filter(labName__exact=data["labRequest"]).last().get_id()
        )
    else:
        return str("labRequest " + data["labRequest"] + " is not defined in database")
    if SampleType.objects.filter(sampleType__exact=data["sampleType"]).exists():
        data["sampleType"] = (
            SampleType.objects.filter(sampleType__exact=data["sampleType"])
            .last()
            .get_sample_type_id()
        )
    else:
        return str("sampleType " + data["sampleType"] + " is not defined in database")
    if Species.objects.filter(speciesName__exact=data["species"]).exists():
        data["species"] = (
            Species.objects.filter(speciesName__exact=data["species"]).last().get_id()
        )
    else:
        return str("species " + data["species"] + " is not defined in database")
    if SampleProjects.objects.filter(sampleProjectName__exact=data["project"]).exists():
        data["project"] = (
            SampleProjects.objects.filter(sampleProjectName__exact=data["project"])
            .last()
            .get_id()
        )
    else:
        return str("project " + data["project"] + " is not defined")
    if data["onlyRecorded"].lower() == "yes":
        data["sampleState"] = (
            StatesForSample.objects.filter(sampleStateName="Completed").last().get_id()
        )
    else:
        data["sampleState"] = (
            StatesForSample.objects.filter(sampleStateName="Defined").last().get_id()
        )

    return data


def include_codding(user_name, sample):
    """Include Unique_id and Code_"""
    c_data = {}
    if not Samples.objects.exclude(uniqueSampleID__isnull=True).exists():
        c_data["uniqueSampleID"] = "AAA-0001"
    else:
        last_unique_value = (
            Samples.objects.exclude(uniqueSampleID__isnull=True).last().uniqueSampleID
        )
        c_data["uniqueSampleID"] = increase_unique_value(last_unique_value)
    c_data["sampleCodeID"] = str(user_name + "_" + sample)
    return c_data
