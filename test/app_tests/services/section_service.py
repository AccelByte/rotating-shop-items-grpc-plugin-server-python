# Copyright (c) 2023 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

from typing import List
from unittest import IsolatedAsyncioTestCase
import uuid

from app.proto.section_pb2 import (
    GetRotationItemsRequest, 
    GetRotationItemsResponse,
    SectionObject, 
    SectionItemObject,
    BackfillRequest,
    BackfillResponse,
    RotationItemObject
)
from app.services.section_service import AsyncSectionService

from accelbyte_grpc_plugin_tests import create_server


class AsyncSectionServiceTestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.service = AsyncSectionService(None)

    async def test_get_rotation_items(self):
        # arrange
        items : List[SectionItemObject] = []
        for sku in ["S1","S2","S3","S4","S5","S6","S7","S8"]:
            items.append(SectionItemObject(itemId=str(uuid.uuid4()).replace("-",""),itemSku=sku))
        section_object = SectionObject(items=items)
        request = GetRotationItemsRequest(sectionObject=section_object)

        # act
        response = await self.service.GetRotationItems(request, None)

        # assert
        self.assertIsNotNone(response)
        self.assertIsInstance(response, GetRotationItemsResponse)
        self.assertEqual(len(response.items), 1)
    
    async def test_backfill(self):
        # arrange
        items : List[RotationItemObject] = []
        for sku in ["S1","S2","S3"]:
            items.append(RotationItemObject(itemId=str(uuid.uuid4()).replace("-",""), itemSku=sku, owned=(sku == "S1")))
        request = BackfillRequest(items=items)

        # act
        response = await self.service.Backfill(request, None)

        # assert
        self.assertIsNotNone(response)
        self.assertIsInstance(response, BackfillResponse)
        self.assertEqual(len(response.backfilledItems), 1)
