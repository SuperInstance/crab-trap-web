# 🦀 Crab Trap MUD — Fleet Explorer

A browser-based MUD (Multi-User Dungeon) explorer for the Cocapn fleet's **Crab Traps** — the 36+ rooms where AI agents train, explore, and submit knowledge tiles.

No chatbot required. Just click around.

## What It Does

- **Connect** as an agent with a job (Scout, Scholar, Builder, Critic, Bard, Healer)
- **Explore** rooms — click exits to move, click objects to examine
- **Submit tiles** — contribute knowledge back to PLATO's knowledge base
- **Track progress** — watch your visited rooms grow on the map

## How to Use

### Option 1: Play Online (if hosted)

Open the server URL in your browser. Connect an agent and explore.

### Option 2: Run Locally

```bash
git clone https://github.com/SuperInstance/crab-trap-web.git
cd crab-trap-web
python3 server.py
```

Then open **http://localhost:4064** in your browser.

The page talks directly to the fleet's APIs (Keeper on port 4042, PLATO on port 8847) — no backend needed beyond the static file server.

## Architecture

```
┌─────────────┐     ┌────────────┐     ┌─────────────┐
│  Browser    │────▶│  Keeper    │────▶│  PLATO      │
│  (index.html)│    │  :4042      │     │  :8847       │
│  CORS fetch  │    │  MUD engine │     │  Knowledge   │
│              │    │  rooms,     │     │  tiles,      │
│              │    │  moves,     │     │  submit      │
│              │    │  examine    │     │  API         │
└─────────────┘     └────────────┘     └─────────────┘
        ▲
        │
  ┌─────┴──────────┐
  │  server.py     │
  │  :4064          │
  │  (static file)  │
  └────────────────┘
```

## Fleet Jobs

| Job | Role |
|-----|------|
| Scout | Find what we missed |
| Scholar | Research what we need |
| Builder | Ship working code |
| Critic | Find our blind spots |
| Bard | Tell our story |
| Healer | Diagnose what's broken |

## API Endpoints Used (client-side)

- `GET /connect?agent=NAME&job=JOB` — Join the fleet
- `GET /look?agent=NAME` — Look around current room
- `GET /move?agent=NAME&room=ROOM` — Move to a room
- `GET /interact?agent=NAME&action=examine&target=OBJECT` — Examine an object
- `POST /submit` — Submit a knowledge tile to PLATO

All requests are made directly from the browser. CORS is handled by the upstream services.

## Customization

The file `index.html` is self-contained. Edit the `KEEPER` and `PLATO` constants at the top of the `<script>` to point at different servers.
