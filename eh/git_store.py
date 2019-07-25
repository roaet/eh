import os
import git

import click

from eh import topic_store as ts


class GitTopicStore(ts.TopicStore):
    def __init__(self, conf, repo, filepath):
        """
        repo - is the git url
        filepath - is the place the repo will be cloned
        """
        self.repo = repo
        self.repo_path = '%s%s' % (filepath, os.sep)
        super(GitTopicStore, self).__init__(conf, filepath)

    def initialize(self, conf):
        if not self._check_if_directories_exist():
            self._init_repo()
        super(GitTopicStore, self).initialize(conf)

    def _setup_repo_directory(self):
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        git.Repo.clone_from(self.repo, self.repo_path)

    def _init_repo(self):
        try:
            self._setup_repo_directory()
        except git.exc.GitCommandError as e:
            click.echo("Failed to clone: %s" % e)
            exit(1)

    def _get_subjects_from_repo(self):
        if not self._check_if_directories_exist():
            click.echo('Need to initialize subjects')
            self._init_repo()

    def _check_if_directories_exist(self):
        return os.path.exists(self.repo_path)

    def update(self):
        if not self._check_if_directories_exist():
            click.echo('Need to initialize subjects')
            self._init_repo()
        else:
            g = git.cmd.Git(self.repo_path)
            g.pull()
            click.echo("Updated subjects")
