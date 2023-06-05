import traceback
import uuid
import sys
from typing import List, Tuple, Union
from datetime import datetime, timedelta
from os import environ

import accelbyte_py_sdk
import accelbyte_py_sdk.services.auth as auth_service
import accelbyte_py_sdk.api.iam as iam_service
import accelbyte_py_sdk.api.iam.models as iam_models
import accelbyte_py_sdk.api.platform as platform_service
import accelbyte_py_sdk.api.platform.models as platform_models

def get_user_info() -> Tuple[iam_models.ModelUserResponseV3, any]:
    return iam_service.public_get_my_user_v3() 

def set_grpc_plugin_server(namespace : str, grpc_server_url : str):
    return platform_service.update_service_plugin_config(
        namespace=namespace,
        body=platform_models.ServicePluginConfigUpdate.create(
                grpc_server_address=grpc_server_url
            )
    )
        
def create_store(namespace : str, title : str) -> Tuple[platform_models.StoreInfo, any]:
    return platform_service.create_store(
        namespace=namespace,
        body=platform_models.StoreCreate.create(
            title=title,
            description="Description for %s" % title,
            default_language="en",
            default_region="US",
            supported_languages=["en"],
            supported_regions=["US"]
        )
    )
    
def publish_store(namespace : str, store_id : str):
    platform_service.publish_all(
        namespace=namespace,
        store_id=store_id
    )

def create_category(namespace : str, store_id : str, category_path : str):
    platform_service.create_category(
        namespace=namespace,
        store_id=store_id,
        body=platform_models.CategoryCreate.create(
            category_path=category_path,
            localization_display_names={"en" : category_path}
        )
    )

def create_store_view(namespace : str, store_id : str, title : str) -> Tuple[platform_models.FullViewInfo, any]:
    return platform_service.create_view(
        namespace=namespace,
        store_id=store_id,
        body=platform_models.ViewCreate.create(
            name=title,
            display_order=1,
            localizations={"en" : platform_models.Localization.create(title=title)}
        )
    )
    
def create_item(namespace : str, store_id : str, category_path : str, item_base_name : str, item_base_index : int) -> Tuple[platform_models.FullItemInfo, any]:
    title="Item %s %s" % (item_base_name, item_base_index)
    sku="SKU_%s_%s" % (item_base_name, item_base_index)
    return platform_service.create_item(
        namespace=namespace,
        store_id=store_id,
        body=platform_models.ItemCreate.create(
            name=title,
            item_type=platform_models.ItemCreateItemTypeEnum.SEASON,
            category_path=category_path,
            entitlement_type=platform_models.ItemCreateEntitlementTypeEnum.DURABLE,
            season_type=platform_models.ItemCreateSeasonTypeEnum.TIER,
            status = platform_models.ItemCreateStatusEnum.ACTIVE,
            listable=True,
            purchasable=True,
            sku=sku,
            localizations={"en": platform_models.Localization.create(title=title)},
            region_data={"US" : [platform_models.RegionDataItem.create(
                currency_code="USD",
                currency_namespace="accelbyte",
                currency_type=platform_models.RegionDataItemCurrencyTypeEnum.REAL,
                price=(item_base_index+1)*2
            )]}
        )
    )
    
def create_section(namespace : str, store_id : str, category_path : str, view_id : str, section_base_name : str, item_ids : List[str]) -> Tuple[platform_models.FullSectionInfo, None]:
    title="Section %s" % (section_base_name)
    return platform_service.create_section(
        namespace=namespace,
        store_id=store_id,
        body=platform_models.SectionCreate.create(
            view_id=view_id,
            display_order=1,
            name=title,
            active=True,
            start_date=(datetime.today() - timedelta(days=1)).isoformat(),
            end_date=(datetime.today() + timedelta(days=1)).isoformat(),
            rotation_type=platform_models.SectionCreateRotationTypeEnum.FIXED_PERIOD,
            fixed_period_rotation_config=platform_models.FixedPeriodRotationConfig.create(
                backfill_type=platform_models.FixedPeriodRotationConfigBackfillTypeEnum.NONE,
                rule=platform_models.FixedPeriodRotationConfigRuleEnum.SEQUENCE
            ),
            localizations={"en": platform_models.Localization.create(title=title)},
            items=[platform_models.SectionItem.create(id_=id) for id in item_ids]
        )
    )
        
def enable_custom_rotation_for_section(namespace : str, store_id : str, section_id : str, section_base_name : str):
    title="Section %s" % (section_base_name)
    platform_service.update_section(
        namespace=namespace,
        store_id=store_id,
        section_id = section_id,
        body=platform_models.SectionUpdate.create(
            name=title,
            rotation_type=platform_models.SectionUpdateRotationTypeEnum.CUSTOM,
            start_date=(datetime.today() - timedelta(days=1)).isoformat(),
            end_date=(datetime.today() + timedelta(days=1)).isoformat(),
            localizations={"en": platform_models.Localization.create(title=title)}
        )
    )

def enable_fixed_rotation_with_custom_backfill_for_section(namespace : str, store_id : str, section_id : str, section_base_name : str):
    title="Section %s" % (section_base_name)
    platform_service.update_section(
        namespace=namespace,
        store_id=store_id,
        section_id = section_id,
        body=platform_models.SectionUpdate.create(
            name=title,
            rotation_type=platform_models.SectionUpdateRotationTypeEnum.FIXED_PERIOD,
            start_date=(datetime.today() - timedelta(days=1)).isoformat(),
            end_date=(datetime.today() + timedelta(days=1)).isoformat(),
            localizations={"en": platform_models.Localization.create(title=title)},
            fixed_period_rotation_config=platform_models.FixedPeriodRotationConfig.create(
                backfill_type=platform_models.FixedPeriodRotationConfigBackfillTypeEnum.CUSTOM,
                rule=platform_models.FixedPeriodRotationConfigRuleEnum.SEQUENCE
            )
        )
    )
    
