
import argparse
import pathlib
import tarfile
from functools import cached_property
from typing import Type, Union

from envoy.base import runner, utils
from envoy.gpg import identity

from .exceptions import SigningError
from .util import DirectorySigningUtil


class PackageSigningRunner(runner.Runner):
    """For a given `package_type` and `path` this will run the relevant signing
    util for the packages they contain."""

    _signing_utils = ()

    @classmethod
    def register_util(
            cls,
            name: str,
            util: Type[DirectorySigningUtil]) -> None:
        """Register util for signing a package type."""
        cls._signing_utils = getattr(cls, "_signing_utils") + ((name, util),)

    @property
    def extract(self) -> bool:
        return self.args.extract

    @cached_property
    def maintainer(self) -> identity.GPGIdentity:
        """A representation of the maintainer with GPG capabilities."""
        return self.maintainer_class(
            self.maintainer_name,
            self.maintainer_email,
            self.log)

    @property
    def maintainer_class(self) -> Type[identity.GPGIdentity]:
        return identity.GPGIdentity

    @property
    def maintainer_email(self) -> str:
        """Email of the maintainer if set."""
        return self.args.maintainer_email

    @property
    def maintainer_name(self) -> str:
        """Name of the maintainer if set."""
        return self.args.maintainer_name

    @property
    def package_type(self) -> str:
        """Package type - eg deb/rpm"""
        return self.args.package_type

    @property
    def path(self) -> pathlib.Path:
        """Path to the packages directory."""
        return pathlib.Path(self.args.path)

    @property
    def tar(self) -> str:
        return self.args.tar

    @cached_property
    def signing_utils(self) -> dict:
        """Configured signing utils - eg `DebSigningUtil`, `RPMSigningUtil`"""
        return dict(getattr(self, "_signing_utils"))

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        super().add_arguments(parser)
        parser.add_argument(
            "path",
            default="",
            help="Path to the directory containing packages to sign")
        parser.add_argument(
            "--extract",
            action="store_true",
            help=(
                "If set, treat the path as a tarball containing directories "
                "according to package_type"))
        parser.add_argument(
            "--tar",
            help="Path to save the signed packages as tar file")
        parser.add_argument(
            "--type",
            default="",
            choices=[c for c in self.signing_utils] + [""],
            help="Package type to sign")
        parser.add_argument(
            "--maintainer-name",
            default="",
            help=(
                "Maintainer name to match when searching for a GPG key "
                "to match with"))
        parser.add_argument(
            "--maintainer-email",
            default="",
            help=(
                "Maintainer email to match when searching for a GPG key "
                "to match with"))

    def archive(self, path: Union[pathlib.Path, str]) -> None:
        with tarfile.open(self.tar, "w") as tar:
            tar.add(path, arcname=".")

    def get_signing_util(self, path: pathlib.Path) -> DirectorySigningUtil:
        return self.signing_utils[path.name](path, self.maintainer, self.log)

    @runner.catches((identity.GPGError, SigningError))
    def run(self) -> None:
        if self.extract:
            self.sign_tarball()
        else:
            self.sign_directory()
        self.log.success("Successfully signed packages")

    def sign(self, path: pathlib.Path) -> None:
        self.log.notice(
            f"Signing {path.name}s ({self.maintainer}) {str(path)}")
        self.get_signing_util(path).sign()

    def sign_all(self, path: pathlib.Path) -> None:
        for directory in path.glob("*"):
            if directory.name in self.signing_utils:
                self.sign(directory)

    def sign_directory(self) -> None:
        self.sign(self.path)
        if self.tar:
            self.archive(self.path)

    def sign_tarball(self) -> None:
        if not self.tar:
            raise SigningError(
                "You must set a `--tar` file to save to "
                "when `--extract` is set")
        with utils.untar(self.path) as tardir:
            self.sign_all(tardir)
            self.archive(tardir)
