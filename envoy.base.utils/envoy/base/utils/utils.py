#
# Provides shared utils used by other python modules
#

import io
import os
import pathlib
import tarfile
import tempfile
from configparser import ConfigParser
from contextlib import (
    ExitStack, contextmanager, redirect_stderr, redirect_stdout)
from typing import (
    Any, AsyncGenerator, Callable, Generator,
    Iterator, List, Optional, Set, Type, Union)

import yaml

from trycast import trycast  # type:ignore

from .exceptions import TypeCastingError


# See here for a list of known tar file extensions:
#   https://en.wikipedia.org/wiki/Tar_(computing)#Suffixes_for_compressed_files
# not all are listed here, and some extensions may require additional software
# to handle. This list can be updated as required
TAR_EXTS: Set[str] = {"tar", "tar.gz", "tar.xz", "tar.bz2"}


class ExtractError(Exception):
    pass


# this is testing specific - consider moving to tools.testing.utils
@contextmanager
def coverage_with_data_file(data_file: str) -> Iterator[str]:
    """This context manager takes the path of a data file and creates a custom
    coveragerc with the data file path included.

    The context is yielded the path to the custom rc file.
    """
    parser = ConfigParser()
    parser.read(".coveragerc")
    parser["run"]["data_file"] = data_file
    # use a temporary .coveragerc
    with tempfile.TemporaryDirectory() as tmpdir:
        tmprc = os.path.join(tmpdir, ".coveragerc")
        with open(tmprc, "w") as f:
            parser.write(f)
        yield tmprc


class BufferUtilError(Exception):
    pass


@contextmanager
def nested(*contexts):
    with ExitStack() as stack:
        yield [stack.enter_context(context) for context in contexts]


@contextmanager
def buffered(
        stdout: list = None,
        stderr: list = None,
        mangle: Optional[Callable[[list], list]] = None) -> Iterator[None]:
    """Captures stdout and stderr and feeds lines to supplied lists."""

    mangle = mangle or (lambda lines: lines)

    if stdout is None and stderr is None:
        raise BufferUtilError("You must specify stdout and/or stderr")

    contexts: List[
        Union[
            redirect_stderr[io.TextIOWrapper],
            redirect_stdout[io.TextIOWrapper]]] = []

    if stdout is not None:
        _stdout = io.TextIOWrapper(io.BytesIO())
        contexts.append(redirect_stdout(_stdout))
    if stderr is not None:
        _stderr = io.TextIOWrapper(io.BytesIO())
        contexts.append(redirect_stderr(_stderr))

    with nested(*contexts):
        yield

    if stdout is not None:
        _stdout.seek(0)
        stdout.extend(mangle(_stdout.read().strip().split("\n")))
    if stderr is not None:
        _stderr.seek(0)
        stderr.extend(mangle(_stderr.read().strip().split("\n")))


def extract(
        path: Union[pathlib.Path, str],
        *tarballs: Union[pathlib.Path, str]) -> pathlib.Path:
    if not tarballs:
        raise ExtractError(f"No tarballs specified for extraction to {path}")
    openers = nested(*tuple(tarfile.open(tarball) for tarball in tarballs))

    with openers as tarfiles:
        for tar in tarfiles:
            tar.extractall(path=path)
    return pathlib.Path(path)


@contextmanager
def untar(*tarballs: Union[pathlib.Path, str]) -> Iterator[pathlib.Path]:
    """Untar a tarball into a temporary directory.

    for example to list the contents of a tarball:

    ```
    import os

    from tooling.base.utils import untar


    with untar("path/to.tar") as tmpdir:
        print(os.listdir(tmpdir))

    ```

    the created temp directory will be cleaned up on
    exiting the contextmanager
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield extract(tmpdir, *tarballs)


def from_yaml(path: Union[pathlib.Path, str]) -> Union[dict, list, str, int]:
    """Returns the loaded python object from a yaml file given by `path`"""
    return yaml.safe_load(pathlib.Path(path).read_text())


def to_yaml(
        data: Union[dict, list, str, int],
        path: Union[pathlib.Path, str]) -> pathlib.Path:
    """For given `data` dumps as yaml to provided `path`.

    Returns `path`
    """
    path = pathlib.Path(path)
    path.write_text(yaml.dump(data))
    return path


def is_tarlike(path: Union[pathlib.Path, str]) -> bool:
    """Returns a bool based on whether a file looks like a tar file depending
    on its file extension.

    This allows for a provided path to save to, to dynamically be either
    considered a directory (to create) or a tar file (to create).
    """
    return any(str(path).endswith(ext) for ext in TAR_EXTS)


def ellipsize(text: str, max_len: int) -> str:
    """Truncate strings to a given length with an ellipsis suffix where
    required."""
    if len(text) <= max_len:
        return text
    return f"{text[:max_len - 3]}..."


def typed(tocast: Type, value: Any) -> Any:
    """Attempts to cast a value to a given type, TypeVar, or TypeDict.

    raises TypeError if cast value is `None`
    """

    if trycast(tocast, value) is not None:
        return value
    raise TypeCastingError(
        "Value has wrong type or shape for Type "
        f"{tocast}: {ellipsize(str(value), 10)}")


async def async_list(
        gen: AsyncGenerator,
        filter: Optional[Callable] = None) -> List:
    """Turn an async generator into a here and now list, with optional
    filter."""
    results = []
    async for x in gen:
        if filter and not filter(x):
            continue
        results.append(x)
    return results


@contextmanager
def cd_and_return(
        path: Union[pathlib.Path, str]) -> Generator[None, None, None]:
    """Changes working directory to given path and returns to previous working
    directory on exit."""
    prev_cwd = pathlib.Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(prev_cwd)


def to_bytes(data: Union[str, bytes]) -> bytes:
    return (
        bytes(data, encoding="utf-8")
        if not isinstance(data, bytes)
        else data)
