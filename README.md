# CDImage
## A tool for burning visible pictures on a compact disc surface

![alt text](https://github.com/arduinocelentano/cdimage/blob/main/demo.png)

## Project's Origins and Credits
I know of at least two successful attempts to implement a similar technique. One was accomplished about 15 years ago by [argon](https://www.instructables.com/Burning-visible-images-onto-CD-Rs-with-data-beta/) Instructables user. [Another attempt](http://undefer.narod.ru/cdpaint/index.html) was made by a user with nickname [unDEFER] (no English documentation unfortunately). These two projects inspired me some time ago. And in fact my coordinate conversion code is mostly based on [unDEFER]’s implementation. I also used geometric parameters of some compact discs from that project. I acknowledge and am grateful to these developers for their contributions.

I played with color shades and different compact discs with moderate success and created a GUI with visual preview mode. I tried to implement a user-friendly solution but finally abandoned the project in 2008 due to a problem of calibration for every particular brand and type of compact disc. Recently I found my old code and decided to share it. More as a tribute to the compact disc era. But maybe you will make some use of it. I fixed some obvious bugs, brushed the code up a little and ported it to modern Qt6. I considered porting to Python but I still need C++ because audio track generation takes some time even on modern hardware.

## Building
You'll need [Qt 6](https://www.qt.io/product/qt6) library to build it. Just run `qmake` and then `make`. Alternatively you could build the project with [Qt Creator](https://www.qt.io/product/development-tools) if you installed it.

## Windows Users
Since many Windows users experienced problems with building it or did not want to install Qt and all the stuff, I've made a [Windows binary build](https://github.com/arduinocelentano/cdimage/releases).
However I have not tested it thoroughly yet because I don't have a working CD recorder at hand right now.
I think I'll try to burn some discs with Windows tools later and note down the steps for Windows users.

## Before you start
If your compact disc is not mentioned in the track generating dialog, you'll probably fail. All the discs are slightly different geometrically. This difference does not matter for data storage but dramatically influences image calculation.
You could try to guess geometry of an unknown disc and input it manually, but you'll probably spoil a lot of discs before you get some results. Moreover, all your test discs should be perfectly identical or you should use the same CD-RW disc. Sometimes discs of the same model happen to have different parameters. Don't know why. After all, manufacturers have never cared since those discs were never supposed to be used this way.

## Usage
1. Click **Edit→Load image** and select an image file. I recommend that you use a high-contrast image. If you choose a full color image, it will be converted to grayscale. You can adjust and scale your image:

* **left mouse button** — move image;

* **double click** — center image;

* **mouse scroll wheel** — zoom image.

2. Click Edit→Create track and select the model of your compact disc.

> If your disc is not in the list (which is likely), you may input geometry manually. However unknown disc calibration is neither easy nor quick procedure. If you still wish to give it a try, I recommend that you read the ["Red Book"](https://www.ecma-international.org/wp-content/uploads/ECMA-130_2nd_edition_june_1996.pdf) as well as  [Considering Calibration](#considering-calibration) section before you start. **If you know the geometry of some compact disc which is not in the list, let me know and I’ll include it into the distribution.**

Depending on your hardware, conversion will take some time. Finally you’ll get a huge Audio CD track. *Yes, about 800Mb, which is normal for **Audio CD**.*

3. You could use any software you like to burn it. For example:

`cdrecord -sao -audio dev=<recorder_device> <generated_track>`

Remember that you should create an **Audio CD**!

## Considering Calibration
From the Mathematical point of view we have a sort of [multi-objective optimization](https://en.wikipedia.org/wiki/Multi-objective_optimization) problem. Bicriteria optimization, to be more precise. It means that two objective functions should be optimized simultaneously. If we define goal as getting a "neat image", we need an expert who is able to provide some feedback regarding image "quality". Which leads us to [interactive methods](https://en.wikipedia.org/wiki/Multi-objective_optimization#Solution).

The first and the most obvious idea is to select some series of equally spaced values for each criterium and burn a lot of discs with all possible combinations. If the space is narrow enough, you'll see something at some discs. Then narrow the range and repeat. A typical Computational Mathematics approach. A lot of iterations and time.

The number of iterations could be reduced if we gradually change criteria within one image from disc center to rim. Then one should look for areas where some distinctive fragments could be seen. The only implementation I know about was a part of [CD PAINT](http://undefer.narod.ru/cdpaint/index.html) project I mentioned. I thought it was gone, but finally found it. It was called `defcdparams`. Apparently CD PAINT project contributors used it to define geometry of four discs I know. However it is still a time consuming procedure. I think it was the main reason why CD PAINT project was abandoned.

At least for me it was the reason why I finally gave up. However I'd like to share some of my thoughts regarding possible improvements of calibration technique. The weakest component in the mentioned algorithm is the necessity of human expertise. How it could be automated?

1. If all the discs are geometrically different, then seek time delays would be different to. Because the same sector A is located at different angles for two different discs. So if we know "ideal" delays for a calibrated disc, we theoretically should be able to calibrate another one. But... These delays must be optical drive dependent. So this solution potentially would face some hardware issues.

2. I have not considered this option in 2008, but now we have more advanced image recognition algorithms and better cameras. So maybe some AI solution might be used instead of human expertise.

If you have other ideas, please share them.

### A start to finish calibration method
All the calibration images are available in the `calibration/images` directory.

You would start by burning `out-alt-lines-coarse.png` and see a similar pattern to:
<p align="center">
    <img src="https://github.com/arduinocelentano/cdimage/blob/main/calibration/example-distortion-patterns/reconstructed-coarse.png" width="200" alt="reconstructed coarse"/>
</p>
If the thick line is closer to the inside when compared to the thin line then your guessed tr0 is too low and if the thick lines is closer to the edge when compared to the thin line then your guessed tr0 is too high.

You can adjust your values by trial and error or you can use the solver (see below), note that with the images `out-alt-lines-coarse.png`, `out-alt-lines-0.png`, `out-alt-lines-1.png`, `out-alt-lines-2.png` and `out-alt-lines-3.png` there are no reference rings at 4mm intervals (for clarity reasons) such as with `grad-ref.png` and `grad-ref-out.png` so only use those images initially since you actually have to measure distances from the center of the disc for the ring positions the solver expects (28.5 mm for ring 1, 40.5 mm for ring 4 and 56.5 mm for ring 8) then use `grad-ref.png` (or `grad-ref-out.png` although it isn't as clear as `grad-ref.png` to read) once you can clearly make out the radial lines.

Slowly move up through images `out-alt-lines-coarse.png`, `out-alt-lines-0.png`, `out-alt-lines-1.png`, `out-alt-lines-2.png` and `out-alt-lines-3.png` then `grad-ref.png` (or `grad-ref-out.png`) as the winding gets less and less intense.

You can either use the solver (see below) or use the graph (see below) once a pretty good initial guess has been made (one or two windings across the whole disc surface) until your values converge.

#### For more examples of expected distortion patterns
The `calibration/example-distortion-patterns` folder contains simulated patterns for a tr0 that's 30 too low and correct dtr with actual settings being at (23380.0, 1.3899) and the "burn" settings being (23350.0, 1.3899) for the corresponding reference images in the `calibration/images` folder gives the corresponding patterns with `grad-ref.png` and `grad-ref-out.png` not being simulated as they would yield unreadable simulation results at these errors.

### Using the solver
The `calibration/solver` directory contains a `solver.py` Python script that can be used to create new tr0 and dtr guesses provided measurements of burnt discs with the different radial lines containing images with a guess for the tr0 and dtr values.

If you burnt an image with radial lines but no reference rings at 4mm intervals you can measure the distance from the center of the disc and see where the winding lines intersect those distances (28.5 mm for ring 1, 40.5 mm for ring 4 and 56.5 mm for ring 8).

Set these different variables in the solver script with your own values:
```python
t1 = 23000.0 # tr0 guess (the one used to burn your disc)
d1 = 1.385459 # dtr guess (the one used to burn your disc)

n1 = -0.014 # number of turns clockwise (fractional and signed) between where one winding radial line (pick one to follow if you use a file with two, usually the thin one if you can make it out) intersects ring 1 and ring 4 (going from the center towards the edge following that line).
n2 = -0.002 # number of turns clockwise (fractional and signed) between where one winding radial line (pick one to follow if you use a file with two, usually the thin one if you can make it out) intersects ring 4 and ring 8 (going from the center towards the edge following that line).
```

Note that if you're using `out-alt-lines-coarse.png`, `out-alt-lines-0.png`, `out-alt-lines-1.png`, `out-alt-lines-2.png` or `out-alt-lines-3.png`, but can't tell if the winding line is clockwise or counter-clockwise, the lines wind clockwise when the thick line is closer to the edge when compared to the thin line next to it and counter-clockwise when the thick line is closer to the center when compared to the thin line next to it.

Then run it. It should return new guesses for tr0 and dtr.

Rinse and repeat until the values converge.

### Using the graph
Here follows a visual method for calibration once a close initial guess has been found (this can be done with [unDEFER]'s defcdparams software or with a preset that yields a close result or the method presented above) using a graph.

#### Step 1: Burn with an inital guess for the parameters
Burn your disc with one of the following patterns (the first one is more readable):

<p align="center">
    <img src="https://github.com/arduinocelentano/cdimage/blob/main/calibration/images/grad-ref.png" width="200" alt="non alternating lines"/>
    <img src="https://github.com/arduinocelentano/cdimage/blob/main/calibration/images/grad-ref-old.png" width="200" alt="alternating lines"/>
</p>

#### Step 2: Coming up with a refined guess
Open [this Desmos graph](https://www.desmos.com/calculator/vqbhbt7bkj). You can take a picture of your CD's surface and load it into Desmos and move it around till the concentric lines line up with the purple lines. You don't have to but it makes lining up the simulated lines easier.

Then you set t1 (first track length) and d1 (track delta) to your initial guess, the settings you used to burn your CD.

Then you change the values for t0 (first track length), d0 (track delta) and alpha0 (angle for the start of the line) till the black line overlaps with the line you see on your CD. The black line corresponds to the expected pattern for a disc of actual/real parameters t0 and d0 that is burned with parameters t1 and d1.
<p align="center">
    <img src="https://github.com/arduinocelentano/cdimage/blob/main/calibration/docs/linedup.png" width="600" alt="screenshot of example usage of the Desmos graph"/>
</p>

The values for t0 (first track length) and d0 (track delta) you get are a new guess for the geometry parameters.

You should only have to repeat this process 6-7 times to get a satisfying result.

## Further readings

[Probably the first implementation of similar technique](https://www.instructables.com/Burning-visible-images-onto-CD-Rs-with-data-beta/).

[The "Red Book"](https://www.ecma-international.org/wp-content/uploads/ECMA-130_2nd_edition_june_1996.pdf) (CD-ROM ECMA standard).

[Hackaday post](https://hackaday.io/project/186303-burning-pictures-on-a-compact-disc-surface) about this project.

[A project regarding optical drive reverse engineering](https://scanlime.org/2016/08/scanlime001-coastermelt-part-1/). Not related directly to this project, but might be useful to give you a clue to how it probably could be done with hardware approach. Thanks to [some guy](https://hackaday.com/2022/07/11/burn-pictures-on-a-cd-r-no-special-drive-needed/#comment-6491772) for suggestion.
