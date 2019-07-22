import git
import mock

from eh import constants
from eh import exceptions as exc
from eh.tests import base_test as base
from eh import git_store as gs


class TestGitStore(base.TestCase):
    def setUp(self):
        super(TestGitStore, self).setUp()
        self.store = gs.GitTopicStore({}, "somerepo", "")

    def tearDown(self):
        super(TestGitStore, self).tearDown()
        mock.patch.stopall()

    def test_create_git_store(self):
        self.assertIsNotNone(self.store)

    @mock.patch('os.path.exists', create=True)
    @mock.patch('os.makedirs', create=True)
    @mock.patch('git.Repo.clone_from', create=True)
    def test_setup_repo_dir_make_if_missing(
            self, mock_clone, mock_dirs, mock_exists):
        mock_exists.return_value = False
        self.store._setup_repo_directory()
        self.assertEquals(1, mock_dirs.call_count)

    @mock.patch('os.path.exists', create=True)
    @mock.patch('os.makedirs', create=True)
    @mock.patch('git.Repo.clone_from', create=True)
    def test_setup_repo_dir_dont_make_if_there(
            self, mock_clone, mock_dirs, mock_exists):
        mock_exists.return_value = True
        self.store._setup_repo_directory()
        self.assertEquals(0, mock_dirs.call_count)

    @mock.patch('os.path.exists', create=True)
    @mock.patch('os.makedirs', create=True)
    @mock.patch('git.Repo.clone_from', create=True)
    @mock.patch('eh.git_store.exit', create=True)
    def test_init_repo_exit_on_giterror(
            self, mock_exit, mock_clone, mock_dirs, mock_exists):
        mock_exists.return_value = True
        mock_clone.side_effect = git.exc.GitCommandError("clone", "failboat")
        self.store._init_repo()
        self.assertEquals(1, mock_exit.call_count)

    @mock.patch('os.path.exists', create=True)
    @mock.patch('os.makedirs', create=True)
    @mock.patch('git.Repo.clone_from', create=True)
    @mock.patch('eh.git_store.exit', create=True)
    def test_init_repo_no_exit_on_okay(
            self, mock_exit, mock_clone, mock_dirs, mock_exists):
        mock_exists.return_value = True
        self.store._init_repo()
        self.assertEquals(0, mock_exit.call_count)

    @mock.patch('os.path.exists', create=True)
    def test_check_if_dir_exists_based_on_file(self, mock_exists):
        mock_exists.return_value = False
        self.assertFalse(self.store._check_if_directories_exist())
        mock_exists.return_value = True
        self.assertTrue(self.store._check_if_directories_exist())

    @mock.patch('os.path.exists', create=True)
    @mock.patch('eh.git_store.GitTopicStore._init_repo', create=True)
    def test_get_subjects_init_repo_if_missing(self, mock_init, mock_exists):
        mock_exists.return_value = False
        self.store._get_subjects_from_repo()
        self.assertEquals(1, mock_init.call_count)

    @mock.patch('os.path.exists', create=True)
    @mock.patch('eh.git_store.GitTopicStore._init_repo', create=True)
    def test_get_subjects_dont_init_repo_if_there(
            self, mock_init, mock_exists):
        mock_exists.return_value = True
        self.store._get_subjects_from_repo()
        self.assertEquals(0, mock_init.call_count)

    @mock.patch('os.path.exists', create=True)
    @mock.patch('eh.git_store.GitTopicStore._init_repo', create=True)
    @mock.patch('git.cmd.Git', create=True)
    def test_update_pull_if_exists(self, mock_git, mock_init, mock_exists):
        mock_exists.return_value = True
        mock_pull = mock.MagicMock()
        mock_git_cmd = mock.MagicMock()
        mock_git_cmd.pull = mock_pull
        mock_git.return_value = mock_git_cmd
        self.store.update()
        self.assertEquals(1, mock_git.call_count)
        self.assertEquals(1, mock_pull.call_count)
        self.assertEquals(0, mock_init.call_count)

    @mock.patch('os.path.exists', create=True)
    @mock.patch('eh.git_store.GitTopicStore._init_repo', create=True)
    @mock.patch('git.cmd.Git', create=True)
    def test_update_init_if_new(self, mock_git, mock_init, mock_exists):
        mock_exists.return_value = False
        mock_pull = mock.MagicMock()
        mock_git_cmd = mock.MagicMock()
        mock_git_cmd.pull = mock_pull
        mock_git.return_value = mock_git_cmd
        self.store.update()
        self.assertEquals(0, mock_git.call_count)
        self.assertEquals(0, mock_pull.call_count)
        self.assertEquals(1, mock_init.call_count)
