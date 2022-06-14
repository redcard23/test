import json
import requests

key = input("YOUR REST_API_KEY: ")
source = input("출발지 주소는?(도로명 주소로 입력) ")
destination = input("도착지 주소는?(도로명 주소로 입력) ")
print('\n')
headers = { "Authorization" : "KakaoAK " + key }

#####출발지 주소의 x,y 좌표 값 가져오기#####
params = { "query" : source }

api_url = "https://dapi.kakao.com/v2/local/search/address.json"

result = requests.post(api_url, headers = headers, params = params)

if result.status_code == 200:
    response_body = json.loads(result.text) #결과 값 JSON 형식으로 변환
    s_x = response_body['documents'][0]['x']
    s_y = response_body['documents'][0]['y']

else:
    print("출발지의 좌표 정보를 찾는 중 에러가 발생했습니다. Error Code:" + str(result.status_code))

#####목적지 주소의 x,y 좌표 값 가져오기#####
params = { "query" : destination }

api_url = "https://dapi.kakao.com/v2/local/search/address.json"

result = requests.post(api_url, headers = headers, params = params)

if result.status_code == 200:
    response_body = json.loads(result.text) #결과 값 JSON 형식으로 변환
    d_x = response_body['documents'][0]['x']
    d_y = response_body['documents'][0]['y']

else:
    print("출발지의 좌표 정보를 찾는 중 에러가 발생했습니다. Error Code:" + str(result.status_code))

#####길 찾기#####
#distance를 km 단위로 변환 시켜주는 함수
def conv_dis(distance):
        if distance > 1000:
            result = str(round(guide_list[i+1]['distance']/1000,1))+"km"
        else:
            result = str(guide_list[i+1]['distance'])+"m"
        return result

params = {  "origin" : s_x+","+s_y,
            "destination" : d_x+","+d_y }
 
api_url = "https://apis-navi.kakaomobility.com/v1/directions"

result = requests.get(api_url, headers = headers, params = params)
    
if result.status_code == 200:
    response_body = json.loads(result.text) #결과 값 JSON 형식으로 변환
    print('출발지인 \"{}\"에서 목적지인 \"{}\"(으)로 가는 경로를 발견했습니다.'.format(source, destination))
    print('\n')
    guide_list = response_body['routes'][0]['sections'][0]['guides']
    i = 0

    for guide in guide_list:
        print(str(i)+".")

        if guide['name'] == "출발지":
            distance = conv_dis(guide_list[i+1]['distance'])
            print("출발지에서 출발합니다. 다음 지점까지, \"{}\" 쭉 직진하세요.".format(distance))

        elif guide['name'] == "목적지":
            print("목적지에 도착했습니다.")

        elif guide['name'] == "":
            distance = conv_dis(guide_list[i+1]['distance'])
            if guide['guidance'][-2:] == "방향":
                print("이번 지점에서 \"{}\"으로, 다음 지점까지, \"{}\" 쭉 직진하세요.".format(guide['guidance'],distance))
            elif guide['guidance'][-2:] == "입구" or guide['guidance'][-2:] == "출구":
                print("이번 지점에서 \"{}\"로 진입 후, 다음 지점까지, \"{}\" 쭉 직진하세요.".format(guide['name'],guide['guidance'],distance))                
            else:
                print("이번 지점에서 \"{}\" 후, 다음 지점까지, \"{}\" 쭉 직진하세요.".format(guide['guidance'],distance))

        else:
            distance = conv_dis(guide_list[i+1]['distance'])
            if guide['guidance'][-2:] == "방향":
                print("\"{}\"에서 \"{}\"으로, 다음 지점까지, \"{}\" 쭉 직진하세요.".format(guide['name'],guide['guidance'],distance))                
            elif guide['guidance'][-2:] == "입구" or guide['guidance'][-2:] == "출구":
                print("\"{}\"에서 \"{}\"로 진입 후, 다음 지점까지, \"{}\" 쭉 직진하세요.".format(guide['name'],guide['guidance'],distance))                
            else:
                print("\"{}\"에서 \"{}\" 후, 다음 지점까지, \"{}\" 쭉 직진하세요.".format(guide['name'],guide['guidance'],distance))

        print('\n')
        i += 1

else:
    print("길 찾기 정보를 찾는 중 에러가 발생했습니다. Error Code:" + str(result.status_code))