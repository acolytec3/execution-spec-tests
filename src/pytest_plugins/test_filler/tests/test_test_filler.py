"""
Test the forks plugin.
"""
import json
import os
import textwrap
from pathlib import Path

import pytest


def get_all_files_in_directory(base_dir):  # noqa: D103
    base_path = Path(base_dir)
    return [f.relative_to(os.getcwd()) for f in base_path.rglob("*") if f.is_file()]


def count_keys_in_fixture(file_path):  # noqa: D103
    with open(file_path, "r") as f:
        data = json.load(f)
        if not isinstance(data, dict):  # Ensure the loaded data is a dictionary
            raise ValueError(
                f"Expected a dictionary in {file_path}, but got {type(data).__name__}."
            )
        return len(data)


test_module_merge = textwrap.dedent(
    """\
    import pytest

    from ethereum_test_tools import Account, Environment, TestAddress

    @pytest.mark.valid_from("Merge")
    @pytest.mark.valid_until("Shanghai")
    def test_merge_one(state_test):
        state_test(env=Environment(),
                    pre={TestAddress: Account(balance=1_000_000)}, post={}, txs=[])

    @pytest.mark.valid_from("Merge")
    @pytest.mark.valid_until("Shanghai")
    def test_merge_two(state_test):
        state_test(env=Environment(),
                    pre={TestAddress: Account(balance=1_000_000)}, post={}, txs=[])
    """
)
test_count_merge = 4

test_module_shanghai = textwrap.dedent(
    """\
    import pytest

    from ethereum_test_tools import Account, Environment, TestAddress

    @pytest.mark.valid_from("Merge")
    @pytest.mark.valid_until("Shanghai")
    def test_shanghai_one(state_test):
        state_test(env=Environment(),
                    pre={TestAddress: Account(balance=1_000_000)}, post={}, txs=[])

    @pytest.mark.parametrize("x", [1, 2, 3])
    @pytest.mark.valid_from("Merge")
    @pytest.mark.valid_until("Shanghai")
    def test_shanghai_two(state_test, x):
        state_test(env=Environment(),
                    pre={TestAddress: Account(balance=1_000_000)}, post={}, txs=[])
    """
)

test_count_shanghai = 8
test_count = test_count_merge + test_count_shanghai


