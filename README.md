# tetrisgame
## About
The classic game Tetris written entirely in python, using the `pygame` library to draw the game in a separate window. Includes the following features:
- Correct basic colour scheme (Cyan I, Yellow O etc;)
- Super Rotation System (SRS)
- Random bag for piece generation
- Hold piece
- Ghost piece
- Proper loss detection
- Display of the next tetrominoes
- 'Cascade' gravity after line clearing

## Shortcuts
Whilst the controls can easily be found ingame, there are several useful keyboard shortcuts. These shortcuts are intentionally complicated to prevent people accidentally discovering them, since this was designed to be showcased to people.
- Quit game: ctrl + alt + shift + capslock + -
- Open console: ctrl + alt + shift + capslock + /

## Console commands
- setdebugmode (0, 1)
- setcolourmode (0 - 5)
- setdrawmode (0-2)
- setbackgroundimage (relative image path)
- setrepeatablecooldown (any float >= 0)
- setsingularcooldown (0, 1)