def get_active_sections(namespace : str, view_id : str, user_id : str) -> Tuple[Union[None, List[platform_models.SectionInfo]],any]:
    return platform_service.public_list_active_sections(
        namespace=namespace,
        view_id=view_id,
        user_id=user_id
    )
    
def publish_store(namespace : str, store_id : str):
    return platform_service.publish_all(
        namespace=namespace,
        store_id=store_id
    ) 

def delete_store(namespace : str, store_id : str):
    return platform_service.delete_store(
        namespace=namespace,
        store_id=store_id
    )

def unset_grpc_plugin_server(namespace : str):
    return platform_service.delete_service_plugin_config(
        namespace=namespace
    )

def main():
    MODE_ROTATION="rotation"
    MODE_BACKFILL="backfill"
    
    if len(sys.argv) < 3:
        print("Usage: python3 %s [GRPC_SERVER_URL] [%s|%s]" % (sys.argv[0], MODE_ROTATION, MODE_BACKFILL))
        exit(1)
        
    grpc_server_url = sys.argv[1]
    mode = sys.argv[2]
        
    if mode not in [MODE_ROTATION, MODE_BACKFILL]:
        print("Unknown mode: %s" % mode )
        exit(1)
        
    for e in ["AB_BASE_URL", "AB_NAMESPACE", "AB_CLIENT_ID", "AB_CLIENT_SECRET", "AB_USERNAME", "AB_PASSWORD"]:
        if not e in environ:
            print("Missing required environment variable: %s" % e)
            exit(1)
    
    username = environ["AB_USERNAME"]
    password = environ["AB_PASSWORD"]
    namespace = environ["AB_NAMESPACE"]
    
    accelbyte_py_sdk.initialize()
    
    category_path = "/customitemrotationtest"
    item_count = 10

    dummy_base_name = str(uuid.uuid4()).split('-')[0]    # Random string used for creating dummy data
    store_info = None
    
    try:
        print("# Arrange")
        print("## Login user")
        _, error = auth_service.login_user(username=username, password=password)
        if error:
            raise Exception(error)
        print("## Get user info")
        user_info, error = get_user_info() 
        if error:
            raise Exception(error)
        print("## Set gRPC server URL")
        _, error = set_grpc_plugin_server(namespace=namespace, grpc_server_url=grpc_server_url)
        if error:
            raise Exception(error)
        print("## Create store")
        store_info, error = create_store(
            namespace=namespace, 
            title="Item Rotation Plugin Demo Store"
        )
        if error:
            raise Exception(error)
        print("## Create category")
        create_category(
            namespace=namespace,
            store_id=store_info.store_id,
            category_path=category_path
        )
        if error:
            raise Exception(error)
        print("## Create store view")
        view_info, error = create_store_view(
            namespace=namespace,
            store_id=store_info.store_id,
            title="Item Rotation Default View"
        )
        if error:
            raise Exception(error)
        print("## Create item")
        item_ids : List[str] = []
        for i in range(item_count):
            print("- Item %s %s" % (dummy_base_name,i+1))
            new_item, error = create_item(
                namespace=namespace,
                store_id=store_info.store_id,
                category_path=category_path,
                item_base_name=dummy_base_name,
                item_base_index=i+1
            )
            if error:
                raise Exception(error)
            item_ids.append(new_item.item_id)
        print("## Create section")
        section_info, error = create_section(
            namespace=namespace, 
            store_id=store_info.store_id,
            category_path=category_path,
            view_id=view_info.view_id,
            section_base_name=dummy_base_name,
            item_ids=item_ids
        )
        if error:
            raise Exception(error)
        print("# Act")
        if mode == MODE_ROTATION:
            print("## Enable custom rotation for section")
            enable_custom_rotation_for_section(
                namespace=namespace,
                store_id=store_info.store_id,
                section_id=section_info.section_id,
                section_base_name=dummy_base_name
            )
        else:
            print("## Enable fixed rotation with custom backfill for section")
            enable_fixed_rotation_with_custom_backfill_for_section(
                namespace=namespace,
                store_id=store_info.store_id,
                section_id=section_info.section_id,
                section_base_name=dummy_base_name
            )
        print("## Publish store")
        _, error = publish_store(namespace=namespace,store_id=store_info.store_id)
        if error:
            raise Exception(error)
        print("# Assert")
        print("## Get active sections")
        active_sections, error = get_active_sections(
            namespace=namespace,
            view_id=view_info.view_id,
            user_id=user_info.user_id
        )
        if error:
            raise Exception(error)
        if active_sections is None or len(active_sections) <= 0:
            raise Exception("active_sections is not supposed to be empty")
        for section in active_sections:
            print("- Section %s:" % section.section_id)
            if section.current_rotation_items is not None and len(section.current_rotation_items) > 0:
                for item in section.current_rotation_items:
                    print("  - %s" % item.title)
    except:
        print(traceback.format_exc())
    finally:
        print("# Clean Up")
        if store_info:
            print("## Delete store")
            _, error = delete_store(namespace=namespace, store_id=store_info.store_id)
            if error:
                print("An error has occurred but ignored: %s" % error)
        print("## Unset gRPC server URL")
        _, error = unset_grpc_plugin_server(namespace=namespace)
        if error:
            print("An error has occurred but ignored: %s" % error)


if __name__ == "__main__":
    main()
