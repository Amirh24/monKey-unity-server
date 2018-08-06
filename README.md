# Banano monKey Unity Server script

To understand what monKey is, go to www.monkeygen.com

This script utilize the monKey api in order to transform the 'Banano Runner' game faucet title character.
It takes the fur_color amd eye_color values and color (using a FloodFill function) the following texture according to those parameters:

![Unity character texture](https://i.imgur.com/sAFXZq9.png)

Each monKey corresponds to a unique public key. This means that you are the sole owner of your monKey
When the Unity client replaces the previous texture with the new one the player gets to control a character that no one else has.
The number of possible 3D monkey combinations is 256^3 * 256^3 = 16,777,216^2 = 281,474,976,710,656

[Video example](https://www.youtube.com/watch?v=u20Yzu5T3Ao)

