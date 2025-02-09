

## Envoy pytooling

Python libraries, runners and checkers for Envoy proxy's CI

### Packages


#### [abstracts](abstracts)

version: 0.0.13.dev0

pypi: https://pypi.org/project/abstracts

---


#### [aio.functional](aio.functional)

version: 0.0.10.dev0

pypi: https://pypi.org/project/aio.functional

##### requirements:

- [abstracts](https://pypi.org/project/abstracts)

---


#### [aio.stream](aio.stream)

version: 0.0.3.dev0

pypi: https://pypi.org/project/aio.stream

##### requirements:

- [aiofiles](https://pypi.org/project/aiofiles)
- [aiohttp](https://pypi.org/project/aiohttp)

---


#### [aio.subprocess](aio.subprocess)

version: 0.0.5.dev0

pypi: https://pypi.org/project/aio.subprocess

---


#### [aio.tasks](aio.tasks)

version: 0.0.5.dev0

pypi: https://pypi.org/project/aio.tasks

##### requirements:

- [aio.functional](https://pypi.org/project/aio.functional)

---


#### [envoy.abstract.command](envoy.abstract.command)

version: 0.0.4.dev0

pypi: https://pypi.org/project/envoy.abstract.command

##### requirements:

- [abstracts](https://pypi.org/project/abstracts) >=0.0.11

---


#### [envoy.base.checker](envoy.base.checker)

version: 0.0.3.dev0

pypi: https://pypi.org/project/envoy.base.checker

##### requirements:

- [envoy.base.runner](https://pypi.org/project/envoy.base.runner) >=0.0.4

---


#### [envoy.base.runner](envoy.base.runner)

version: 0.0.5.dev0

pypi: https://pypi.org/project/envoy.base.runner

##### requirements:

- [coloredlogs](https://pypi.org/project/coloredlogs)
- [envoy.abstract.command](https://pypi.org/project/envoy.abstract.command)
- [frozendict](https://pypi.org/project/frozendict)
- [verboselogs](https://pypi.org/project/verboselogs)

---


#### [envoy.base.utils](envoy.base.utils)

version: 0.0.10

pypi: https://pypi.org/project/envoy.base.utils

##### requirements:

- [abstracts](https://pypi.org/project/abstracts)
- [pyyaml](https://pypi.org/project/pyyaml)
- [trycast](https://pypi.org/project/trycast)

---


#### [envoy.code_format.python_check](envoy.code_format.python_check)

version: 0.0.5.dev0

pypi: https://pypi.org/project/envoy.code_format.python_check

##### requirements:

- [abstracts](https://pypi.org/project/abstracts) >=0.0.12
- [aio.subprocess](https://pypi.org/project/aio.subprocess)
- [aio.tasks](https://pypi.org/project/aio.tasks)
- [envoy.base.checker](https://pypi.org/project/envoy.base.checker) >=0.0.2
- [envoy.base.utils](https://pypi.org/project/envoy.base.utils) >=0.0.3
- [flake8](https://pypi.org/project/flake8)
- [pep8-naming](https://pypi.org/project/pep8-naming)
- [yapf](https://pypi.org/project/yapf)

---


#### [envoy.dependency.pip_check](envoy.dependency.pip_check)

version: 0.0.5.dev0

pypi: https://pypi.org/project/envoy.dependency.pip_check

##### requirements:

- [abstracts](https://pypi.org/project/abstracts) >=0.0.12
- [envoy.base.checker](https://pypi.org/project/envoy.base.checker) >=0.0.2
- [envoy.base.utils](https://pypi.org/project/envoy.base.utils) >=0.0.3

---


#### [envoy.distribution.distrotest](envoy.distribution.distrotest)

version: 0.0.4.dev0

pypi: https://pypi.org/project/envoy.distribution.distrotest

##### requirements:

- [aiodocker](https://pypi.org/project/aiodocker)
- [envoy.base.checker](https://pypi.org/project/envoy.base.checker) >=0.0.2
- [envoy.base.utils](https://pypi.org/project/envoy.base.utils) >=0.0.3
- [envoy.docker.utils](https://pypi.org/project/envoy.docker.utils) >=0.0.2

---


#### [envoy.distribution.release](envoy.distribution.release)

version: 0.0.5.dev0

pypi: https://pypi.org/project/envoy.distribution.release

##### requirements:

- [envoy.abstract.command](https://pypi.org/project/envoy.abstract.command) >=0.0.3
- [envoy.base.runner](https://pypi.org/project/envoy.base.runner) >=0.0.4
- [envoy.github.abstract](https://pypi.org/project/envoy.github.abstract) >=0.0.16
- [envoy.github.release](https://pypi.org/project/envoy.github.release) >=0.0.8

---


#### [envoy.distribution.repo](envoy.distribution.repo)

version: 0.0.3.dev0

pypi: https://pypi.org/project/envoy.distribution.repo

##### requirements:

- [abstracts](https://pypi.org/project/abstracts) >=0.0.12
- [aio.functional](https://pypi.org/project/aio.functional) >=0.0.9
- [aio.subprocess](https://pypi.org/project/aio.subprocess) >=0.0.4
- [envoy.abstract.command](https://pypi.org/project/envoy.abstract.command) >=0.0.3
- [envoy.base.runner](https://pypi.org/project/envoy.base.runner) >=0.0.4
- [envoy.base.utils](https://pypi.org/project/envoy.base.utils) >=0.0.6
- [envoy.github.abstract](https://pypi.org/project/envoy.github.abstract) >=0.0.16
- [envoy.github.release](https://pypi.org/project/envoy.github.release) >=0.0.8

---


#### [envoy.distribution.verify](envoy.distribution.verify)

version: 0.0.3.dev0

pypi: https://pypi.org/project/envoy.distribution.verify

##### requirements:

- [envoy.base.checker](https://pypi.org/project/envoy.base.checker) >=0.0.2
- [envoy.distribution.distrotest](https://pypi.org/project/envoy.distribution.distrotest) >=0.0.3

---


#### [envoy.docker.utils](envoy.docker.utils)

version: 0.0.3.dev0

pypi: https://pypi.org/project/envoy.docker.utils

##### requirements:

- [aiodocker](https://pypi.org/project/aiodocker)

---


#### [envoy.docs.sphinx_runner](envoy.docs.sphinx_runner)

version: 0.0.4.dev0

pypi: https://pypi.org/project/envoy.docs.sphinx_runner

##### requirements:

- [colorama](https://pypi.org/project/colorama)
- [docutils](https://pypi.org/project/docutils) ~=0.16.0
- [envoy.base.runner](https://pypi.org/project/envoy.base.runner)
- [envoy.base.utils](https://pypi.org/project/envoy.base.utils)
- [sphinx](https://pypi.org/project/sphinx)
- [sphinx-copybutton](https://pypi.org/project/sphinx-copybutton)
- [sphinx-rtd-theme](https://pypi.org/project/sphinx-rtd-theme)
- [sphinx-tabs](https://pypi.org/project/sphinx-tabs)
- [sphinxcontrib-httpdomain](https://pypi.org/project/sphinxcontrib-httpdomain)
- [sphinxcontrib-serializinghtml](https://pypi.org/project/sphinxcontrib-serializinghtml)
- [sphinxext-rediraffe](https://pypi.org/project/sphinxext-rediraffe)

---


#### [envoy.github.abstract](envoy.github.abstract)

version: 0.0.17.dev0

pypi: https://pypi.org/project/envoy.github.abstract

##### requirements:

- [abstracts](https://pypi.org/project/abstracts) >=0.0.11
- [aio.functional](https://pypi.org/project/aio.functional) >=0.0.7
- [aio.tasks](https://pypi.org/project/aio.tasks) >=0.0.4
- [aiohttp](https://pypi.org/project/aiohttp)
- [envoy.base.runner](https://pypi.org/project/envoy.base.runner) >=0.0.4
- [gidgethub](https://pypi.org/project/gidgethub)
- [verboselogs](https://pypi.org/project/verboselogs)

---


#### [envoy.github.release](envoy.github.release)

version: 0.0.9.dev0

pypi: https://pypi.org/project/envoy.github.release

##### requirements:

- [abstracts](https://pypi.org/project/abstracts) >=0.0.11
- [aio.functional](https://pypi.org/project/aio.functional) >=0.0.7
- [aio.stream](https://pypi.org/project/aio.stream) >=0.0.2
- [aio.tasks](https://pypi.org/project/aio.tasks) >=0.0.4
- [aiohttp](https://pypi.org/project/aiohttp)
- [envoy.base.utils](https://pypi.org/project/envoy.base.utils) >=0.0.3
- [envoy.github.abstract](https://pypi.org/project/envoy.github.abstract) >=0.0.16
- [gidgethub](https://pypi.org/project/gidgethub)
- [packaging](https://pypi.org/project/packaging)
- [verboselogs](https://pypi.org/project/verboselogs)

---


#### [envoy.gpg.identity](envoy.gpg.identity)

version: 0.0.3.dev0

pypi: https://pypi.org/project/envoy.gpg.identity

##### requirements:

- [python-gnupg](https://pypi.org/project/python-gnupg)

---


#### [envoy.gpg.sign](envoy.gpg.sign)

version: 0.0.4.dev0

pypi: https://pypi.org/project/envoy.gpg.sign

##### requirements:

- [envoy.base.runner](https://pypi.org/project/envoy.base.runner) >=0.0.4
- [envoy.base.utils](https://pypi.org/project/envoy.base.utils) >=0.0.3
- [envoy.gpg.identity](https://pypi.org/project/envoy.gpg.identity) >=0.0.2

---


#### [mypy-abstracts](mypy-abstracts)

version: 0.0.7.dev0

pypi: https://pypi.org/project/mypy-abstracts

##### requirements:

- [mypy](https://pypi.org/project/mypy)

---


#### [pytest-patches](pytest-patches)

version: 0.0.4.dev0

pypi: https://pypi.org/project/pytest-patches

##### requirements:

- [pytest](https://pypi.org/project/pytest) >=3.5.0

---

