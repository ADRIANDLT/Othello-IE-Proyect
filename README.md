# Othello-IE-Proyect

Othello game using Game2DBoard, data structures and algorithms for computer mind. 

## Grab the code locally (clone the repo)

In your computer, clone this repo from a terminal or PowerShell window (You can use the Anaconda Powershell Prompt, too).

```git clone https://github.com/ADRIANDLT/Othello-IE-Proyect.git```

## System requirements:

### Python 3.8 and Conda

Make sure to have Python 3.8 and Conda installed in your machine.

Conda is optional but it will be easier to use a conda environment for the game.

### Create Conda environment from our othello-game-python-3-8.yaml conda environment definition

In a terminal window go to the root folder of the cloned repo:

```cd my_path_to_the_local_folder_repo```

Create a new coda environment like a clone based on the .yaml file

```conda env create --file othello-game-python-3-8.yaml```

![image](https://github.com/ADRIANDLT/Othello-IE-Proyect/assets/36977944/8acde357-dc30-421c-bfa1-41820026a519)

Now you can check that you have the new environment created:

```conda env list```

![image](https://github.com/ADRIANDLT/Othello-IE-Proyect/assets/36977944/4a9dac5d-b6e7-4729-a93f-40d35e9da2c5)

Now lets activate the new environment:

```conda activate othello-game-python-3-8```

![image](https://github.com/ADRIANDLT/Othello-IE-Proyect/assets/36977944/bf941aa1-7ff8-40de-bcf0-b8fa11e2e9cc)

### Run the game

You can run the game from any IDE (VS Code or PyCharm) or you can directly run it in Python with this command:

```python game_launcher.py```

![image](https://github.com/ADRIANDLT/Othello-IE-Proyect/assets/36977944/321fdeba-6d94-4a75-a17d-23677ef27868)


### (OPTIONAL) Python packages to install on activated conda environment

If you dont want to create a new conda environment you can also simply install the following python library package in your current python env:

```pip install game2dboard```

