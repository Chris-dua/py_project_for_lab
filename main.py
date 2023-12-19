import re
from math import radians, cos, sin, asin, sqrt

def dms_to_dd(dms):
    """将度分秒转换为十进制度数"""
    # 使用正则表达式匹配度、分、秒和方向
    match = re.match(r"([NSWE])(\d+)[°](\d+)[′](\d+)[″]", dms)
    if not match:
        raise ValueError("Invalid DMS format")

    direction, degrees, minutes, seconds = match.groups()

    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction in ('S', 'W'):
        dd *= -1
    return dd

def haversine(lon1, lat1, lon2, lat2):
    """计算两个点的大圆距离"""
    # 将十进制度数转换为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # 使用哈弗赛公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # 地球半径（以海里为单位）
    r = 3440.065 # 这是地球半径的海里数
    return c * r


# 给定的坐标点
coord1_longitude = 'E36°07′42″'  # 应该是经度
coord1_latitude = 'N68°47′48″″'   # 应该是纬度
coord2_longitude = 'E37°28′17″'  # 应该是经度
coord2_latitude = 'N73°29′30″'   # 应该是纬度

# 将DMS坐标转换为十进制度数
lon1 = dms_to_dd(coord1_longitude)
lat1 = dms_to_dd(coord1_latitude)
lon2 = dms_to_dd(coord2_longitude)
lat2 = dms_to_dd(coord2_latitude)

# 计算距离
distance = haversine(lon1, lat1, lon2, lat2)
rounded_distance = round(distance, 2)

print(f"The distance between the two coordinates is {rounded_distance} nautical miles.")
