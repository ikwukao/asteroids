# 🚀 Asteroids

A modern Python implementation of the classic **Asteroids** arcade game built with **Pygame**. Pilot your ship through an endless asteroid field, dodge incoming rocks, and blast them into smaller fragments before they destroy you.

This project was built as part of the **Boot.dev Backend Development** curriculum to practice object-oriented programming, game loops, collision detection, sprite management, and real-time game development using Python.

---

## ✨ Features

* 🎮 Smooth player movement and rotation
* 🔫 Shoot projectiles with cooldown mechanics
* ☄️ Procedurally spawning asteroids
* 💥 Asteroid splitting mechanics
* 🎯 Collision detection between:

  * Player and asteroids
  * Shots and asteroids
* 🧩 Object-oriented architecture
* 📦 Sprite groups for updating and rendering
* 📝 Event and game-state logging
* ⚡ Fixed 60 FPS game loop using delta time

---

## 📸 Gameplay

Control your ship, avoid collisions, and survive as long as possible while destroying incoming asteroids.

---

## 🎮 Controls

| Key       | Action        |
| --------- | ------------- |
| **W**     | Move forward  |
| **S**     | Move backward |
| **A**     | Rotate left   |
| **D**     | Rotate right  |
| **Space** | Fire          |

---

## 🛠️ Tech Stack

* Python 3
* Pygame
* uv

---

## 📁 Project Structure

```text
 .
├──  asteroids
│   ├──  asteroid.py
│   ├──  asteroidfield.py
│   ├──  circleshape.py
│   ├──  constants.py
│   ├──  game_events.jsonl
│   ├──  game_state.jsonl
│   ├──  logger.py
│   ├──  main.py
│   ├──  player.py
│   ├──  pyproject.toml
│   ├──  README.md
│   ├──  shot.py
│   └──  uv.lock
├──  LICENSE
└──  README.md
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/ikwukao/asteroids.git
cd asteroids
```

### Install dependencies

Using **uv**:

```bash
uv sync
```

---

## ▶️ Running the Game

Launch the game with:

```bash
uv run main
```

A game window will open where you can fly your ship and destroy asteroids.

---

## 🧠 Concepts Practiced

This project demonstrates:

* Object-Oriented Programming (OOP)
* Inheritance
* Encapsulation
* Polymorphism
* Sprite management
* Collision detection
* Delta time (frame-independent movement)
* Event-driven programming
* Game loop architecture
* Vector mathematics
* Modular project organization

---

## 📈 Future Improvements

Potential enhancements include:

* Score system
* Multiple lives
* Sound effects and background music
* Particle explosion effects
* Power-ups
* Animated sprites
* Start menu and pause menu
* High-score persistence
* Difficulty scaling

---

## 📚 Learning Resource

This project was developed while completing the **Boot.dev Backend Development** learning path.

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 👨‍💻 Author

**Ikwuka Okoye**

* GitHub: https://github.com/ikwukao
