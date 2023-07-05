# The Great Dalmuti

## About

This is a implementation of the **multiplayer** card game The Great Dalmuti in Python. The game starts when the player who has the lead
plays a set of cards of the same rank face up. A set is simply one or more cards. Each player can either play a set of the same number of cards of better rank or pass. The rules can be found [in this PDF](./great_dalmuti_rules.pdf).

<img src="./img/game.png" alt="The Great Dalmuti" width="600"/>

## Instructions

To run the game you only need to install Python 3.7 or higher. The game requires at least 4 players to start. 

### Configuration

The game is played as in a table, implemented in a **Token Ring Network**. To create the ring, edit the [config.txt](./src/config.txt) and fill the **IP address** and **port** of each machine. The `send port` of Player 1 must match to `receive port` of Player 2, and so on. 

<img src="./img/ring2.png" alt="Config" width="300"/>

### Execution

To start the game run the following command in each machine:

```bash
python3 main.py
```

The game was developed and tested in UFPR laboratory machines with SSH.