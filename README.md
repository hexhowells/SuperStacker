# SuperStacker
SuperStacker is a heuristic based AI that can play NES Tetris at a superhuman level.

Recently used in the paper [Outsmarting algorithms: A comparative battle between Reinforcement Learning and heuristics in Atari Tetris](https://www.sciencedirect.com/science/article/pii/S0957417425008735)

-----

<p align="left">
  <img src="https://github.com/hexhowells/SuperStacker/blob/main/gifs/superstacker_clip.gif" width=65%>
</p>
Example of SuperStacker playing past the killscreen

-----

## Usage
This program runs on the BizHawk emulator and uses Python for backend computations. to use:

- Run ```play.py```
- Start NES Tetris in Bizhawk
- Run ```play.lua``` from ```scripts/``` in the BizHawk lua console
- SuperStacker should select the game and begin playing, it will automatically unpause and restart the game 

-----

## How it works
For each current falling piece, SuperStacker finds every possible place the piece can land, each placement is then evaluated using a set of features. The placement with the best evaluation is chosen, actions are then performed to move and orient the piece to arrive at the desired location. 

All of this is done in the first frame of each new piece arriving on screen.

Currently doesn't use information about the next piece and cannot tuck pieces.

-----

## Statistics
- Current Highest Score: 4,243,879
- Current Highest Level: 130
- Most Lines Cleared: 1305

-----

## Heuristic Features
SuperStacker uses many features to determine the value of each possible move

#### Line Clears
- Heavily prioritises clearing lines

#### Holes
- A hole is defined as an empty tile with a solid tile directly above it
- Holes are quite heavily avoided

#### Wells
- A well is defined as an empty tile with a solid tile on both its right and left side
- Wells are lightly avoided

#### Increasing Build Height
- Any placements that increase the max build height is avoided when possible

#### Placement Height
- Pieces are generally placed low down when possible

-----

## TODO
- Utilise next piece information
- ~~Add more heuristic features~~
- Add ability to tuck pieces
- Prioritise getting higher scores through tetrises
- Evaluate hole depth
