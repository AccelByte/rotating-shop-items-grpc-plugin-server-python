# Copyright (c) 2023 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

from datetime import datetime
import json
from logging import Logger, getLogger
import math
from typing import List, Optional
import uuid

from google.protobuf.json_format import MessageToDict

from app.proto.section_pb2 import (
    BackfillRequest,
    BackfilledItemObject,
    RotationItemObject,
    BackfillResponse,
    GetRotationItemsRequest,
    GetRotationItemsResponse,
    SectionItemObject,
    DESCRIPTOR,
)
from app.proto.section_pb2_grpc import SectionServicer

class AsyncSectionService(SectionServicer):
    full_name: str = DESCRIPTOR.services_by_name["Section"].full_name
    upper_limit : float = float(24)

    def __init__(self, logger: Optional[Logger]) -> None:
        self.logger = (
            logger if logger is not None else getLogger(self.__class__.__name__)
        )

    async def GetRotationItems(self, request : GetRotationItemsRequest, context):
        """*
        GetRotationItems: get current rotation items, this method will be called by rotation type is CUSTOM
        """
        self.log_payload(f'{self.GetRotationItems.__name__} request: %s', request)
        items : List[SectionItemObject] = request.sectionObject.items
        input_count : int = len(items)
        current_point : float = float(datetime.now().hour)
        selected_index : int = int(math.floor((input_count/self.upper_limit)*current_point))
        selected_item : SectionItemObject = items[selected_index]
        response_items : List[SectionItemObject] = [selected_item]
        response : GetRotationItemsResponse = GetRotationItemsResponse(expiredAt=0, items=response_items)
        self.log_payload(f'{self.GetRotationItems.__name__} response: %s', response)
        return response

    async def Backfill(self, request : BackfillRequest, context):
        """*
        Backfill method trigger condition:
        1. Rotation type is FIXED_PERIOD
        2. Backfill type is CUSTOM
        3. User already owned any one of current rotation items.
        """
        self.log_payload(f'{self.Backfill.__name__} request: %s', request)
        new_items : List[BackfilledItemObject] = []
        item : RotationItemObject
        for item in request.items:
             if item.owned:
                 new_item : BackfilledItemObject = BackfilledItemObject(itemId=str(uuid.uuid4()).replace("-",""), index=item.index)
                 new_items.append(new_item)
        response : BackfillResponse = BackfillResponse(backfilledItems=new_items)
        self.log_payload(f'{self.Backfill.__name__} response: %s', response)
        return response
    
    def log_payload(self, format : str, payload):
        if not self.logger:
            return
        payload_dict = MessageToDict(payload, preserving_proto_field_name=True)
        payload_json = json.dumps(payload_dict)
        self.logger.info(format % payload_json)
    