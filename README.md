# A database of (approximately) optimal experimental designs

**Editor**: Jeffrey M. Hokanson

## Introduction

Space-filling experimental designs pose notoriously 
difficult optimization problems.
Here we collect the best known current designs
for the dual purpose of 

* providing experimentalists with precomputed near-optimal designs and 
* a benchmark for the performance of new algorithms for constructing experimental designs.

Visualizations of these designs can be seen at [my website](http://hokanson.us/design/).


## Related Work

* [Packomania](http://www.packomania.com): an extensive resource for sphere packing (analogous to maximin design
* [Space-filling designs](https://spacefillingdesigns.nl): a database of designs with many maximin designs

## Contributing

I welcome other researchers to submit new experimental designs.
To submit a design issue a pull request in the directory 
corresponding to the type of design constructed.
For example, to submit a 40-point minimax design using the l2-metric
on the unit-square add a file

```
designs/minimax/l2/square_0040.json
```

This file should be in `json` format with the following fields:

* `X` Coordinates for the design
* `objective` the design criteria used, in this case `minimax`
* `metric` the distance metric used, in this case `l2`
* `domain` the space on which the design is constructed, in this case `square`
* `radius` the radius of the discs covering the domain (a.k.a. dispersion, fill-distance)
* `author` who submitted the design
* `notes` (optional) notes for reproducing the design

When a pull request is issued, 
Travis-CI will check the submitted design
verifying that design has the right number of points 
and `radius` value is correct.
In addition, these checks will also check that the new designs
are better than the ones that are being replaced.



