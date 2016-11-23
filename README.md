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

