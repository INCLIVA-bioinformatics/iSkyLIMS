
from iSkyLIMS_core.models import *
from iSkyLIMS_core.utils.handling_protocols import get_protocol_obj_from_name
from iSkyLIMS_core.core_config import *
from django.contrib.auth.models import User
from datetime import date

def get_commercial_kit_id(kit_name):
    if CommercialKits.objects.filter(name__iexact = kit_name).exists():
        return CommercialKits.objects.get(name__iexact = kit_name)
    else:
        return None

def get_defined_commercial_kits():
    commercial_kit_list = []
    if CommercialKits.objects.exists():
        kits = CommercialKits.objects.all().order_by('name')
        for kit in kits:
            commercial_kit_list.append(kit.get_name())
    return commercial_kit_list

def get_lot_user_commercial_kit_id(lot_number):
    if UserLotCommercialKits.objects.filter(chipLot__iexact = lot_number).exists():
        return UserLotCommercialKits.objects.get(chipLot__iexact = lot_number)
    else:
        return None

def get_commercial_kit_obj_from_name(kit_name):
    if CommercialKits.objects.filter(name__exact = kit_name).exists():
        return CommercialKits.objects.get(name__exact = kit_name)
    return None

def get_data_for_commercial_kits():

    data_commercial_kits = {}
    data_commercial_kits['data'] = {}
    if CommercialKits.objects.exists():
        kits = CommercialKits.objects.all().order_by('name')
        for kit in kits:
            data_kits = []
            commercial_kit_name = kit.get_name()

            protocol_objs = kit.protocolKits.all()
            protocols = []
            for protocol_obj in protocol_objs:
                protocols.append(protocol_obj.get_name())

            data_kits.append(protocols)
            #data_kits.append(kit.get_name())
            data_kits.append(kit.get_provider_kit_name())
            data_kits.append(kit.get_cat_number())
            data_kits.append(kit.get_maximum_uses())


            #if not protocol in data_commercial_kits['data']:
            #   data_commercial_kits['data'][protocols] = []
            data_commercial_kits['data'][commercial_kit_name] = [data_kits]
        data_commercial_kits['headings'] = HEADING_FOR_COMMERCIAL_KIT_BASIC_DATA

    return data_commercial_kits

def get_commercial_kit_basic_data(kit_obj):
    kit_data = {}
    kit_data['data'] = kit_obj.get_basic_data()
    kit_data['heading'] = HEADING_FOR_NEW_SAVED_COMMERCIAL_KIT
    return  kit_data

def get_expired_lot_user_kit (register_user_obj):

    user_expired_kits = {}
    user_expired_kits['data'] = {}
    if UserLotCommercialKits.objects.filter(user = register_user_obj, expirationDate__lt = date.today()).exists():

        user_kits = UserLotCommercialKits.objects.filter(user = register_user_obj, expirationDate__lt = date.today()).order_by('basedCommercial')
        for user_kit in user_kits:
            data_kit = []
            c_kit = user_kit.get_commercial_kit()
            data_kit.append(user_kit.get_nick_name())
            data_kit.append(user_kit.get_lot_number())
            data_kit.append(user_kit.get_expiration_date())
            data_kit.append(user_kit.get_used_percentage())
            if not c_kit in user_expired_kits['data']:
                user_expired_kits['data'][c_kit] = []
            user_expired_kits['data'][c_kit].append(data_kit)
    user_expired_kits['headings'] = HEADING_FOR_USER_LOT_INVENTORY
    return user_expired_kits

def get_valid_lot_user_kit (register_user_obj):

    valid_kits = {}
    valid_kits['data'] = {}
    if UserLotCommercialKits.objects.filter(user = register_user_obj, expirationDate__gte = date.today()).exists():

        user_kits = UserLotCommercialKits.objects.filter(user = register_user_obj, expirationDate__gte = date.today()).order_by('basedCommercial')
        for user_kit in user_kits:
            data_kit = []
            c_kit = user_kit.get_commercial_kit()
            data_kit.append(user_kit.get_nick_name())
            data_kit.append(user_kit.get_lot_number())
            data_kit.append(user_kit.get_expiration_date())
            data_kit.append(user_kit.get_used_percentage())
            if not c_kit in valid_kits['data']:
                valid_kits['data'][c_kit] = []
            valid_kits['data'][c_kit].append(data_kit)
    valid_kits['headings'] = HEADING_FOR_USER_LOT_INVENTORY
    return valid_kits

def get_lot_user_commercial_kit_basic_data(kit_obj):
    lot_kit_data = {}
    lot_kit_data['data'] = kit_obj.get_basic_data()
    lot_kit_data['heading'] = HEADING_FOR_LOT_USER_COMMERCIAL_KIT_BASIC_DATA
    return  lot_kit_data


def get_lot_commercial_kits(protocol_obj):
    '''
    Description:
        The function get the user commercial kits that are defined for using
        for the protocol.
        Because of the sharing lot commercial kits between the investigators
        the result is not longer filtered by the user whom record the kit.
    Input:
        protocol_obj  # protocol object
    Return
        user_kit_list
    '''
    user_kit_list = []

    if CommercialKits.objects.filter(protocolKits = protocol_obj).exists():
        commercial_kits = CommercialKits.objects.filter(protocolKits = protocol_obj)
        if UserLotCommercialKits.objects.filter(basedCommercial__in = commercial_kits, expirationDate__gte = date.today()).exists():
            user_kits = UserLotCommercialKits.objects.filter(basedCommercial__in = commercial_kits, expirationDate__gte = date.today())
            for user_kit in user_kits:
                user_kit_list.append(user_kit.get_lot_number())
    return user_kit_list


def store_commercial_kit (kit_data):
    commercial_kit_values = {}
    #commercial_kit_values['protocol_id']= get_protocol_obj_from_name(kit_data['protocol'])
    commercial_kit_values['name'] = kit_data['kitName']
    commercial_kit_values['provider'] = kit_data['provider']
    commercial_kit_values['cat_number'] = kit_data ['catNo']
    commercial_kit_values['description'] = kit_data['description']
    #commercial_kit_values['maximumUses'] = kit_data['usesNumber']
    commercial_kit_values['maximumUses'] =  0

    new_kit = CommercialKits.objects.create_commercial_kit(commercial_kit_values )
    for protocol in kit_data.getlist('protocol'):
        new_kit.protocolKits.add(get_protocol_obj_from_name(protocol))
    return new_kit

def store_lot_user_commercial_kit (kit_data, user_name):
    commercial_kit_obj = get_commercial_kit_obj_from_name(kit_data['commercialKit'])
    lot_kit_values = {}
    lot_kit_values['user'] = user_name
    lot_kit_values['basedCommercial']= commercial_kit_obj
    lot_kit_values['chipLot'] = kit_data['barCode']
    lot_kit_values['expirationDate'] = kit_data ['expirationDate']

    new_kit = UserLotCommercialKits.objects.create_user_lot_commercial_kit(lot_kit_values )
    return new_kit
