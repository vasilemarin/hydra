# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from hydra_plugins.example_sweeper import ExampleSweeper

from hydra._internal.plugins import Plugins
from hydra.plugins import Sweeper

# noinspection PyUnresolvedReferences
from hydra.test_utils.test_utils import sweep_runner  # noqa: F401


def test_discovery():
    """
    Tests that this plugin can be discovered via the plugins subsystem when looking for Sweeper
    :return:
    """
    assert ExampleSweeper.__name__ in [x.__name__ for x in Plugins.discover(Sweeper)]


def test_launched_jobs(sweep_runner):  # noqa: F811
    sweep = sweep_runner(
        calling_file=None,
        calling_module="hydra.test_utils.a_module",
        config_path="configs/compose.yaml",
        overrides=["hydra/sweeper=example", "hydra/launcher=basic", "foo=1,2"],
        strict=True,
    )
    with sweep:
        job_ret = sweep.returns[0]
        assert len(job_ret) == 2
        assert job_ret[0].overrides == ["foo=1"]
        assert job_ret[0].cfg == {"foo": 1, "bar": 100}
        assert job_ret[1].overrides == ["foo=2"]
        assert job_ret[1].cfg == {"foo": 2, "bar": 100}
