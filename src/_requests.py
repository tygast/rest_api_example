# -*- coding: utf-8 -*-
import copy
import numpy as np
import requests
from requests.auth import HTTPBasicAuth
from requests.models import HTTPError, Response
from configs import config

auth = HTTPBasicAuth(config.user, config.password)


def _get(
    module: str,
    _filter: str = None,
    operator: str = None,
    identifier: str = None,
    top: int = None,
    skip: int = None,
    raw: bool = False,
) -> Response:
    """
    Returns:
        json response from maintenance connection web api which returns result
        sets that will default to a page size of 50 with a maximum of 500. For
        paging through result sets, see URL Example url_6.

    Modules:
        assets
        classifications

    Filters:
        ID -> asset/location tag id or classification abbreviation
        PK -> Mainenance Connection assigned integer associated with asset/location/classification
        parentRef.ID -> asset/location tag id of asset parent
        ClassificationRef.ID -> classifiation id of asset/location
        RepairCenterRef.ID -> repair center id of asset/location
        ShopRef.ID -> shop id of asset/location
        Vicinity -> P&ID page number of asset/location
        Icon -> icon.gif of asset/location
        IsLocation -> Boolean (True or False)
        TypeDetails.Value -> 'A' for asset or 'L' for location
        LastModifiedDate -> most recent date asset or location was modified
        IsOpen -> all work orders currently open (boolean)

    Logical Operators:
        eq -> equals
        ne -> not equal
        gt -> greater than
        ge -> greater than or equal
        lt -> less than
        le -> less than or equal
        and -> logical and
        or -> logical or
        not -> logical negation

    Grouping Operators:
        ( ) -> precedence grouping

    Identifiers:
        'ID' -> the asset/location tag id or classification abbreviation
        'Date' -> filter asset/location or classification based on operator
        'Value' -> asset('A') or location('L')
        'top' -> int used to parse through values on a page
        'skip' -> int used to parse through pages
        'orderby' -> rearrange how objectas appear using (decending ('desc') or ascending ('asc'))

    Top & Skip Querystrings:
        By default, GET requests to the Maintenance Connection Web API will return a page containing the top 50 matching
        results. This can be extended to a maximum of 500 results by appending an OData style $top
        querystring to the end of the request URI. Paging through result sets is done through the
        use of the $skip keyword.

    URL Examples:
        >>> url_1 = 'http://server/v8/assets?$filter=ID%20eq%20"SHI-V-1405"'
        >>> url_2 = 'http://server/v8/classifications?$filter=ID%20eq%20"V"'
        >>> url_3 = 'http://server/v8/assets?$filter=parentRef.ID%20eq%20"SHI-V-1405"'
        >>> url_4 = 'http://server/v8/assets?$filter=ClassificationRef.ID%20eq%20"V"'
        >>> url_5 = 'http://server/v8/assets?$filter=RepairCenterRef.ID%20eq%20"Main"'
        >>> url_6 = 'http://server/v8/assets?$filter=LastModifiedDate%20gt%20"2012-10-15"'
        >>> url_7 = 'http://server/v8/assets?$filter=IsOpen%20eq%20true%20and%20TargetHours%20lt%5'
        >>> url_8 = 'http://server/v8/assets?$filter=RepairCenterRef.ID%20eq%20"Main"&$top=5&$skip=10'

    """
    if _filter:
        query = (
            f'?$filter={_filter}%20{operator}%20"{identifier}"&$top={top}&$skip={skip}'
        )
    else:
        query = f"?$top={top}&$skip={skip}"

    url = f"http://{config.server}/v8/{module}{query}"

    r = requests.get(url, auth=auth)
    if r.ok == True:
        print(f"Connection Successful!\nStatus Code: {r.status_code}\n")
    else:
        print(f"Connection NOT Successful\nStatus Code: {r.status_code}\n")
    if raw:
        collection = r.json()["Results"]
    else:
        results = r.json()["Results"]
        _resp = {}

        collection = []
        for result in results:
            _resp["PK"] = result.get("PK", None)
            _resp["ID"] = result.get("ID", None)
            _resp["Name"] = result.get("Name", None)
            _resp["IsLocation"] = result.get("IsLocation", None)
            _resp["Vicinity"] = result.get("Vicinity", None)
            _resp["Icon"] = result.get("Icon", None)
            _resp["UDFChar9"] = result.get("UDFChar9", None)
            try:
                _resp["ParentRef"] = {
                    "ID": result.get("ParentRef", None).get("ID", None)
                }
            except AttributeError:
                _resp["ParentRef"] = result.get("ParentRef", None)
            try:
                _resp["ClassificationRef"] = {
                    "ID": result.get("ClassificationRef", None).get("ID", None)
                }
            except AttributeError:
                _resp["ClassificationRef"] = result.get("ClassificationRef", None)
            try:
                _resp["RepairCenterRef"] = {
                    "ID": result.get("RepairCenterRef", None).get("ID", None)
                }
            except AttributeError:
                _resp["RepairCenterRef"] = result.get("RepairCenterRef", None)
            try:
                _resp["ShopRef"] = {"ID": result.get("ShopRef", None).get("ID", None)}
            except AttributeError:
                _resp["ShopRef"] = result.get("ShopRef", None)
            try:
                _resp["TypeDetails"] = {
                    "Value": result.get("TypeDetails").get("Value", None)
                }
            except AttributeError:
                _resp["TypeDetails"] = result.get("TypeDetails")

            collection.append(copy.deepcopy(_resp))

    return collection


