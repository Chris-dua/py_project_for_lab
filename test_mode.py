from typing import Optional, Generator, List
from pathlib import Path
import pandas as pd

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
    def execute(self):
        print(f"{self.name} Command Mission executing.")


class DecisionMission(CombatMission):
    def execute(self):
        print(f"{self.name} Decision Mission executing.")


class JudgmentMission(CombatMission):
    def execute(self):
        print(f"{self.name} Judgment Mission executing.")


class ReconnaissanceMission(CombatMission):
    def execute(self):
        print(f"{self.name} Reconnaissance Mission executing.")


class StrikeMission(CombatMission):
    def execute(self):
        print(f"{self.name} Strike Mission executing.")


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


def read_equipment_info_from_datafile(equipment_type: str, filename: str, filepath: Path) -> []:
    rec_equip_path = next(filepath.rglob(filename), None)
    if rec_equip_path is None:
        raise FileNotFoundError(f'{filename} not found in {filepath}.')
    try:
        df = pd.read_excel(rec_equip_path)
    except Exception as err:
        print(f"Read Excel file error: {err}")
    rec_equipment_list = []
    for index, row in df.iterrows():
        equipment_data = dict(row)
        rec_equipment_list.append(WarfareFactory.create_equipment(equipment_type, **equipment_data))
    return rec_equipment_list


def read_capability_info_from_file(filepath: Path):
    pass


def read_mission_info_from_file(mission_type: str, filename: str, filepath: Path) -> []:
    acquire_file_path = next(filepath.rglob(filepath), None)
    if acquire_file_path is None:
        raise FileNotFoundError(f'{filename} not found in {filepath}.')
    try:
        df = pd.read_excel(acquire_file_path)
    except Exception as err:
        print(f"Read Excel file error: {err}")
    task_info_list = []
    for index, row in df.iterrows():
        mission_data = dict(row)
        task_info_list.append(WarfareFactory.create_mission(mission_type, **mission_data))
    return acquire_file_path

def get_strike_equipment(task, strike_equipment_list:[]):
    for index, equipment in strike_equipment_list:
        for key, value in equipment.__dict__.item():
            flag = False
            if key == 'Target type':
                for typename in value.split('、'):
                    if typename == task.__dict__['Target type']:
                        flag = True
                        break
            elif key == 'Maximum':
                pass



def mission_equipment_mapping_rule(mission_info: [], strike_equipment_info:[], rec_equipment_info:[]):
    for index, task in mission_info:
        for key, value in task.__dict__.items():
            pass


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

try:
    equipment_type = type_name['reconnaissance']
    rec_equip_file_name = equipment_file_name[equipment_type]
    rec_equipment_info_list = read_equipment_info_from_datafile(equipment_type, rec_equip_file_name, data_path)

    equipment_type = type_name['strike']
    strike_equip_file_name = equipment_file_name[equipment_type]
    strike_equipment_info_list = read_equipment_info_from_datafile(equipment_type, strike_equip_file_name, data_path)

    mission_type = type_name['strike']
    strike_mission_file_name = 'combat_mission_info.xlsx'
    strike_mission_info_list = read_mission_info_from_file(mission_type, strike_equip_file_name, data_path)


except ValueError as e:
    print(e)
