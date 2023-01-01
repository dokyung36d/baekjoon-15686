import sys

n,m=sys.stdin.readline().split(" ")
n=int(n)
m=int(m)
num_chicken=0
chicken_locations=[]
home_locations=[]

info_list=[]
for i in range(n):
    new_list=list(sys.stdin.readline().split(" "))
    for j in range(n):
        new_list[j] = int(new_list[j])
        if new_list[j] == 2:
            num_chicken+=1
            chicken_locations.append([i, j])
        
        elif new_list[j] == 1:
            home_locations.append([i, j])
    info_list.append(new_list)


num_haveto_delete_chicken=num_chicken-m



#단순히 best인 것만을 선택-> greedy 알고리즘 -> 추후에 문제가 생길수도 있음
#일단 dfs로 결과값을 하나 구한 다음, 브루트포스로 가다가 이미 값이 좋지 않으면 바로 손절
#치킨집이 줄어들수록 거리는 계속해서 증가함
#현재 우리는 거리의 최솟값을 구하고 싶음

def find_total_distance(home_location_list, chicken_location_list): #나중에 delete_chicken제거
    total_distance=0                                                #ex1 case에 너무 복잡해짐

    for home_location in home_location_list:
        home_chicken_distance_list=[]

        for chicken_location in chicken_location_list:
            home_chicken_distance_list.append(abs(home_location[0]-chicken_location[0]) + abs(home_location[1]-chicken_location[1]))
        total_distance += min(home_chicken_distance_list)

    return total_distance

current_distance = find_total_distance(home_locations, chicken_locations) #문제 없음
min_distance=10**10

def find_best_dfs(distance,num_ckicken_deleted, remain_chicken_locations):
    global min_distance
    if num_ckicken_deleted == num_haveto_delete_chicken: #삭제해야 하는 갯수에 도달하면 return 한다.
        return distance                                  #이전 과정들은 단지 어떤 치킨집을 제거할 것인지를 결정하는 과정
    
    for remain_chicken in remain_chicken_locations:
        chicken_deleted_list=remain_chicken_locations.copy()
        chicken_deleted_list.remove(remain_chicken)
        new_distance=find_total_distance(home_locations, chicken_deleted_list)
        if new_distance>min_distance:
            continue
        new_distance=find_best_dfs(new_distance, num_ckicken_deleted+1, chicken_deleted_list)
        if new_distance< min_distance:
            min_distance = new_distance
    
    return min_distance
#발상의 전환 -> 치킨집을 전부 제거하고 최대 m개를 새로 개업한다면?

def insort_right(a, x, lo=0, hi=None):
    """Insert item x in list a, and keep it sorted assuming a is sorted.
    If x is already in a, insert it to the right of the rightmost x.
    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x[0] < a[mid][0]:
            hi = mid
        else:
            lo = mid+1
    a.insert(lo, x)

def find_best_bfs():
    global min_distance
    candidate_list=[]
    candidate_list.append([0, current_distance, chicken_locations]) #[num_deleted, distance, remain_chicken_locations]

    while candidate_list:
        candidate=candidate_list[0]
        candidate_list=candidate_list[1:] #제일 앞에 것을 제거

        if candidate[0] == num_haveto_delete_chicken: #이미 치킨집을 다 제거한 경우
            if candidate[1] < min_distance:
                min_distance=candidate[1]
            continue

        for chicken_location in candidate[2]:
            after_delete_chicken_locations=candidate[2].copy()
            after_delete_chicken_locations.remove(chicken_location)
            new_candidate_distance=find_total_distance(home_locations, after_delete_chicken_locations)
            if new_candidate_distance > min_distance: #치킨집을 제거할수록 거리는 증가하는데 이미 넘어서면 가망이 없음
                continue
            new_candidate=[candidate[0]+1, new_candidate_distance, after_delete_chicken_locations]
            insort_right(candidate_list, new_candidate)
    
    return min_distance
