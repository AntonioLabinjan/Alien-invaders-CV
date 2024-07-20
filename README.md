# CV Space Invaders

Welcome to CV Space Invaders, a modern twist on the classic arcade game! This game uses your webcam to track your hand movements and control the spaceship. Dodge and shoot aliens, collect power-ups, and achieve the highest score possible!

## Features

- **Hand Detection Control**: Move your spaceship with real-time hand tracking using Mediapipe and OpenCV.
- **Variety of Aliens**: Face different types of aliens including normal, fast, strong, shooting, and boss aliens.
- **Power-Ups**: Collect power-ups to gain shields, health, double bullets, and spread bullets.
- **High Score Tracking**: Your highest score is saved and displayed at the end of each game.

## How to Play

1. **Start the Game**: Run the game script. Your webcam will activate and start tracking your hand movements.
2. **Move Your Spaceship**: Move your hand to control the spaceship's horizontal position.
3. **Shoot Aliens**: The spaceship will automatically shoot bullets at a fixed rate. Aim carefully to hit the aliens.
4. **Avoid Alien Bullets**: Dodge incoming bullets from shooting aliens and boss aliens.
5. **Collect Power-Ups**: Gain advantages by collecting different power-ups that fall from the top.
6. **Stay Alive**: Keep your health above zero by avoiding collisions with aliens and alien bullets.
7. **Score Points**: Destroy aliens to score points. Stronger aliens and boss aliens give more points.
8. **End Game**: The game ends when your health reaches zero. Compare your score with the high score and try again!

## Alien Types

- **Normal Alien**: Standard speed and single hit to destroy.
- **Fast Alien**: Moves quickly but only takes one hit.
- **Strong Alien**: Takes multiple hits to destroy.
- **Shooting Alien**: Fires bullets at the player. Takes one hit to destroy.
- **Boss Alien**: Moves slowly but takes multiple hits to destroy and provides a high score reward.

## Power-Ups

- **Shield**: Grants temporary invincibility.
- **Health Pack**: Restores one health point.
- **Double Bullet**: Shoots two bullets at a time.
- **Spread Bullet**: Shoots three bullets in a spread pattern.

## Installation

1. Ensure you have Python installed on your system.
2. Install the necessary packages using pip:

```
pip install pygame opencv-python mediapipe
```

3. Download the game assets and place them in the same directory as the script:

- `ship.png`
- `alien.png`
- `fast_alien.jpg`
- `strong_alien.jpg`
- `shooting_alien.jpg`
- `boss_alien.jpg`
- `shield.jpg`
- `health_pack.jpg`
- `double_bullet.jpg`
- `spread_bullet.jpg`

## Running the Game

Run the script using Python:

```
python cv_space_invaders.py
```

Ensure your webcam is connected and working properly.

## Controls

- Move your hand in front of the webcam to control the spaceship's horizontal movement.
- The spaceship will automatically shoot bullets at a fixed rate.

## High Score

Your highest score is saved in a file named `high_score.txt` in the same directory as the game script. Try to beat your high score each time you play!

## Game Over

When the game ends, you will be given an option to play again by pressing 'Y' or to quit by pressing 'N'.

## Credits

Developed by [Antonio Labinjan]

This game uses the following libraries:

- [Pygame](https://www.pygame.org/)
- [OpenCV](https://opencv.org/)
- [Mediapipe](https://mediapipe.dev/)

Enjoy the game and have fun shooting those aliens!
