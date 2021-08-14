# [Minecraft Plus!](https://undarkaido.github.io/Minecraft-Plus/)

[*Read Mojang's original announcment on the Minecraft Blog*]()

A tweaked version of *Minecraft Plus!*, Minecraft's 2021 April Fool's joke.

All copyright belongs to Mojang Studios

## Changes
* URLs are now relative for rehosting
* The canvas is now initially sized properly
* The canvas resizes when the window does
  * The WASM can't seem to be able to tell this is happening though
* Load an alternate `resources.zip` with the `resources` parameter
* Decrease contrast with the `opacity` and `background-color` parameters

## Usage
URL parameters
* `autorun`
  * With 'window' it opens a random module in windowed mode [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window)
  * With no value it takes you striaght to the launch screen
  * When not included you get the default slow that offers you a download of the `.scr` version and lets you choose between fullscreen and windowed mode
* `background-color`
  * Takes a CSS color
  * Inactive unless `opacity` is set
  * With no value defaults to `white`
* `module`
  * With a parameter it loads the specified module instead of a random one. Input is `% max`
    * `0` A rotating block with random faces [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=0)
    * `1` A DVD bounce with a trail [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=1)
    * `2` A traditional DVD bunce [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=2)
    * `3` Litters random items on the ground [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=3)
    * `4` Isometric view of Alpha water [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=4)
    * `5` Isometric view of Alpha lava [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=5)
    * `6` A random main menu panorama [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=6)
    * `7` Colored footsteps [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=7)
    * `8` Swimming glowsquids [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=8)
    * `9` Random items and blocks bouncing Solitaire style [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=9)
    * `10` Grass growing across the screen [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=10)
    * `11` A rotating field of blocks [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=11)
    * `12` Hyperspace but creepers [\[link\]](https://undarkaido.github.io/Minecraft-Plus/?autorun=window&module=12)
  * With no value it defaults to `0`
* `opacity`
  * Set the opacity of the canvas with a decimal where `0 <= x <= 1`
  * With no value it defaults to `1`
* `resources`
  * The full path of an alternate `resources.zip`
