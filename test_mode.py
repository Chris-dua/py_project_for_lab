from typing import Optional, Generator, List
from pathlib import Path
import pandas as pd
from geopy import Point, distance
import re
from math import radians, cos, sin, asin, sqrt

# const 变量，到时候可以放到另外一个file中
data_path = Path('/Users/chris/Desktop/data_for_NWPU')
equipment_file_name = {
    'command': None,
    'decision': None,
    'judgment': None,
    'reconnaissance': 'Reconnaissance-equip-info.xlsx',
    'strike': 'strike-equip-info.xlsx'
}
combat_mission_file_name = {
    'combat_mission_info.xlsx'
}
type_name = {
    'command_control': 'command',
    'decision': 'decision',
    'judgment': 'judgment',
    'reconnaissance': 'reconnaissance',
    'strike': 'strike'
}

area = {'空中': '飞机、直升机、导弹',
        '海面': '潜艇'}


# 作战任务基类
class CombatMission:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def execute(self):
        raise NotImplementedError("You should implement this method!")


# 作战任务的子类
class CommandMission(CombatMission):
    pass


class DecisionMission(CombatMission):
    pass


class JudgmentMission(CombatMission):
    pass


class ReconnaissanceMission(CombatMission):
    pass


class StrikeMission(CombatMission):
    pass


# 作战能力基类
class CombatCapability:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def activate(self):
        raise NotImplementedError("You should implement this method!")


# 作战能力的子类
class CommandCapability(CombatCapability):
    pass


class DecisionCapability(CombatCapability):
    pass


class JudgmentCapability(CombatCapability):
    pass


class ReconnaissanceCapability(CombatCapability):
    pass


class StrikeCapability(CombatCapability):
    pass


# 武器装备基类
class WeaponEquipment:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def fire(self):
        raise NotImplementedError("You should implement this method!")


# 武器装备的子类
class CommandControlEquipment(WeaponEquipment):
    pass


class DecisionEquipment(WeaponEquipment):
    pass


class JudgmentEquipment(WeaponEquipment):
    pass


class ReconnaissanceEquipment(WeaponEquipment):
    pass


class StrikeEquipment(WeaponEquipment):
    pass


# 工厂类
class WarfareFactory:
    @staticmethod
    def create_mission(mission_type, **kwargs):
        missions = {
            'command': CommandMission,
            'decision': DecisionMission,
            'judgment': JudgmentMission,
            'reconnaissance': ReconnaissanceMission,
            'strike': StrikeMission
        }
        mission_class = missions.get(mission_type)
        if mission_class:
            return mission_class(**kwargs)
        raise ValueError(f"Unknown mission type: {mission_type}")

    @staticmethod
    def create_capability(capability_type, **kwargs):
        capabilities = {
            'command': CommandCapability,
            'decision': DecisionCapability,
            'judgment': JudgmentCapability,
            'reconnaissance': ReconnaissanceCapability,
            'strike': StrikeCapability
        }
        capability_class = capabilities.get(capability_type)
        if capability_class:
            return capability_class(**kwargs)
        raise ValueError(f"Unknown capability type: {capability_type}")

    @staticmethod
    def create_equipment(equipment_type, **kwargs):
        equipments = {
            'command_control': CommandControlEquipment,
            'decision': DecisionEquipment,
            'judgment': JudgmentEquipment,
            'reconnaissance': ReconnaissanceEquipment,
            'strike': StrikeEquipment
        }
        equipment_class = equipments.get(equipment_type)
        if equipment_class:
            return equipment_class(**kwargs)
        raise ValueError(f"Unknown equipment type: {equipment_type}")


def read_equipment_info_from_datafile(equipment_type: str, filename: str, filepath: Path) -> list:
    rec_equip_path = next(filepath.rglob(filename), None)
    if rec_equip_path is None:
        raise FileNotFoundError(f'{filename} not found in {filepath}.')
    df = None
    try:
        df = pd.read_excel(rec_equip_path)
    except Exception as err:
        print(f"Read Excel file error: {err}")
    rec_equipment_list = []
    if df is not None:
        for index, row in df.iterrows():
            equipment_data = dict(row)
            rec_equipment_list.append(WarfareFactory.create_equipment(equipment_type, **equipment_data))
    return rec_equipment_list


def read_capability_info_from_file(filepath: Path):
    pass