@pytest.mark.parametrize(
    "args, expected_fixture_files, expected_fixture_counts",
    [
        pytest.param(
            [],
            [
                Path("fixtures/merge/module_merge/merge_one.json"),
                Path("fixtures/merge/module_merge/merge_two.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_one.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_two.json"),
            ],
            [2, 2, 2, 6],
            id="default-args",
        ),
        pytest.param(
            ["--flat-output"],
            [
                Path("fixtures/merge_one.json"),
                Path("fixtures/merge_two.json"),
                Path("fixtures/shanghai_one.json"),
                Path("fixtures/shanghai_two.json"),
            ],
            [2, 2, 2, 6],
            id="flat-output",
        ),
        pytest.param(
            ["--flat-output", "--output", "other_fixtures"],
            [
                Path("other_fixtures/merge_one.json"),
                Path("other_fixtures/merge_two.json"),
                Path("other_fixtures/shanghai_one.json"),
                Path("other_fixtures/shanghai_two.json"),
            ],
            [2, 2, 2, 6],
            id="flat-output_custom-output-dir",
        ),
        pytest.param(
            ["--flat-output", "--output", "other_fixtures", "--enable-hive"],
            [
                Path("other_fixtures/merge_one.json"),
                Path("other_fixtures/merge_two.json"),
                Path("other_fixtures/shanghai_one.json"),
                Path("other_fixtures/shanghai_two.json"),
            ],
            [2, 2, 2, 6],
            id="flat-output_custom-output-dir_enable-hive",
        ),
        pytest.param(
            ["--single-fixture-per-file"],
            [
                Path("fixtures/merge/module_merge/merge_one__fork_Merge.json"),
                Path("fixtures/merge/module_merge/merge_one__fork_Shanghai.json"),
                Path("fixtures/merge/module_merge/merge_two__fork_Merge.json"),
                Path("fixtures/merge/module_merge/merge_two__fork_Shanghai.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_one__fork_Merge.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_one__fork_Shanghai.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_two__fork_Merge_x_1.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_two__fork_Merge_x_2.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_two__fork_Merge_x_3.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_two__fork_Shanghai_x_1.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_two__fork_Shanghai_x_2.json"),
                Path("fixtures/shanghai/module_shanghai/shanghai_two__fork_Shanghai_x_3.json"),
            ],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            id="single-fixture-per-file",
        ),
        pytest.param(
            ["--single-fixture-per-file", "--output", "other_fixtures"],
            [
                Path("other_fixtures/merge/module_merge/merge_one__fork_Merge.json"),
                Path("other_fixtures/merge/module_merge/merge_one__fork_Shanghai.json"),
                Path("other_fixtures/merge/module_merge/merge_two__fork_Merge.json"),
                Path("other_fixtures/merge/module_merge/merge_two__fork_Shanghai.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_one__fork_Merge.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_one__fork_Shanghai.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Merge_x_1.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Merge_x_2.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Merge_x_3.json"),
                Path(
                    "other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Shanghai_x_1.json"
                ),
                Path(
                    "other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Shanghai_x_2.json"
                ),
                Path(
                    "other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Shanghai_x_3.json"
                ),
            ],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            id="single-fixture-per-file_custom_output_dir",
        ),
        pytest.param(
            ["--single-fixture-per-file", "--output", "other_fixtures", "--enable-hive"],
            [
                Path("other_fixtures/merge/module_merge/merge_one__fork_Merge.json"),
                Path("other_fixtures/merge/module_merge/merge_one__fork_Shanghai.json"),
                Path("other_fixtures/merge/module_merge/merge_two__fork_Merge.json"),
                Path("other_fixtures/merge/module_merge/merge_two__fork_Shanghai.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_one__fork_Merge.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_one__fork_Shanghai.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Merge_x_1.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Merge_x_2.json"),
                Path("other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Merge_x_3.json"),
                Path(
                    "other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Shanghai_x_1.json"
                ),
                Path(
                    "other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Shanghai_x_2.json"
                ),
                Path(
                    "other_fixtures/shanghai/module_shanghai/shanghai_two__fork_Shanghai_x_3.json"
                ),
            ],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            id="single-fixture-per-file_custom_output_dir_enable-hive",
        ),
        pytest.param(
            ["--flat-output", "--single-fixture-per-file"],
            [
                Path("fixtures/merge_one__fork_Merge.json"),
                Path("fixtures/merge_one__fork_Shanghai.json"),
                Path("fixtures/merge_two__fork_Merge.json"),
                Path("fixtures/merge_two__fork_Shanghai.json"),
                Path("fixtures/shanghai_one__fork_Merge.json"),
                Path("fixtures/shanghai_one__fork_Shanghai.json"),
                Path("fixtures/shanghai_two__fork_Merge_x_1.json"),
                Path("fixtures/shanghai_two__fork_Merge_x_2.json"),
                Path("fixtures/shanghai_two__fork_Merge_x_3.json"),
                Path("fixtures/shanghai_two__fork_Shanghai_x_1.json"),
                Path("fixtures/shanghai_two__fork_Shanghai_x_2.json"),
                Path("fixtures/shanghai_two__fork_Shanghai_x_3.json"),
            ],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            id="flat-single-per-file_flat-output",
        ),
    ],
)
def test_fixture_output_based_on_command_line_args(
    testdir, args, expected_fixture_files, expected_fixture_counts
):
    """
    Test:
    - fixture files are created at the expected paths.
    - no other files are present in the output directory.
    - each fixture file contains the expected number of fixtures.

    The modules above generate the following test cases:
        tests/merge/test_module_merge.py::test_merge_one[fork_Merge] PASSED
        tests/merge/test_module_merge.py::test_merge_one[fork_Shanghai] PASSED
        tests/merge/test_module_merge.py::test_merge_two[fork_Merge] PASSED
        tests/merge/test_module_merge.py::test_merge_two[fork_Shanghai] PASSED
        tests/shanghai/test_module_shanghai.py::test_shanghai_one[fork_Merge] PASSED
        tests/shanghai/test_module_shanghai.py::test_shanghai_one[fork_Shanghai] PASSED
        tests/shanghai/test_module_shanghai.py::test_shanghai_two[fork_Merge-x=1] PASSED
        tests/shanghai/test_module_shanghai.py::test_shanghai_two[fork_Merge-x=2] PASSED
        tests/shanghai/test_module_shanghai.py::test_shanghai_two[fork_Merge-x=3] PASSED
        tests/shanghai/test_module_shanghai.py::test_shanghai_two[fork_Shanghai-x=1] PASSED
        tests/shanghai/test_module_shanghai.py::test_shanghai_two[fork_Shanghai-x=2] PASSED
        tests/shanghai/test_module_shanghai.py::test_shanghai_two[fork_Shanghai-x=3] PASSED
    """
    tests_dir = testdir.mkdir("tests")

    merge_tests_dir = tests_dir.mkdir("merge")
    test_module = merge_tests_dir.join("test_module_merge.py")
    test_module.write(test_module_merge)

    shanghai_tests_dir = tests_dir.mkdir("shanghai")
    test_module = shanghai_tests_dir.join("test_module_shanghai.py")
    test_module.write(test_module_shanghai)

    testdir.copy_example(name="pytest.ini")
    args.append("-v")
    result = testdir.runpytest(*args)
    result.assert_outcomes(
        passed=test_count,
        failed=0,
        skipped=0,
        errors=0,
    )
    if "--output" in args:
        output_dir = Path(args[args.index("--output") + 1]).absolute()
    else:
        output_dir = Path("fixtures").absolute()
    assert output_dir.exists()

    all_files = get_all_files_in_directory(output_dir)

    for fixture_file, fixture_count in zip(expected_fixture_files, expected_fixture_counts):
        assert fixture_file.exists()
        assert fixture_count == count_keys_in_fixture(fixture_file)

    assert set(all_files) == set(
        expected_fixture_files
    ), f"Unexpected files in directory: {set(all_files) - set(expected_fixture_files)}"
