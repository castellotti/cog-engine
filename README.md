# Cog Engine

The **Cog Engine** is an open-source adventure game engine designed to make video game creation accessible to users without programming knowledge — targeting "a range from children to gurus." It provides a point-and-click graphical interface with photo-realistic room graphics, a clickable compass for navigation, and text-to-speech output, with a companion visual IDE for authoring game content.

Originally developed by [Steve Castellotti](https://github.com/castellotti) starting in 1999, the engine reached its v1.0 stable release in January 2002 after three years of development. This repository modernizes the codebase to run on contemporary systems via Docker.

---

## Features

- **No programming required** — games are authored entirely through the graphical Cog Development Application
- **Photo-realistic graphics** — room environments, close-up object views, and item icons
- **Point-and-click gameplay** — compass navigation, clickable inventory and room-object panels, graphical mouse pointers for actions
- **Text-to-Speech synthesis** — Festival TTS for all in-game text output
- **Rich event system** — conditional requirements and effects (pick up items, unlock rooms, play audio, trigger obstructions)
- **Portable game format** — games stored as `.cog` files, playable cross-platform
- **Visual game IDE** — editors for rooms, items, verbs, directions, obstructions, and events with live in-editor testing

## Example Game: Cycon Odyssey

[**Cycon Odyssey**](https://github.com/castellotti/cycon-odyssey) is the reference game built for the Cog Engine — a full adventure game over a decade in the making, featuring hand-drawn and photographed room graphics, item artwork, and a complete narrative. It serves as the primary demonstration of engine capabilities and the best starting point for understanding how `.cog` game files are structured.

---

## Running with Docker

The easiest way to run Cog Engine on a modern system is via Docker. The container bundles Python 2.7, GTK2, pygame/SDL, Festival TTS, and a VNC-based browser interface.

**Prerequisites:** Docker and Docker Compose installed.

```bash
# Clone the engine
git clone https://github.com/castellotti/cog-engine.git
cd cog-engine

# Clone the example game alongside it
git clone https://github.com/castellotti/cycon-odyssey.git ../cycon-odyssey

# Build and start the game player
docker compose up --build cogengine
```

Open **http://localhost:6080/cogengine.html** in your browser, click **START** to unlock audio, and the game will begin.

```bash
# Run the game development IDE instead
docker compose -p cogdevapp up --build --profile devapp cogdevapp
```

```bash
# Safe startup (checks for port conflicts)
bash docker/start.sh
```

### Optional: macOS Host Audio via PulseAudio

By default, TTS audio is delivered through the browser via the Web Audio API (no host software needed). For direct system audio on macOS:

```bash
bash docker/setup-macos-audio.sh          # one-time host setup
PULSE_SERVER=tcp:host.docker.internal:4713 docker compose up cogengine
```

---

## Architecture

### Applications

| Component | Description |
|-----------|-------------|
| `cogengine/` | Game player — loads `.cog` files and runs the game |
| `cogdevapp/` | Visual IDE — creates and edits game content |

### Game Engine (`cogengine/`)

The engine uses a layered class inheritance architecture where modules higher in the hierarchy are accessible to more components below. Key modules:

- **`CogEngine_Modules.py`** — core game state machine: verb/item/room/direction parsing, event evaluation and effect execution
- **`CogEngine_GtkSDL_Modules.py`** — GTK2/Pygame rendering layer: inventory panel, compass panel, room-object panel, SDL event loop
- **`CogEngine_Application_GtkSDL.py`** — main entry point, wires GTK2 UI (defined in `CogEngine_Application_GtkSDL.glade`) to the engine
- **`CogEngine_Festival_Modules.py`** — Festival TTS integration: spawns `festival --server`, sends text over socket, receives WAV output
- **`CogObjects.py`** — data model: `GameInformation`, `PlayerInformation`, `RoomData`, `ItemData`, `VerbData`, `EventData`, `DirectionData`, `ObstructionData`
- **`CogEngine_Utilities.py`** — pickle-based `.cog` file I/O

### Game Development IDE (`cogdevapp/`)

The Cog Development Application provides dedicated editors for every game object type (rooms, items, verbs, directions, obstructions, events) with drop-down selection lists, undo support, and live in-editor game testing. The event builder supports a visual grammar for composing conditional requirements and effects such as `PickUpItem`, `PlaySoundFile`, `UnlockRoom`, and more.

### Container Stack

```
Browser → http://localhost:6080/cogengine.html
  ├── VNC iframe ← websockify ← x11vnc ← Xvfb (640×595)
  └── Web Audio API
       └── polls counter.txt every 300ms → fetches latest.wav → AudioContext
            ↑
       Festival TTS → WAV → /usr/share/novnc/audio/
```

`docker/entrypoint.sh` orchestrates startup: Xvfb → x11vnc → websockify → Festival → game app. The app waits for a browser VNC connection before launching, and one click on the START overlay is required to unlock browser autoplay policy.

### Game Data Format

Games are stored as Python pickle files (`.cog`). The format has been stable since v1.1.3 (June 2002), with migration scripts (`cogdevapp/convert-*.py`) provided for older versions.

---

## History

| Date       | Milestone |
|------------|-----------|
| 1999-05-08 | Initial public release |
| 1999-06-11 | Dynamic GUI components (toggleable compass, inventory, command line) |
| 2000-03-18 | Beta v0.90 — backgrounded image downloads for smoother online play |
| 2001-02-07 | Cog Development Application rewritten in Python/GTK+ (replacing Java) |
| 2001-06-12 | CogDevApp v0.80 — first public IDE release |
| 2001-09-13 | Cycon Odyssey first Beta (v0.92) released — playable after "over a decade in the making" |
| 2001-09-17 | CogDevApp ported to Windows |
| 2001-11-02 | COG Engine awarded DaveCentral's Best of Linux |
| 2002-01-27 | **Cog Engine v1.0 released** — stable release after three years of development |
| 2002-03-09 | Pygame/SDL integration for room image display |
| 2002-03-07 | Ported to Compaq iPAQ (Familiar Linux) |
| 2002-05-16 | v1.1.1 — Python rewrite of engine; Java v1.0 deprecated |
| 2002-05-31 | v1.1.2 — Text-to-Speech (Festival on Linux, MS Speech SDK on Windows) |
| 2002-06-10 | v1.1.3 — Graphical inventory and object panels; new `.cog` file format |
| 2002-06-17 | v1.1.4 — 100% graphical play mode; no keyboard required |
| 2002-06-21 | v1.1.5 — Audio file event support (`PlaySoundFile`); word wrapping |
| 2002-07-15 | v1.1.6 — Compass shows visited rooms and last direction; object close-up interaction |
| 2026+      | **Branch 1.2.0** — Docker modernization; runs on contemporary systems via browser VNC + Web Audio |

---

## License

The Cog Engine comes with **ABSOLUTELY NO WARRANTY**. See the `COPYING` file for details.

Original project homepage: http://cogengine.sourceforge.net
SourceForge development site: http://sourceforge.net/projects/cogengine/