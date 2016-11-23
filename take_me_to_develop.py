import logging

from git import Repo, Git
import re

"""
Take Me To Develop!
ABOUT:
This tool detects a release branch you're on (of the form release-M.mm.0),
and merges it to all future release branches and then to develop.
for example, if you're on release-2.52.0, and you run the tool, it should perform these merges:

    1. merge release-2.52.0 -> release-2.53.0
    2. push release-2.53.0
    3. release-2.53.0 -> develop
    4. push develop

In case of a conflict or other git errors, it will fail spectacularly.

USAGE:
Just run it inside the repo, with a release branch you want to merge checked out.

Author: Adam Narkunski
"""

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('take')
logger.setLevel(logging.INFO)


class TakeMe(object):
    def __init__(self, repo_path):
        self.release_pattern = re.compile("^release-(\d+)\.(\d+)\.0$")
        self.repo = Repo(path=repo_path)
        self.git = Git(repo_path)
        self.initial_branch = self.get_current_branch()
        self.remote = self.repo.remotes[0]
        if self.remote.name != 'origin':
            logger.warn('remote is: %s', self.remote.name)

    def main(self):
        # 0. figure out the list of branches to merge to
        self.get_targets()
        last_branch = self.initial_branch
        for target_branch in self.targets:
            # 1. check out the next branch
            logger.info('checking out {}'.format(target_branch.name))
            target_branch.checkout()

            # 2. pull
            logger.info('pulling {}'.format(self.get_current_branch().name))
            self.git.pull()

            # 3. merge current branch
            logger.info('merging {}'.format(last_branch))
            self.git.merge(last_branch.name)

            # 3.f. if there's a conflict, stop the whole thing and show message to the user
            """ So weird, where is the error handling? """

            # 4. push to origin
            logger.info('pushing {}'.format(self.get_current_branch()))
            self.git.push()

            # 5. go to the next release branch, or develop
            last_branch = self.get_current_branch()

        logger.info('checking out original branch')
        self.initial_branch.checkout()

    def get_current_branch(self):
        logger.debug("current branch is '%s'", self.repo.active_branch)
        return self.repo.active_branch

    def get_targets(self):
        assert self._is_release(self.initial_branch.name)
        major, minor = self._get_major_minor(self.initial_branch.name)
        # filter all release branches that are later than ours
        targets = []
        for branch0 in self.repo.branches:
            if self._is_release(branch0.name):
                major0, minor0 = self._get_major_minor(branch0.name)
                if major0 >= major and minor < minor0:
                    targets.append(branch0)

        try:
            targets.append(self.repo.branches.develop)
        except:
            raise Exception("So weird, where is develop branch")
        logger.debug(targets)
        self.targets = targets

    def _get_major_minor(self, branch_name):
        assert self._is_release(branch_name)
        match = self.release_pattern.match(branch_name)
        if not match:
            raise Exception("So weird, '{}' doesn't seem like a release branch.".format(self.initial_branch))
        major, minor = match.groups()
        logger.debug("{} => major={} ; minor={}".format(branch_name, major, minor))
        return major, minor

    def _is_release(self, branch_name):
        match = self.release_pattern.match(branch_name)
        return True if match else False


def test(tm):
    assert not tm._is_release('kakiel')
    assert not tm._is_release('release-2.41.0_h1')
    assert tm._is_release('release-2.41.0')
    assert ('2', '47') == tm._get_major_minor('release-2.47.0')


def main():
    tm = TakeMe("/Users/adam/repos/test/")
    test(tm)
    tm.main()



if __name__ == "__main__":
    main()
