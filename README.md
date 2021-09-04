# BDD Minimal Cutsets

NOTE: WIP

Implementation of Rauzy's algorithm for finding minimal cutsets given a binary decision diagram.

Rauzy, Antoine. "New algorithms for fault tree analysis," *Reliability Engineering and System Safety* 40 (1993) 203-211

Requires https://github.com/tulip-control/dd


## Status

* Major issue arises with negated edges, leading to inaccurate MCS.
* Negated edges can be mostly eliminated by careful variable ordering in advance of BDD construction.
* However as long as negated edges are present in the BDD I would not rely on this implementation for MCS.