def read_mission_info_from_file(mission_type: str, filename: str, filepath: Path) -> list:
    acquire_file_path = next(filepath.rglob(filename), None)
    if acquire_file_path is None:
        raise FileNotFoundError(f'{filename} not found in {filepath}.')
    df = None
    try:
        df = pd.read_excel(acquire_file_path)
    except Exception as err:
        print(f"Read Excel file error: {err}")

    task_info_list = []
    if df is not None:
        for index, row in df.iterrows():
            mission_data = dict(row)
            task_info_list.append(WarfareFactory.create_mission(mission_type, **mission_data))
    return task_info_list


def dms_to_decimal(dms):
    match = re.match(r"([NSWE])?(\d+)[°](\d+)[′](\d+)[″]", dms)
    if not match:
        raise ValueError("Invalid DMS format")
    direction, degrees, minutes, seconds = match.groups()
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction in ('S', 'W'):
        dd *= -1
    return dd


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3440.065
    return c * r


def get_dist(target, rec_equipment_list) -> dict:
    dist_dict = {}
    for equipment in rec_equipment_list:
        value = equipment.__dict__['Loading platforms']
        dist_name = value + ' ' + target.__dict__['Target name']
        if dist_name not in dist_dict:
            coord1_latitude = dms_to_decimal(target.__dict__['Target Latitude'])
            coord1_longitude = dms_to_decimal(target.__dict__['Target Longitudes'])
            coord2_latitude = dms_to_decimal(equipment.__dict__['Latitude'])
            coord2_longitude = dms_to_decimal(equipment.__dict__['Longitudes'])
            dist = haversine(coord1_longitude, coord1_latitude, coord2_longitude, coord2_latitude)
            dist_dict[dist_name] = round(dist, 2)
    return dist_dict


def get_platform_height(rec_equipment_list) -> dict:
    platform_height = {}
    for rec_equipment in rec_equipment_list:
        platform_height[rec_equipment.__dict__['Loading platforms']] = rec_equipment.__dict__['Altitude']
    return platform_height


def get_reconnaissance_equipment(mission, rec_equipment_list: list, dist_all: dict):
    rec_equipment_res = []
    for equipment in rec_equipment_list:
        target_all_name = equipment.__dict__['Target type']
        for target_name in target_all_name.split('、'):
            for typename in area[target_name].split('、'):
                if typename == mission.__dict__['Target type']:
                    break
            else:
                break
        dist_dict = dist_all[mission.__dict__['Target name']]
        dist_name = equipment.__dict__['Loading platforms'] + ' ' + mission.__dict__['Target name']
        if equipment.__dict__['Detection distance'] < dist_dict[dist_name]:
            break
        rec_equipment_res.append(equipment)
    return rec_equipment_res


def get_strike_equipment(mission, strike_equipment_list: list, dist_all: dict, platform_height_list: dict) -> list:
    strike_equipment_res = []
    for equipment in strike_equipment_list:
        target_name = equipment.__dict__['Target type']
        for typename in target_name.split('、'):
            if typename == mission.__dict__['Target type']:
                break
        else:
            continue
        dist_dict = dist_all[mission.__dict__['Target name']]
        dist_name = equipment.__dict__['Loading platforms'] + ' ' + mission.__dict__['Target name']
        if equipment.__dict__['Maximum range range'] < dist_dict[dist_name]:
            continue
        if equipment.__dict__['Minimum range range'] > dist_dict[dist_name]:
            continue
        if equipment.__dict__['Hit rate'] < mission.__dict__['Target destruction value']:
            continue
        if equipment.__dict__['Target Maximum speed'] < mission.__dict__['Target speed']:
            continue
        if equipment.__dict__['Minimum target height'] > mission.__dict__['Target Altitude']:
            continue
        if equipment.__dict__['Target Maximum height'] < mission.__dict__['Target Altitude']:
            continue
        if equipment.__dict__['Minimum Launch Height'] > platform_height_list[equipment.__dict__['Loading platforms']]:
            continue
        if equipment.__dict__['Maximum firing height Shooting Height'] < platform_height_list[equipment.__dict__['Loading platforms']]:
            continue
        strike_equipment_res.append(equipment)

    return strike_equipment_res


