#!/usr/bin/python3


import requests
url = 'https://api.place.naver.com/graphql'
header = {'content-type': 'application/json'}

query = '''[{"operationName":"vaccineList","variables":{"input":{"keyword":"코로나백신위탁의료기관","x":"XPOS","y":"YPOS"},"businessesInput":{"start":0,"display":100,"deviceType":"mobile","x":"XPOS","y":"YPOS","sortingOrder":"distance"},"isNmap":false,"isBounds":false},"query":"query vaccineList($input: RestsInput, $businessesInput: RestsBusinessesInput, $isNmap: Boolean\u0021, $isBounds: Boolean\u0021) {\\n  rests(input: $input) {\\n    businesses(input: $businessesInput) {\\n      total\\n      vaccineLastSave\\n      isUpdateDelayed\\n      items {\\n        id\\n        name\\n        dbType\\n        phone\\n        virtualPhone\\n        hasBooking\\n        hasNPay\\n        bookingReviewCount\\n        description\\n        distance\\n        commonAddress\\n        roadAddress\\n        address\\n        imageUrl\\n        imageCount\\n        tags\\n        distance\\n        promotionTitle\\n        category\\n        routeUrl\\n        businessHours\\n        x\\n        y\\n        imageMarker @include(if: $isNmap) {\\n          marker\\n          markerSelected\\n          __typename\\n        }\\n        markerLabel @include(if: $isNmap) {\\n          text\\n          style\\n          __typename\\n        }\\n        isDelivery\\n        isTakeOut\\n        isPreOrder\\n        isTableOrder\\n        naverBookingCategory\\n        bookingDisplayName\\n        bookingBusinessId\\n        bookingVisitId\\n        bookingPickupId\\n        vaccineQuantity {\\n          quantity\\n          quantityStatus\\n          vaccineType\\n          vaccineOrganizationCode\\n          __typename\\n        }\\n        __typename\\n      }\\n      optionsForMap @include(if: $isBounds) {\\n        maxZoom\\n        minZoom\\n        includeMyLocation\\n        maxIncludePoiCount\\n        center\\n        __typename\\n      }\\n      __typename\\n    }\\n    queryResult {\\n      keyword\\n      vaccineFilter\\n      categories\\n      region\\n      isBrandList\\n      filterBooking\\n      hasNearQuery\\n      isPublicMask\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"}]'''

if __name__ == '__main__':
  import sys
  if len(sys.argv) <3:
      print('> Usage cmd [xpos] [ypox]')
      exit(0)
  query_xy=query.replace('XPOS', sys.argv[1]).replace('YPOS', sys.argv[2]).encode('UTF-8')
  resp = requests.post(url, headers=header,data=query_xy)

  r = resp.json()
  d = r[0]['data']['rests']['businesses']
  for i in d['items']:
    #if int(i['vaccineQuantity']['quantity']) <1:
    #  continue
    print (i['name'],'[',i['commonAddress'], i['address'].split()[0],']', i['vaccineQuantity']['quantity'])
