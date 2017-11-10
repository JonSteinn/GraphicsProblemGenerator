# Computer Graphics Problem Generator

Generates random computer graphics math problem `.tex` files.

## Problem types
* 2d collision (point and line)
* Camera translation
* Lighting (Phong lighting, single light)
* Rasterization
* Bezier curves

## How to run

```bash
py src/make_all.py
```

or

```bash
py src/make_all.py 25
```

if you want a specific number of problems of each type (in this case, 25). The default is set as 5. You can also use the bat/bash scripts which accept the count argument as well.