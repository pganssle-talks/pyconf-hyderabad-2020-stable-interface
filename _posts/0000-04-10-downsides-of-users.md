<blockquote class="callout">
With a sufficient number of users of an API,
it does not matter what you promise in the contract:
all observable behaviors of your system
will be depended on by somebody.
<footer><a href="https://www.hyrumslaw.com">Hyrum's Law</a></footer>
</blockquote>

--

<img src="images/bpo-37500-no-longer-optimized.png"
     alt="bugs.python.org issue #37500, where in if 0: is no longer optimized"
     />

--

<blockquote class="callout" style="font-size: 1.25em">
The real-word implications from my world are this: if your code has "if 0:" clauses in it, and you measure its coverage, then because the lines have not been optimized away, coverage.py will think the lines are a possible execution path, and will be considered a miss because they are not executed.  This will reduce your coverage percentage.
<footer>Ned Batchelder, <a href="https://bugs.python.org/issue37500#msg347362">bpo-37500</a></footer>
</blockquote>

<br/>

```python
def f() -> int:
    if 0:
        print("This code is unreachable!")

    if not __debug__:
        print("Running in optimized mode!")

    return 3
```

<div class="caption">This code would have 100% coverage prior to the change, but less than 100% coverage afterwards.</div>

--

# Packaging in Python: A Tale of Woe
<br/>

In Python 2.0, `distutils` was added to the standard library. This allowed distro maintainers:
<br/>
<br/>

1. A standard way of converting Python projects into Linux distro packages
2. System administrators a standard way of installing them directly onto target systems

<br/>
<br/>

Package authors would write a `setup.py` that runs `distutils.core.setup()`, and end users would execute any number of commands via `setup.py <command>` (e.g. `setup.py install` and `setup.py test`).


Notes:

There was not:

- PyPI
- `pip`
- `setuptools`

--

<img src="images/pypi-2003.png"
     alt="The PyPI website as of 2003."
     id="splash"
     />

--

<blockquote class="callout" style="font-size: 1.5em">
The sheer amount of features that Setuptools brings to the table must be stressed: namespace packages, optional dependencies, automatic manifest building by inspecting version control systems, web scraping to find packages in unusual places, recognition of complex version numbering schemes, and so on, and so on. Some of these features perhaps seem esoteric to many, but complex projects use many of them.
<footer><a href="https://blog.startifact.com/posts/older/a-history-of-python-packaging.html">Martin Faasen, A History of Python Packaging (2009)</a></footer>
</blockquote>

--

```bash
$ pip install attrs
Collecting attrs
  Downloading attrs-20.3.0.tar.gz (164 kB)
     |████████████████████████████████| 164 kB 6.1 MB/s
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
    Preparing wheel metadata ... done
Building wheels for collected packages: attrs
  Building wheel for attrs (PEP 517) ... done
  Created wheel for attrs: filename=attrs-20.3.0-py2.py3-none-any.whl size=49337
                           sha256=a6b44de70bcc7834e967dbea0b96c5f1ad03d438227c1e78f5dcbfbeb338607c
  Stored in directory: ~/.cache/pip/wheels/a4/3a/c7/ae1b7ae92f377604b64cab81594eb43ea843376139f34cc8a5
Successfully built attrs
Installing collected packages: attrs
Successfully installed attrs-20.3.0
```

<br/>

<div class="caption"><tt>pip</tt> (which stands for <em><tt>pip</tt> installs packages</em>) was introduced by Ian Bicking in 2008.</div>

--

<img src="external-images/gathering-storm.jpg"
     alt="Dark clouds gather over New York city"
     id="splash"
     />

Notes:

The packaging landscape was looking better than ever with `pip`, PyPI, `setuptools`, `easy_install` and `distutils`, and a number of other innovations I haven't mentioned here, but there were dark clouds gathering on the horizon.

The problem is that everything here was being done in an ad hoc fashion. People were building on top of one anothers' work, but there was no clearly specified interface. The interface you were targeting was "works with what people are already doing", which leaves less and less room for innovation when you can't meaningfully compete without being bug-for-bug compatible with `setuptools`.

--

# Packaging Problems

- Installing a package requires executing `setup.py`
    - Arbitrary code execution... often as root!
    - Compilation is time consuming, but no standards exist for distributing or installing binaries.
    - No way to specify dependencies for `setup.py` <sup>†</sup>
      <br/><br/>

- `distutils`
    - Largely unmaintained because of the long release cadences and the fact that changes would break arbitrary packages.
    - A sprawling module with a bunch of stuff unrelated to build code.
      <br/><br/>

- `setuptools`
    - Monkey-patches `distutils` on import
    - Also integrated with `pkg_resources` and `easy_install`
      <br/><br/>

- `pip`:
    - Always injects `import setuptools` as part of installation and build
    - Executes `setup.py` commands
      <br/><br/>

- `distribute`: Imported as `import setuptools`
  <br/><br/>

<span style="font-size: 0.25em"><sup>†</sup>Sort of</span>

--

<div class="fragment fade-out nospace-fragment disappearing-fragment" data-fragment-index="0">
<img src="images/pep517-pep.png"
     alt="PEP 517 -- A build-system independent format for source trees, Created 30-Sep-2015" />
 <br/>

<img src="images/pep518-pep.png"
     alt="PEP 517 -- A build-system independent format for source trees, Created 30-Sep-2015"
     />
</div>
<div class="fragment fade-in disappearing-fragment nospace-fragment" data-fragment-index="0">
<img src="images/pep632-pep.png"
     alt="PEP 632 -- Deprecate distutils module"
     />
</div>

- [**PEP 440**](https://www.python.org/dev/peps/pep-0440) - *Version Identification and Dependency Specification*
- [**PEP 453**](https://www.python.org/dev/peps/pep-0453) - *Explicit bootstrapping of pip in Python installations*
- [**PEP 503**](https://www.python.org/dev/peps/pep-0503) - *Simple Repository API*
- [**PEP 508**](https://www.python.org/dev/peps/pep-0508) - *Dependency Specification for Python Software Packages*
- [**PEP 513**](https://www.python.org/dev/peps/pep-0513) - *A Platform Tag for Portable Linux Built Distributions*
