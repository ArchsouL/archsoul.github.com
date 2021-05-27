import sys, requests
from datetime import datetime
from github import Github

url = 'https://api.place.naver.com/graphql'
header = {'content-type': 'application/json'}

query = '''[{"operationName":"vaccineList","variables":{"input":{"keyword":"코로나백신위탁의료기관","x":"XPOS","y":"YPOS"},"businessesInput":{"start":0,"display":100,"deviceType":"mobile","x":"XPOS","y":"YPOS","sortingOrder":"distance"},"isNmap":false,"isBounds":false},"query":"query vaccineList($input: RestsInput, $businessesInput: RestsBusinessesInput, $isNmap: Boolean\u0021, $isBounds: Boolean\u0021) {\\n  rests(input: $input) {\\n    businesses(input: $businessesInput) {\\n      total\\n      vaccineLastSave\\n      isUpdateDelayed\\n      items {\\n        id\\n        name\\n        dbType\\n        phone\\n        virtualPhone\\n        hasBooking\\n        hasNPay\\n        bookingReviewCount\\n        description\\n        distance\\n        commonAddress\\n        roadAddress\\n        address\\n        imageUrl\\n        imageCount\\n        tags\\n        distance\\n        promotionTitle\\n        category\\n        routeUrl\\n        businessHours\\n        x\\n        y\\n        imageMarker @include(if: $isNmap) {\\n          marker\\n          markerSelected\\n          __typename\\n        }\\n        markerLabel @include(if: $isNmap) {\\n          text\\n          style\\n          __typename\\n        }\\n        isDelivery\\n        isTakeOut\\n        isPreOrder\\n        isTableOrder\\n        naverBookingCategory\\n        bookingDisplayName\\n        bookingBusinessId\\n        bookingVisitId\\n        bookingPickupId\\n        vaccineQuantity {\\n          quantity\\n          quantityStatus\\n          vaccineType\\n          vaccineOrganizationCode\\n          __typename\\n        }\\n        __typename\\n      }\\n      optionsForMap @include(if: $isBounds) {\\n        maxZoom\\n        minZoom\\n        includeMyLocation\\n        maxIncludePoiCount\\n        center\\n        __typename\\n      }\\n      __typename\\n    }\\n    queryResult {\\n      keyword\\n      vaccineFilter\\n      categories\\n      region\\n      isBrandList\\n      filterBooking\\n      hasNearQuery\\n      isPublicMask\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"}]'''

def get_github_repo(access_token, repository_name):
    """
    github repo object를 얻는 함수
    :param access_token: Github access token
    :param repository_name: repo 이름
    :return: repo object
    """
    g = Github(access_token)
    repo = g.get_user().get_repo(repository_name)
    return repo
  
def upload_github_issue(repo, title, body):
  """
  해당 repo에 title 이름으로 issue를 생성하고, 내용을 body로 채우는 함수
  :param repo: repo 이름
  :param title: issue title
  :param body: issue body
  :return: None
  """
  repo.create_issue(title=title, body=body)

if __name__ == '__main__':
#   if len(sys.argv) <3:
#       print('> Usage cmd [xpos] [ypox]')
#       exit(0)
  pos = [37.545152, 127.075241]
  query_xy=query.replace('XPOS', pos[0]).replace('YPOS', pos[1]).encode('UTF-8')
  resp = requests.post(url, headers=header,data=query_xy)

  r = resp.json()
  d = r[0]['data']['rests']['businesses']
  h_list = []
  for i in d['items']:
    #if int(i['vaccineQuantity']['quantity']) <1:
    #  continue
    h_list.append([i['name'],'[',i['commonAddress'], i['address'].split()[0],']', i['vaccineQuantity']['quantity']])

  today = datetime.datetime.now(datetime.timezone.utc)
  today_data = today.astimezone().strftime('%m-%d %H')
  
  repository_name = "archsoul.github.com"
  issue_title = f"No Show Vaccine Noti ({today_data})"
  
  access_token = os.environ['MY_GITHUB_TOKEN']
  repo = get_github_repo(access_token, repository_name)
  upload_github_issue(repo, issue_title, h_list)
  print("Upload Github Issue Success!")

  
