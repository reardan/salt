# SALT Encoding Parser/Encoder for StarCraft 2

A Python library for parsing and encoding SALT (StarCraft Action List Timestamp) strings, which are used to represent StarCraft 2 build orders in a compact, encoded format.

## Overview

SALT encoding is a compact format for storing and sharing StarCraft 2 build orders. This library provides functionality to:
- Parse SALT encoded strings into readable build orders
- Encode build orders back into SALT format
- Display build orders in a human-readable format with proper grouping

## Features

- **Complete SALT Support**: Parse and encode SALT strings with full metadata support
- **Comprehensive Coverage**: Includes all StarCraft 2 structures, units, morphs, and upgrades
- **Smart Grouping**: Automatically groups identical actions at the same time for cleaner display
- **Metadata Handling**: Supports title, author, and description metadata
- **Command Line Interface**: Can be used as a standalone script

## Installation

Simply download the `salt_parser.py` file and import it into your Python project.

## Usage

### Basic Parsing

```python
from salt_parser import SaltParser

parser = SaltParser()

# Parse a SALT string
salt_string = "$196809|spawningtool.com||~+ C D+ O!?+!! I.!; C/!P!@/!P!@/!R!C5!Z!?9\"7!@9\"7!@=\"C!?G#'\"#I#/ HI#2 CI#2 CN#N DM#R#BM#W!AM#W!AM#W!AM#W!AQ$%\"(_%%#C"
build_order = parser.parse(salt_string)

# Print the build order
build_order.print()
```

### Encoding Build Orders

```python
from salt_parser import BuildOrder, BuildStep, SaltParser

# Create a build order
build_order = BuildOrder(
    title="Example Build", 
    author="Player", 
    description="A sample build order"
)

# Add steps
build_order.add_step(BuildStep(12, 0, 5, "SCV"))
build_order.add_step(BuildStep(13, 0, 17, "SCV"))
build_order.add_step(BuildStep(14, 0, 25, "Supply Depot"))

# Encode to SALT format
parser = SaltParser()
salt_string = parser.encode(build_order, "Example Build", "Player", "A sample build order")
print(salt_string)
```

### Command Line Usage

Run the script directly to see an example:

```bash
python salt_parser.py
```

Or parse a SALT string from a file:

```bash
python salt_parser.py build_order.txt
```

## SALT Format Structure

SALT strings have the following format:
```
$<title>|<author>|<description>|~<encoded_data>
```

- **Metadata Section**: Contains title, author, and description separated by pipes (`|`)
- **Separator**: Tilde (`~`) separates metadata from encoded data
- **Encoded Data**: 5-character chunks representing each build step:
  - Character 1: Supply count
  - Character 2: Minute
  - Character 3: Second
  - Character 4: Step type (0=Structure, 1=Unit, 2=Morph, 3=Upgrade)
  - Character 5: Item code

## Supported Items

The library includes comprehensive mappings for:

### Structures (47 items)
- Terran: Command Center, Barracks, Factory, Starport, etc.
- Protoss: Nexus, Gateway, Robotics Facility, Stargate, etc.
- Zerg: Hatchery, Spawning Pool, Roach Warren, Spire, etc.

### Units (52 items)
- All standard units from all three races
- Includes workers (SCV, Probe, Drone)

### Morphs (14 items)
- Unit morphs: Baneling, Brood Lord, Archon, etc.
- Structure morphs: Orbital Command, Warp Gate, Lair, Hive, etc.

### Upgrades (74 items)
- Combat upgrades (weapons, armor)
- Ability upgrades (Stimpack, Blink, Burrow)
- Technology upgrades

## Classes

### `BuildStep`
Represents a single action in a build order.

**Attributes:**
- `supply`: Supply count when action occurs
- `minute`: Minute timestamp
- `second`: Second timestamp
- `name`: Human-readable name of the action
- `step_type`: Type code (0-3)
- `code`: Item code within type

### `BuildOrder`
Container for a complete build order.

**Attributes:**
- `steps`: List of BuildStep objects
- `title`: Build order title
- `author`: Author name
- `description`: Build description

**Methods:**
- `add_step(step)`: Add a BuildStep to the order
- `print()`: Display the build order in formatted output

### `SaltParser`
Main parser class for encoding/decoding SALT strings.

**Methods:**
- `parse(salt_string)`: Convert SALT string to BuildOrder object
- `encode(build_order, title, author, description)`: Convert BuildOrder to SALT string

## Example Output

```
Title: Example Build
Author: spawningtool.com
Description: 
--------------------
 12	0:05	SCV
 13	0:17	SCV
 14	0:25	Supply Depot
 15	0:29	SCV
 16	0:41	SCV
 17	0:50	Barracks
 18	0:53	SCV
 19	1:05	SCV
```

## Requirements

- Python 3.6+
- No external dependencies

## License

MIT License - Created by Wesley Reardan 2025

## References

Based on the SALT encoding specification from the StarCraft 2 community. Original implementation reference: https://github.com/Veritasimo/sc2-scrapbook/blob/68028fdbc7ce67a394ba139746e82485ebbf4312/SALT.cs

## Contributing

Feel free to submit issues and enhancement requests!
