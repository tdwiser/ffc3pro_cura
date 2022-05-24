# Cura Profile for Flashforge Creator 3 Pro

**Acknowledgements:** Based on and heavily modified from [ArteFlux's Creator 3 profile](https://www.thingiverse.com/thing:4574596).

## Installation

Find your Cura settings directory:

- Windows: `%APPDATA%\cura\<version>`
- macOS: `~/Library/Application Support/cura/<version>/`
- Linux: `~/.cura/<version>/`
	
There should be subdirectories `definitions`, `extruders`, and `scripts`. Copy the files from this repository into the matching subdirectories, and then (re)start Cura.

The Creator 3 Pro seems to be unreasonably particular about G-Code format and order, so **a post-processing script is required** and must be manually activated from the Extensions->Post-Processing->Modify G-Code menu.
