from math import sin, cos, sqrt, atan2, radians

def dms_to_decimal(dms):
    # 判断是N/S还是E/W
    direction = 1 if (dms[0] in ['N', 'E']) else -1

    # 分割度分秒
    parts = dms[1:-1].split('°')
    degrees = float(parts[0])

    # 分割分和秒
    minutes_parts = parts[1].split('′')
    minutes = float(minutes_parts[0])

    seconds_parts = minutes_parts[1].split('″')
    seconds = float(seconds_parts[0])

    # 计算总的十进制度数
    decimal = direction * (degrees + minutes / 60.0 + seconds / 3600.0)

    return decimal

def haversine_distance(coord1, coord2):
    # 使用 Haversine 公式计算两点之间的距离（单位：千米）
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # 将经纬度转换为弧度
    lat1_rad, lon1_rad = map(lambda x: x * (3.14159265358979323846 / 180), [lat1, lon1])
    lat2_rad, lon2_rad = map(lambda x: x * (3.14159265358979323846 / 180), [lat2, lon2])

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = (pow(sin(dlat / 2), 2) + cos(lat1_rad) * cos(lat2_rad) * pow(sin(dlon / 2), 2))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 地球半径（单位：千米）
    radius = 6371.0

    # 计算距离并转换为海里
    distance_km = radius * c
    distance_nautical = distance_km / 1.852  # 1海里 = 1.852千米

    return distance_nautical

# 输入坐标
coord1_longitude = 'E36°07′42″'  # 应该是经度
coord1_latitude = 'N68°47′48″'   # 应该是纬度
coord2_longitude = 'E37°28′17″'  # 应该是经度
coord2_latitude = 'N73°29′30″'   # 应该是纬度

# 转换为十进制度数
coord1 = (dms_to_decimal(coord1_latitude), dms_to_decimal(coord1_longitude))
coord2 = (dms_to_decimal(coord2_latitude), dms_to_decimal(coord2_longitude))

# 计算距离
distance_in_nautical_miles = haversine_distance(coord1, coord2)

print("两点之间的距离（海里）:", distance_in_nautical_miles)
