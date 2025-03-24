# Copyright (c) 2025 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

from datetime import datetime
import json
from logging import Logger
import math
from typing import List, Optional

from google.protobuf.json_format import MessageToDict

from accelbyte_py_sdk import AccelByteSDK

from ..proto.section_pb2 import (
    BackfillRequest,
    BackfilledItemObject,
    RotationItemObject,
    BackfillResponse,
    GetRotationItemsRequest,
    GetRotationItemsResponse,
    SectionItemObject,
    DESCRIPTOR,
)
from ..proto.section_pb2_grpc import SectionServicer


class AsyncSectionService(SectionServicer):
    full_name: str = DESCRIPTOR.services_by_name["Section"].full_name
    upper_limit: float = float(24)

    def __init__(self, sdk: Optional[AccelByteSDK] = None, logger: Optional[Logger] = None) -> None:
        self.sdk = sdk
        self.logger = logger

    async def GetRotationItems(self, request: GetRotationItemsRequest, context):
        """*
        GetRotationItems: get current rotation items, this method will be called by rotation type is CUSTOM
        """
        self.log_payload(f'{self.GetRotationItems.__name__} request: %s', request)
        items: List[SectionItemObject] = request.sectionObject.items
        input_count: int = len(items)
        current_point: float = float(datetime.now().hour)
        selected_index: int = int(math.floor((input_count/self.upper_limit)*current_point))
        selected_item: SectionItemObject = items[selected_index]
        response_items: List[SectionItemObject] = [selected_item]
        response: GetRotationItemsResponse = GetRotationItemsResponse(expiredAt=0, items=response_items)
        self.log_payload(f'{self.GetRotationItems.__name__} response: %s', response)
        return response

    async def Backfill(self, request: BackfillRequest, context):
        """*
        Backfill method trigger condition:
        1. Rotation type is FIXED_PERIOD
        2. Backfill type is CUSTOM
        3. User already owned any one of current rotation items.
        """
        self.log_payload(f'{self.Backfill.__name__} request: %s', request)
        new_items: List[BackfilledItemObject] = []
        item: RotationItemObject
        for item in request.items:
            if item.owned:
                # Use the last item in the request for backfill for demo purpose only
                backfill_item_id = request.items[-1].itemId
                new_item: BackfilledItemObject = BackfilledItemObject(itemId=backfill_item_id, index=item.index)
                new_items.append(new_item)
        response: BackfillResponse = BackfillResponse(backfilledItems=new_items)
        self.log_payload(f'{self.Backfill.__name__} response: %s', response)
        return response

    # noinspection PyShadowingBuiltins
    def log_payload(self, format: str, payload):
        if not self.logger:
            return
        payload_dict = MessageToDict(payload, preserving_proto_field_name=True)
        payload_json = json.dumps(payload_dict)
        self.logger.info(format % payload_json)
