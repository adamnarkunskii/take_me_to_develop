import logging
import re
import os

from git import Repo, Git

FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('take')
logger.setLevel(logging.INFO)


class TakeMe(object):
    def __init__(self, repo_path):
        self.release_pattern = re.compile(r"^release-(\d+)\.(\d+)\.0$")
        self.repo = Repo(path=repo_path)
        self.git = Git(repo_path)
        self.initial_branch = self.get_current_branch()
        self.remote = self.repo.remote()
        self.targets = []

    def main(self):
        if not self._is_release(self.initial_branch.name):
            raise Exception("So weird, not on a release branch")

        self.fetch_missing_release_branches()

        # 0. figure out the list of branches to merge to
        targets = self.get_targets(self.repo.refs)
        last_branch = self.initial_branch
        for target_branch in targets:
            # 1. check out the next branch
            logger.info('checking out {}'.format(target_branch.name))
            target_branch.checkout()

            # 2. pull
            logger.info('pulling {}'.format(self.get_current_branch().name))
            self.git.pull()

            # 3. merge current branch
            logger.info('merging {}'.format(last_branch))
            self.git.merge(last_branch.name)

            # 4. push to origin
            logger.info('pushing {}'.format(self.get_current_branch()))
            self.git.push()

            # 5. go to the next release branch, or develop
            last_branch = self.get_current_branch()

    def get_current_branch(self):
        logger.debug("current branch is '%s'", self.repo.active_branch)
        return self.repo.active_branch

    def fetch_missing_release_branches(self):
        original_head = self.get_current_branch()
        try:
            targets = self.get_targets(self.remote.refs, skip_develop=True, filter_origin=False)
            for ref in targets:
                if self._is_release(ref.remote_head):
                    logger.info('verifying that %s is available locally', ref.remote_head)
                    # fetches and tracks the release branch
                    self.git.checkout(ref.remote_head)
        finally:
            logger.info('checking out original branch again: {}'.format(original_head.name))
            original_head.checkout()

    def get_targets(self, branches, skip_develop=False, filter_origin=True):
        major, minor = self._get_major_minor(self.initial_branch.name)
        # filter all release branches that are later than ours
        targets = []
        for branch0 in branches:
            name = re.sub(r"^.*/", "", branch0.name)
            if self._is_release(name):
                major0, minor0 = self._get_major_minor(name)
                if major0 >= major and minor < minor0:
                    if not (filter_origin and self.remote.name in branch0.name):
                        targets.append(branch0)

        try:
            if not skip_develop:
                targets.append(self.repo.branches.develop)
        except:
            raise Exception("So weird, where is develop branch")
        logger.debug(targets)
        return targets

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


def main():
    TakeMe(os.getcwd()).main()


if __name__ == "__main__":
    main()
