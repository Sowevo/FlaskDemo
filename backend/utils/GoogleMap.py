import json

import requests
from flask import current_app


def places_search_text(keyword):
    """
    :param keyword:
    :return:
    """
    headers = {
        'X-Goog-Api-Key': current_app.config['GOOGLE_API_KEY'],
        'X-Goog-FieldMask': 'places.id,places.displayName,places.addressComponents,places.plusCode,places.location,'
                            'places.rating,places.googleMapsUri,places.websiteUri,places.editorialSummary,'
                            'places.formattedAddress',
        'Content-Type': 'application/json'
    }

    url = "https://places.googleapis.com/v1/places:searchText"

    payload = json.dumps({
        "textQuery": keyword,
        "languageCode": "ja",
        "maxResultCount": 10,
    })

    response = requests.request("POST", url, headers=headers, data=payload)

    #     返回值的描述:
    #     id:就是id
    #     name:还是id啦
    #     displayName:显示名称啦...日语的啦
    #     addressComponents:结构化的地址信息
    #     formattedAddress:格式化的地址信息
    #     plusCode:就是plusCode啦
    #     location:经纬度啦
    #     rating:评分啦
    #     googleMapsUri:访问链接啦!
    #     websiteUri:官网啦
    #     photos:https://places.googleapis.com/v1/{拼进去name}/media?maxHeightPx=400&maxWidthPx=400&key={拼进去key}
    return response.json()
