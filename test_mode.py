from typing import Optional, Generator, List
from pathlib import Path
import pandas as pd
from geopy import Point, distance

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
    def activate(self):
        print(f"{self.name} Command Capability activated.")


class DecisionCapability(CombatCapability):
    def activate(self):
        print(f"{self.name} Decision Capability activated.")


class JudgmentCapability(CombatCapability):
    def activate(self):
        print(f"{self.name} Judgment Capability activated.")


class ReconnaissanceCapability(CombatCapability):
    def activate(self):
        print(f"{self.name} Reconnaissance Capability activated.")


class StrikeCapability(CombatCapability):
    def activate(self):
        print(f"{self.name} Strike Capability activated.")


# 武器装备基类
class WeaponEquipment:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def fire(self):
        raise NotImplementedError("You should implement this method!")


# 武器装备的子类
class CommandControlEquipment(WeaponEquipment):
    def fire(self):
        print(f"{self.name} Command Control Equipment firing.")


class DecisionEquipment(WeaponEquipment):
    def fire(self):
        print(f"{self.name} Decision Equipment firing.")


class JudgmentEquipment(WeaponEquipment):
    def fire(self):
        print(f"{self.name} Judgment Equipment firing.")


class ReconnaissanceEquipment(WeaponEquipment):
    def fire(self):
        print(f"{self.name} Reconnaissance Equipment firing.")


class StrikeEquipment(WeaponEquipment):
    def fire(self):
        print(f"{self.name} Strike Equipment firing.")


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


def get_dist(target, rec_equipment_list) -> dict:
    dist_dict = {}
    for index, equipment in rec_equipment_list:
        value = equipment.__dict__['Loading platforms']
        dist_name = value + ' ' + target.__dict__['Target name']
        if dist_name not in dist_dict:
            coord1 = Point(latitude=target.__dict__['Target Latitude'], longitude=target.__dict__['Target Longitudes'])
            coord2 = Point(latitude=equipment.__dict__['Latitude'], longitude=equipment.__dict__['Longitudes'])
            dist = distance.distance(coord1, coord2, unit='nautical')
            dist_dict[dist_name] = dist
    return dist_dict


def get_platform_height(rec_equipment_list) -> dict:
    platform_height = {}
    for index, rec_equipment in rec_equipment_list:
        platform_height[rec_equipment.__dict__['Loading platforms']] = rec_equipment.__dict__['Altitude']
    return platform_height


def get_strike_equipment(mission, strike_equipment_list: list, dist_all: dict, platform_height_list: dict) -> list:
    strike_equipment_res = []
    for index, equipment in strike_equipment_list:
        target_name = equipment.__dict__['Target type']
        for typename in target_name.split('、'):
            if typename == mission.__dict__['Target type']:
                break
        else:
            break
        dist_dict = dist_all[mission.__dict__['Target name']]
        dist_name = equipment.__dict__['Loading platforms'] + ' ' + mission.__dict__['Targen name']
        if equipment.__dict__['Maximum'] < dist_dict[dist_name]:
            break
        if equipment.__dict__['Minimum range range'] > dist_dict[dist_name]:
            break
        if equipment.__dict__['Hit rate'] < mission.__dict__['Target destruction value']:
            break
        if equipment.__dict__['Target Maximum speed'] < mission.__dict__['Target speed']:
            break
        if equipment.__dict__['Minimum target height'] > mission.__dict__['Target Altitude']:
            break
        if equipment.__dict__['Target Maximum height'] < mission.__dict__['Target Altitude']:
            break
        if equipment.__dict__['Minimum Launch Height'] > platform_height_list[equipment.__dict__['Loading platforms']]:
            break
        if equipment.__dict__['Maximum firing height Shooting Height'] < platform_height_list.__dict__['Loading platforms']:
            break
        strike_equipment_res.append(equipment)

    return strike_equipment_res


def mission_equipment_mapping_rule(mission_info_list: list, strike_equipment_info_list: list,
                                   rec_equipment_info_list: list):
    strike_equipment_dict = {}
    dist_all = {}
    for index, mission in mission_info_list:
        dist_all[mission.__dict__['Target name']] = get_dist(mission, rec_equipment_info_list)
    platform_height_list = get_platform_height(rec_equipment_info_list)
    for index, mission in mission_info_list:
        strike_equipment = get_strike_equipment(mission, strike_equipment_info_list, dist_all, platform_height_list)
        strike_equipment_dict[mission] = strike_equipment



def mission_capability_mapping_rule():
    pass


def capability_equipment_mapping_rule():
    pass


def equipment_cooperation_rule():
    pass


def chain_coordination_rules():
    pass


def optimal_chain_by_evaluation_rules():
    pass


def main():
    equipment_type = type_name['reconnaissance']
    rec_equip_file_name = equipment_file_name[equipment_type]
    rec_equipment_info_list = read_equipment_info_from_datafile(equipment_type, rec_equip_file_name, data_path)

    equipment_type = type_name['strike']
    strike_equip_file_name = equipment_file_name[equipment_type]
    strike_equipment_info_list = read_equipment_info_from_datafile(equipment_type, strike_equip_file_name, data_path)

    mission_type = type_name['strike']
    strike_mission_file_name = 'combat_mission_info.xlsx'
    strike_mission_info_list = read_mission_info_from_file(mission_type, strike_equip_file_name, data_path)

    dist_all = {}
    for index, mission in strike_mission_info_list:
        dist_all[mission.__dict__['Target name']] = get_dist(mission, rec_equipment_info_list)

    platform_height_list = get_platform_height(rec_equipment_info_list)