def _post(module: str, data: np.array) -> Response:
    """
    Returns:
        json response for creating one or more asset/classification

    Modules:
        assets
        classifications

    URL Example:
        >>> url_1 = 'http://server/v8/assets'
        >>> url_2 = 'http://server/v8/classifications'

    Data Example:
        [{'ID': 'SHI-V-1405',
        'Name': 'V-1405 Flash Separator',
        'IsLocation': False,
        'Vicinity': 'SHNR-PID-1104',
        'Icon': 'iconlib/CL/classifications/cylindar_g.gif',
        'UDFChar9': 'SHI-V-1405',
        'ParentRef': {'ID': 'SHI-INLET FLASH GAS AREA'},
        'ClassificationRef': {'ID': 'V'},
        'RepairCenterRef': {'ID': 'SA-HUBS-SHI'},
        'ShopRef': {'ID': 'SA-HUBS-SHI-OPS'},
        'TypeDetails': {'Value': 'A'}}]

    Required:
        ID, Name, ParentRef, ClassificationRef

    """

    url = f"http://{config.server}/v8/{module}"
    r = requests.post(url, auth=auth, json=data)
    if r.ok == True:
        print(
            f"Connection Successful!\nStatus Code: {r.status_code}\nThe {module[:-1]} has been added\n"
        )
    else:
        print(f"Connection NOT Successful\nStatus Code: {r.status_code}\n")

    _resp = r.json()

    return _resp


def _put(module: str, data: np.array) -> Response:
    """
    Returns:
        json response for updating one or more asset/classification

    Modules:
        assets
        classifications

    URL Example:
        >>> url_1 = 'http://server/v8/assets'
        >>> url_2 = 'http://server/v8/classifications'

    Data Example:
        [{'PK': 20773,
        'ID': 'SHI-V-1405',
        'Name': 'V-1405 Flash Separator',
        'IsLocation': False,
        'Vicinity': 'SHNR-PID-1104',
        'Icon': 'iconlib/CL/classifications/cylindar_g.gif',
        'UDFChar9': 'SHI-V-1405',
        'ParentRef': {'ID': 'SHI-INLET FLASH GAS AREA'},
        'ClassificationRef': {'ID': 'V'},
        'RepairCenterRef': {'ID': 'SA-HUBS-SHI'},
        'ShopRef': {'ID': 'SA-HUBS-SHI-OPS'},
        'TypeDetails': {'Value': 'A'}}]

    Required:
        PK -- Use _get() to retrieve asset/classification PK

    """

    url = f"http://{config.server}/v8/{module}"
    r = requests.put(url, auth=auth, json=data)

    if r.ok == True:
        print(
            f"Connection Successful!\nStatus Code: {r.status_code}\nThe {module[:-1]} has been updated\n"
        )
    else:
        print(f"Connection NOT Successful\nStatus Code: {r.status_code}\n")

    _resp = r.json()

    return _resp