def mission_equipment_mapping_rule(mission_info_list: list, strike_equipment_info_list: list,
                                   rec_equipment_info_list: list):
    strike_equipment_dict = {}
    rec_equipment_dict = {}
    dist_all = {}

    for mission in mission_info_list:
        dist_all[mission.__dict__['Target name']] = get_dist(mission, rec_equipment_info_list)
    platform_height_list = get_platform_height(rec_equipment_info_list)

    for mission in mission_info_list:
        strike_equipment = get_strike_equipment(mission, strike_equipment_info_list, dist_all, platform_height_list)
        strike_equipment_dict[mission] = strike_equipment
        rec_equipment = get_reconnaissance_equipment(mission, rec_equipment_info_list, dist_all)
        rec_equipment_dict[mission] = rec_equipment

    return strike_equipment_dict, rec_equipment_dict



# def mission_capability_mapping_rule():
#     pass
#
#
# def capability_equipment_mapping_rule():
#     pass
#
#
# def equipment_cooperation_rule():
#     pass
#
#
# def chain_coordination_rules():
#     pass


def optimal_chain_by_evaluation_rules(strike_equipment_list, rec_equipment_list, mission, judge_equipment, dist):
    t_weight = 0.3
    precision_weight = 0.3
    damage_weight = 0.4
    max_t = 0.1
    min_t = 0.03
    max_precision = 1.0
    min_precision = 0.525
    max_damage = 500.0
    min_damage = 0.1
    p_flag = 0.0
    name_res = []

    for strike_equipment in strike_equipment_list:
        for rec_equipment in rec_equipment_list:
            name = []
            dist_name = strike_equipment.__dict__['Loading platforms'] + ' ' + mission.__dict__['Target name']
            t = dist[dist_name] / (strike_equipment.__dict__['Target Maximum speed'] + mission.__dict__['Target speed'])
            precision = rec_equipment.__dict__['Reconnaissance accuracy']*strike_equipment.__dict__['Hit rate']
            damage = strike_equipment.__dict__['Injure value']
            t_new = 1.0 - (t - min_t) / (max_t - min_t)
            precision_new = (precision - min_precision) / (max_precision - min_precision)
            damage_new = 1.0 - (damage - min_damage) / (max_damage - min_damage)
            name.append(mission.__dict__['Target name'])
            name.append(rec_equipment.__dict__['Reconnaissance equipment'] + '(' + rec_equipment.__dict__['Loading platforms'] + ')')
            name.append(judge_equipment)
            name.append(strike_equipment.__dict__['Percussion equipment armaments'] + '(' + strike_equipment.__dict__['Loading platforms'] + ')')
            p = t_weight * t_new + precision_weight * precision_new + damage_weight * damage_new
            if p > p_flag:
                p_flag = p
                name_res = name
    return name_res


def main():
    equipment_type = type_name['reconnaissance']
    rec_equip_file_name = equipment_file_name[equipment_type]
    rec_equipment_info_list = read_equipment_info_from_datafile(equipment_type, rec_equip_file_name, data_path)

    equipment_type = type_name['strike']
    strike_equip_file_name = equipment_file_name[equipment_type]
    strike_equipment_info_list = read_equipment_info_from_datafile(equipment_type, strike_equip_file_name, data_path)

    mission_type = type_name['strike']
    strike_mission_file_name = 'combat_mission_info.xlsx'
    strike_mission_info_list = read_mission_info_from_file(mission_type, strike_mission_file_name, data_path)
    strike_equipment_dict, rec_equipment_dict = mission_equipment_mapping_rule(strike_mission_info_list,
                                                strike_equipment_info_list, rec_equipment_info_list)
    judge_equipment = 'A-100-Premier'
    columns = ['Mission name', 'Reconnaissance Equipment', 'Judgement equipment', 'Strike equipment']
    df = pd.DataFrame(columns=columns)

    for mission in strike_mission_info_list:
        dist = get_dist(mission, rec_equipment_info_list)
        name_res = optimal_chain_by_evaluation_rules(strike_equipment_dict[mission], rec_equipment_dict[mission], mission, judge_equipment, dist)
        temp_df = pd.DataFrame({
            'Mission name': [name_res[0]],
            'Reconnaissance Equipment': [name_res[1]],
            'Judgement equipment': [name_res[2]],
            'Strike equipment': [name_res[3]]
        })
        df = pd.concat([df, temp_df], ignore_index=True)
    excel_path = str(data_path) + '/mission_results.xlsx'
    df.to_excel(excel_path, index=False)


if __name__ == '__main__':
    main()
