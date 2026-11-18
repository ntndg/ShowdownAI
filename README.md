# ShowdownAI

[![CC BY-NC 4.0 License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

ShowdownAI is an external Brawl Stars bot with a refreshed interface and custom playstyles.

## Requirements

- **NVIDIA GPUs**
  - `setup.py` installs `onnxruntime-gpu` when an NVIDIA GPU is detected
  - Falls back to DirectML, then CPU, if CUDA does not load

- **AMD / Intel / iGPU**
  - DirectML on Windows (`onnxruntime-directml`)
  - CPU fallback if DirectML does not load

## Installation

You will need [Python 3.11.9](https://www.python.org/downloads/release/python-3119/).

### Windows

```sh
python setup.py install
```

### Other Platforms

ShowdownAI only supports Windows.


## Using ShowdownAI

> [!NOTE]
> **Note**: This open-source version runs in localhost mode. The cloud features have been disabled by default.

Run the bot:

```sh
python main.py
```

### Startup options

| Flag | Effect |
| --- | --- |
| *(none)* | Console visible, UI in the ShowdownAI desktop window |
| `--no-console` | Hides the console window, output goes to `pyla.log` in the current folder. Ignored when ShowdownAI is started from an existing terminal, so your own terminal is never hidden. |
| `--no-webapp` | Opens the UI in the default browser instead of the desktop window |

Playstyles still use the `.pyla` file format, so existing playstyle files keep working. The default playstyle is Showdown Follower.

## License keys

ShowdownAI only runs on computers that have a key. On first launch it shows a lock screen with a machine ID. To make a key for that computer:

```sh
python tools/generate_license.py MACHINE-ID path/to/private_key.pem
```

Paste the printed key into the lock screen. A key only works on the computer whose machine ID it was made for. Keep `private_key.pem` secret and never commit it: anyone who has it can make keys.

## License and credits

ShowdownAI is a modified fork of [PylaAI](https://github.com/PylaAI/PylaAI) by ivanyordanovgt, AngelFireLA, awarzu and contributors (including Maayan080), used under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Changes from the original include the ShowdownAI name, logo and a redesigned interface.

This project is **not permitted to be sold or monetized** under CC BY-NC 4.0.
