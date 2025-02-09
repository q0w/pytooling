
import abc
import argparse
import pathlib
from functools import cached_property
from typing import Iterable, List, Optional, Tuple

from flake8.main.application import (  # type:ignore
    Application as Flake8Application)

import yapf  # type:ignore

import abstracts

from aio.subprocess import run
from aio.tasks import concurrent

from envoy.base import checker, utils


FLAKE8_CONFIG = '.flake8'
YAPF_CONFIG = '.style.yapf'

# TODO(phlax): add checks for:
#      - isort


class APythonChecker(checker.AsyncChecker, metaclass=abstracts.Abstraction):
    checks = ("flake8", "yapf")

    @property
    def diff_file_path(self) -> Optional[pathlib.Path]:
        return (
            pathlib.Path(self.args.diff_file)
            if self.args.diff_file
            else None)

    @cached_property
    def flake8_app(self) -> Flake8Application:
        flake8_app = Flake8Application()
        flake8_app.initialize(self.flake8_args)
        return flake8_app

    @property
    def flake8_args(self) -> Tuple[str, ...]:
        return ("--config", str(self.flake8_config_path), str(self.path))

    @property
    def flake8_config_path(self) -> pathlib.Path:
        return self.path.joinpath(FLAKE8_CONFIG)

    @property
    @abc.abstractmethod
    def path(self) -> pathlib.Path:
        return super().path

    @property
    def recurse(self) -> bool:
        """Flag to determine whether to apply checks recursively."""
        return self.args.recurse

    @property
    def yapf_config_path(self) -> pathlib.Path:
        return self.path.joinpath(YAPF_CONFIG)

    @property
    def yapf_files(self) -> List[str]:
        return yapf.file_resources.GetCommandLineFiles(
            self.args.paths or [str(self.path)],
            recursive=self.recurse,
            exclude=yapf.file_resources.GetExcludePatternsForDir(
                str(self.path)))

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        super().add_arguments(parser)
        parser.add_argument(
            "--recurse",
            "-r",
            choices=["yes", "no"],
            default="yes",
            help="Recurse path or paths directories")
        parser.add_argument(
            "--diff-file",
            default=None,
            help="Specify the path to a diff file with fixes")

    async def check_flake8(self) -> None:
        """Run flake8 on files and/or repo."""
        errors: List[str] = []
        with utils.buffered(stdout=errors, mangle=self._strip_lines):
            self.flake8_app.run_checks()
            self.flake8_app.report()
        if errors:
            self.error("flake8", errors)

    async def check_yapf(self) -> None:
        """Run flake8 on files and/or repo."""
        futures = concurrent(
            self.yapf_format(python_file)
            for python_file
            in self.yapf_files)

        async for (python_file, (reformatted, encoding, changed)) in futures:
            self.yapf_result(python_file, reformatted, changed)

    async def on_check_run(self, check: str) -> None:
        if check not in self.failed and check not in self.warned:
            self.succeed(check, [check])

    async def on_checks_complete(self) -> int:
        if self.diff_file_path and self.has_failed:
            result = await run(
                ["git", "diff", "HEAD"],
                cwd=self.path,
                capture_output=True)
            self.diff_file_path.write_bytes(result.stdout)
        return await super().on_checks_complete()

    async def yapf_format(self, python_file: str) -> tuple:
        return python_file, yapf.yapf_api.FormatFile(
            python_file,
            style_config=str(self.yapf_config_path),
            in_place=self.fix,
            print_diff=not self.fix)

    def yapf_result(
            self,
            python_file: str,
            reformatted: str,
            changed: bool) -> None:
        if not changed:
            return self.succeed("yapf", [python_file])
        if self.fix:
            return self.warn("yapf", [f"{python_file}: reformatted"])
        if reformatted:
            return self.warn("yapf", [f"{python_file}: diff\n{reformatted}"])
        self.error("yapf", [python_file])

    def _strip_line(self, line: str) -> str:
        return (
            line[len(str(self.path)) + 1:]
            if line.startswith(f"{self.path}/")
            else line)

    def _strip_lines(self, lines: Iterable[str]) -> List[str]:
        return [
            self._strip_line(line)
            for line
            in lines
            if line]
