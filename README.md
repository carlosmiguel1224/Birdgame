---

## 🎮 **2. Multiplayer Flappy Bird Game (LAN)**

# 🐦 Multiplayer Flappy Bird (LAN-Based)

A Python-based real-time multiplayer game inspired by Flappy Bird, built with Pygame and a custom socket-based server. Allows up to 10 players to compete over a LAN network.

---

## 🚀 Features

- Real-time game logic over TCP/IP
- Handles up to 10 simultaneous players
- Custom obstacles (spikes) shared across players
- Unique client ID tracking and reconnect logic
- Restart and sync handled programmatically via server

---

## 🛠 Tech Stack

- **Python**
- **Pygame** – 2D graphics and game loop
- **Socket / Threading** – Custom server-client networking
- **Pickle** – Object serialization for network transmission

---

## 📂 Project Structure

.
├── birdgame-lite.py # Client game logic
├── servermodified.py # TCP socket server
├── assets/ # Images for birds, background, spikes
├── README.md

yaml
Copy
Edit

---

## ▶️ Running the Game

Start the server:

```bash
python servermodified.py
Then start each player on a separate machine (on the same LAN):

bash
Copy
Edit
python birdgame-lite.py
