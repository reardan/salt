"""
Created by Wesley Reardan 2025
MIT License

References:
https://github.com/Veritasimo/sc2-scrapbook/blob/68028fdbc7ce67a394ba139746e82485ebbf4312/SALT.cs
"""

import sys
from collections import namedtuple

class BuildStep:
    def __init__(self, supply, minute, second, name, step_type=None, code=None):
        self.supply = supply
        self.minute = minute
        self.second = second
        self.name = name
        self.step_type = step_type
        self.code = code

class BuildOrder:
    def __init__(self, steps=None, title="", author="", description=""):
        self.steps = steps if steps is not None else []
        self.title = title
        self.author = author
        self.description = description

    def add_step(self, step):
        self.steps.append(step)

    def print(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        if self.description:
            print(f"Description: {self.description}")
        print("-" * 20)

        if not self.steps:
            return

        output_lines = []
        i = 0
        while i < len(self.steps):
            current_step = self.steps[i]
            count = 1
            j = i + 1
            # Grouping logic: check if next step has same time and name
            while j < len(self.steps) and \
                  self.steps[j].name == current_step.name and \
                  self.steps[j].minute == current_step.minute and \
                  self.steps[j].second == current_step.second:
                count += 1
                j += 1
            
            name = current_step.name
            if count > 1:
                name += f" x{count}"
                
            line = f"{current_step.supply:3d}\t{current_step.minute:d}:{current_step.second:02d}\t{name}"
            output_lines.append(line)
            
            i = j # Move index past the grouped items

        print("\n".join(output_lines))

class SaltParser:
    CHARACTERS = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
    MAPPING = {char: i for i, char in enumerate(CHARACTERS)}
    REVERSE_MAPPING = {i: char for char, i in MAPPING.items()}

    STRUCTURES = {
        0: "Armory", 1: "Barracks", 2: "Bunker", 3: "Command Center", 4: "Engineering Bay",
        5: "Factory", 6: "Fusion Core", 7: "Ghost Academy", 8: "Missile Turret",
        9: "Reactor (Barracks)", 10: "Reactor (Factory)", 11: "Reactor (Starport)",
        12: "Refinery", 13: "Sensor Tower", 14: "Starport", 15: "Supply Depot",
        16: "Tech Lab (Barracks)", 17: "Tech Lab (Factory)", 18: "Tech Lab (Starport)",
        19: "Assimilator", 20: "Cybernetics Core", 21: "Dark Shrine", 22: "Fleet Beacon",
        23: "Forge", 24: "Gateway", 25: "Nexus", 26: "Photon Canon", 27: "Pylon",
        28: "Robotics Bay", 29: "Robotics Facility", 30: "Stargate", 31: "Templar Archives",
        32: "Twilight Council", 33: "Baneling Nest", 34: "Evolution Chamber", 35: "Extractor",
        36: "Hatchery", 37: "Hydralisk Den", 38: "Infestation Pit", 39: "Nydus Network",
        40: "Roach Warren", 41: "Spawning Pool", 42: "Spine Crawler", 43: "Spire",
        44: "Spore Crawler", 45: "Ultralisk Cavern", 46: "Creep Tumor"
    }

    UNITS = {
        0: "Banshee", 1: "Battlecruiser", 2: "Ghost", 3: "Hellion", 4: "Marauder",
        5: "Marine", 6: "Medivac", 7: "Raven", 8: "Reaper", 9: "SCV", 10: "Siege Tank",
        11: "Thor", 12: "Viking", 14: "Carrier", 15: "Colossus", 16: "Dark Templar",
        17: "High Templar", 18: "Immortal", 19: "Mothership", 20: "Observer", 21: "Phoenix",
        22: "Probe", 23: "Sentry", 24: "Stalker", 25: "Void Ray", 26: "Zealot",
        27: "Corruptor", 28: "Drone", 29: "Hydralisk", 30: "Mutalisk", 31: "Overlord",
        32: "Queen", 33: "Roach", 34: "Ultralisk", 35: "Zergling", 38: "Infestor",
        39: "Warp Prism", 40: "Battle Hellion", 41: "Warhound", 42: "Widow Mine",
        43: "Mothership Core", 44: "Oracle", 45: "Tempest", 46: "Swarm Host", 47: "Viper",
        48: "Cyclone", 49: "Liberator", 50: "Disruptor", 51: "Adepts"
    }

    MORPHS = {
        0: "Orbital Command", 1: "Planetary Fortress", 2: "Warp Gate", 3: "Lair",
        4: "Hive", 5: "Greater Spire", 6: "Brood Lord", 7: "Baneling", 8: "Overseer",
        9: "Ravager", 10: "Lurker", 12: "Lurker Den", 13: "Archon"
    }

    UPGRADES = {
        0: "Terran Building Armor", 1: "Terran Infantry Armor", 2: "Terran Infantry Weapons",
        3: "Terran Ship Plating", 4: "Terran Ship Weapons", 5: "Terran Vehicle Plating",
        6: "Terran Vehicle Weapons", 7: "250mm Strike Cannons", 8: "Banshee - Cloaking",
        9: "Ghost - Cloaking", 10: "Hellion - Pre-igniter", 11: "Marine - Stimpack",
        12: "Raven - Seeker Missiles", 13: "Siege Tank - Siege Tech", 14: "Bunker - Neosteel Frame",
        15: "Marauder - Concussive Shells", 16: "Marine - Combat Shields", 17: "Reaper Speed",
        18: "Protoss Ground Armor", 19: "Protoss Ground Weapons", 20: "Protoss Air Armor",
        21: "Protoss Air Weapons", 22: "Protoss Shields", 23: "Sentry - Hallucination",
        24: "High Templar - Psi Storm", 25: "Stalker - Blink", 26: "Warp Gate Tech",
        27: "Zealot - Charge", 28: "Zerg Ground Carapace", 29: "Zerg Melee Weapons",
        30: "Zerg Flyer Carapace", 31: "Zerg Flyer Weapons", 32: "Zerg Missile Weapons",
        33: "Hydralisk - Grooved Spines", 34: "Overlord - Pneumatized Carapace",
        35: "Overlord - Ventral Sacs", 36: "Roach - Glial Reconstitution",
        38: "Roach - Tunneling Claws", 40: "Ultralisk - Chitinous Plating",
        41: "Zergling - Adrenal Glands", 42: "Zergling - Metabolic Boost", 44: "Burrow",
        45: "Centrifugal Hooks", 46: "Ghost - Moebius Reactor", 47: "Extended Thermal Lance",
        49: "Neural Parasite", 50: "Pathogen Gland", 51: "Battlecruiser - Behemoth Reactor",
        52: "Battlecruiser - Weapon Refit", 53: "Hi-Sec Auto Tracking",
        54: "Medivac - Caduceus Reactor", 55: "Raven - Corvid Reactor",
        56: "Raven - Durable Materials", 57: "Hellion - Transformation servos",
        58: "Carrier - Graviton Catapult", 59: "Observer - Gravatic Boosters",
        60: "Warp Prrism - Gravatic Drive", 61: "Oracle - Bosonic Core",
        62: "Tempest - Gravity Sling", 64: "Swarm Host - Evolve Enduring Locusts",
        65: "Hydralisk - Muscular Augments", 66: "Drilling claws", 67: "Anion Pulse-Crystals",
        68: "Flying Locusts", 69: "Seismic Spines", 71: "Targeting Optics",
        72: "Advanced Ballistics", 73: "Resonating Glaives"
    }

    def __init__(self):
        self._reverse_name_map = {}
        self._populate_reverse_map()

    def _populate_reverse_map(self):
        for code, name in self.STRUCTURES.items(): self._reverse_name_map[name] = (0, code)
        for code, name in self.UNITS.items(): self._reverse_name_map[name] = (1, code)
        for code, name in self.MORPHS.items(): self._reverse_name_map[name] = (2, code)
        for code, name in self.UPGRADES.items(): self._reverse_name_map[name] = (3, code)

    def _get_name(self, step_type, code):
        if step_type == 0: return self.STRUCTURES.get(code, "Unknown")
        if step_type == 1: return self.UNITS.get(code, "Unknown")
        if step_type == 2: return self.MORPHS.get(code, "Unknown")
        if step_type == 3: return self.UPGRADES.get(code, "Unknown")
        return "Unknown"

    def parse(self, salt_string):
        parts = salt_string.split('~')
        if len(parts) != 2:
            print("Invalid SALT string format.")
            return BuildOrder()

        meta_part = parts[0]
        encoded_data = parts[1]

        title, author, description = "", "", ""
        if meta_part.startswith('$'):
            meta_part = meta_part[1:]
        
        meta_items = meta_part.split('|')
        if len(meta_items) >= 3:
            title = meta_items[0]
            author = meta_items[1]
            description = meta_items[2]

        build_order = BuildOrder(title=title, author=author, description=description)
        minimum_supply = 5

        i = 0
        while i + 4 < len(encoded_data):
            chunk = encoded_data[i:i+5]
            
            supply_char, min_char, sec_char, type_char, code_char = chunk
            
            supply = self.MAPPING.get(supply_char, 0)
            if supply > 0:
                supply += minimum_supply - 1
                
            minute = self.MAPPING.get(min_char, 0)
            second = self.MAPPING.get(sec_char, 0)
            step_type = self.MAPPING.get(type_char, -1)
            code = self.MAPPING.get(code_char, -1)
            
            name = self._get_name(step_type, code)
            step = BuildStep(supply, minute, second, name, step_type, code)
            build_order.add_step(step)
            
            i += 5
        return build_order

    def encode(self, build_order, title="", author="", description=""):
        encoded_steps = []
        minimum_supply = 5
        for step in build_order.steps:
            supply_val = 0
            if step.supply > 0:
                supply_val = step.supply - minimum_supply + 1

            step_type, code = self._reverse_name_map.get(step.name, (None, None))
            if step_type is None:
                print(f"Warning: Could not find mapping for '{step.name}'. Skipping.")
                continue

            chars = [
                self.REVERSE_MAPPING.get(supply_val, ' '),
                self.REVERSE_MAPPING.get(step.minute, ' '),
                self.REVERSE_MAPPING.get(step.second, ' '),
                self.REVERSE_MAPPING.get(step_type, ' '),
                self.REVERSE_MAPPING.get(code, ' ')
            ]
            encoded_steps.append("".join(chars))
        
        metadata = f"|{author}|{description}|"
        # This is a simplified version of the header.
        # The first part is often a build number or unique ID.
        # For now, we'll use the title.
        return f"${title}{metadata}~{''.join(encoded_steps)}"


if __name__ == "__main__":
    parser = SaltParser()
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                salt_string = f.read().strip()
                build_order = parser.parse(salt_string)
                build_order.print()
        except FileNotFoundError:
            print(f"Error: File not found at {filename}")
    else:
        example_salt = "$196809|spawningtool.com||~+ C D+ O!?+!! I.!; C/!P!@/!P!@/!R!C5!Z!?9\"7!@9\"7!@=\"C!?G#'\"#I#/ HI#2 CI#2 CN#N DM#R#BM#W!AM#W!AM#W!AM#W!AQ$%\"(_%%#C"
        print("--- Parsing and Printing Build Order ---")
        build_order = parser.parse(example_salt)
        build_order.print()

        print("\n--- Encoding Build Order and Printing SALT String ---")
        encoded_string = parser.encode(build_order, title=build_order.title, author=build_order.author, description=build_order.description)
        print(encoded_string)

        print("\n--- Verifying: Parsing the new SALT string ---")
        verified_build_order = parser.parse(encoded_string)
        verified_build_order.print()
