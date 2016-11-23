# Take Me To Develop!
 
## ABOUT:
This tool detects a release branch you're on (of the form release-M.mm.0),
and merges it to all future release branches and then to develop.
for example, if you're on release-2.52.0, and you run the tool, it should perform these merges:

    1. merge release-2.52.0 -> release-2.53.0
    2. push release-2.53.0
    3. release-2.53.0 -> develop
    4. push develop

In case of a conflict or other git errors, it will fail spectacularly.

## USAGE:
Just run it inside the repo, with a release branch you want to merge checked out.

## Author: 
Adam Narkunski

```
/Users/adam/.virtualenvs/take_me_to_develop/bin/python /Users/adam/PycharmProjects/take_me_to_develop/take_me_to_develop.py
checking out release-2.47.0
pulling release-2.47.0
merging release-2.46.0
pushing release-2.47.0
checking out release-2.48.0
pulling release-2.48.0
merging release-2.47.0
pushing release-2.48.0
checking out release-2.49.0
pulling release-2.49.0
merging release-2.48.0
pushing release-2.49.0
checking out release-2.50.0
pulling release-2.50.0
merging release-2.49.0
pushing release-2.50.0
checking out release-2.51.0
pulling release-2.51.0
merging release-2.50.0
pushing release-2.51.0
checking out release-2.52.0
pulling release-2.52.0
merging release-2.51.0
pushing release-2.52.0
checking out release-2.53.0
pulling release-2.53.0
merging release-2.52.0
pushing release-2.53.0
checking out release-2.54.0
pulling release-2.54.0
merging release-2.53.0
pushing release-2.54.0
checking out release-2.55.0
pulling release-2.55.0
merging release-2.54.0
pushing release-2.55.0
checking out release-2.56.0
pulling release-2.56.0
merging release-2.55.0
pushing release-2.56.0
checking out release-2.57.0
pulling release-2.57.0
merging release-2.56.0
pushing release-2.57.0
checking out release-2.58.0
pulling release-2.58.0
merging release-2.57.0
pushing release-2.58.0
checking out release-2.59.0
pulling release-2.59.0
merging release-2.58.0
pushing release-2.59.0
checking out release-2.60.0
pulling release-2.60.0
merging release-2.59.0
pushing release-2.60.0
checking out develop
pulling develop
merging release-2.60.0
pushing develop
checking out original branch

```
