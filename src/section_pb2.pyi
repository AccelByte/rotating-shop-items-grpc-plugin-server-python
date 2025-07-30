from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BackfillRequest(_message.Message):
    __slots__ = ["items", "namespace", "sectionId", "sectionName", "userId"]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SECTIONID_FIELD_NUMBER: _ClassVar[int]
    SECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[RotationItemObject]
    namespace: str
    sectionId: str
    sectionName: str
    userId: str
    def __init__(self, userId: _Optional[str] = ..., namespace: _Optional[str] = ..., items: _Optional[_Iterable[_Union[RotationItemObject, _Mapping]]] = ..., sectionName: _Optional[str] = ..., sectionId: _Optional[str] = ...) -> None: ...

class BackfillResponse(_message.Message):
    __slots__ = ["backfilledItems"]
    BACKFILLEDITEMS_FIELD_NUMBER: _ClassVar[int]
    backfilledItems: _containers.RepeatedCompositeFieldContainer[BackfilledItemObject]
    def __init__(self, backfilledItems: _Optional[_Iterable[_Union[BackfilledItemObject, _Mapping]]] = ...) -> None: ...

class BackfilledItemObject(_message.Message):
    __slots__ = ["index", "itemId", "itemSku"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    ITEMID_FIELD_NUMBER: _ClassVar[int]
    ITEMSKU_FIELD_NUMBER: _ClassVar[int]
    index: int
    itemId: str
    itemSku: str
    def __init__(self, itemId: _Optional[str] = ..., itemSku: _Optional[str] = ..., index: _Optional[int] = ...) -> None: ...

class GetRotationItemsRequest(_message.Message):
    __slots__ = ["namespace", "sectionObject", "userId"]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SECTIONOBJECT_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    sectionObject: SectionObject
    userId: str
    def __init__(self, userId: _Optional[str] = ..., namespace: _Optional[str] = ..., sectionObject: _Optional[_Union[SectionObject, _Mapping]] = ...) -> None: ...

class GetRotationItemsResponse(_message.Message):
    __slots__ = ["expiredAt", "items"]
    EXPIREDAT_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    expiredAt: int
    items: _containers.RepeatedCompositeFieldContainer[SectionItemObject]
    def __init__(self, items: _Optional[_Iterable[_Union[SectionItemObject, _Mapping]]] = ..., expiredAt: _Optional[int] = ...) -> None: ...

class RotationItemObject(_message.Message):
    __slots__ = ["index", "itemId", "itemSku", "owned"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    ITEMID_FIELD_NUMBER: _ClassVar[int]
    ITEMSKU_FIELD_NUMBER: _ClassVar[int]
    OWNED_FIELD_NUMBER: _ClassVar[int]
    index: int
    itemId: str
    itemSku: str
    owned: bool
    def __init__(self, itemId: _Optional[str] = ..., itemSku: _Optional[str] = ..., owned: bool = ..., index: _Optional[int] = ...) -> None: ...

class SectionItemObject(_message.Message):
    __slots__ = ["itemId", "itemSku"]
    ITEMID_FIELD_NUMBER: _ClassVar[int]
    ITEMSKU_FIELD_NUMBER: _ClassVar[int]
    itemId: str
    itemSku: str
    def __init__(self, itemId: _Optional[str] = ..., itemSku: _Optional[str] = ...) -> None: ...

class SectionObject(_message.Message):
    __slots__ = ["endDate", "items", "sectionId", "sectionName", "startDate"]
    ENDDATE_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    SECTIONID_FIELD_NUMBER: _ClassVar[int]
    SECTIONNAME_FIELD_NUMBER: _ClassVar[int]
    STARTDATE_FIELD_NUMBER: _ClassVar[int]
    endDate: int
    items: _containers.RepeatedCompositeFieldContainer[SectionItemObject]
    sectionId: str
    sectionName: str
    startDate: int
    def __init__(self, sectionName: _Optional[str] = ..., sectionId: _Optional[str] = ..., startDate: _Optional[int] = ..., endDate: _Optional[int] = ..., items: _Optional[_Iterable[_Union[SectionItemObject, _Mapping]]] = ...) -> None: ...
