# Kantor Virtual PekaAI

Live status board and interactive 3D office of the PekaAI team: 11 divisions, 17 AI staff whose statuses follow the real operational schedule (WIB). Working agents sit at their desks, standby agents patrol their division area, off-shift agents rest in the lounge or the meeting room. Movement is a deterministic function of the wall clock, so every visitor sees the same office at the same moment and a reload never resets anyone.

- Site: https://virtual.peka.ai.id (also embedded on https://peka.ai.id)
- Single-file front end (`index.html`) with a self-hosted Three.js build (`three.module.js`)
- Served by `serve.py` on 127.0.0.1:8093 (systemd `peka-virtual.service` + SSH tunnel `peka-virtual-tunnel.service`)
- The sky, lighting, wall clock, and meeting-room agenda all follow real WIB time
