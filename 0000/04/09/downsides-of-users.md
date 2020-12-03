<blockquote class="callout">
With a sufficient number of users of an API,
it does not matter what you promise in the contract:
all observable behaviors of your system
will be depended on by somebody.
<footer><a href="https://www.hyrumslaw.com">Hyrum's Law</a></footer>
</blockquote>

Notes:

So far, I'd say that we've only covered some of the benefits of a large and thriving ecosystem — your code gets battle-tested and incrementally improved as your users do the testing for you and help guide your design decisions. Now it's time to get into the less rosy side of a large user base.

This is Hyrum's Law, which is something I bring up very frequently in design discussions (and as an aside I just recently learned it was formulated by one of my colleagues at Google!). Hyrum's law states that when the number of users of your API gets large enough, someone will depend on every observable behavior of your system.

What this means, basically, is that, frequently, your bugs end up as "load-bearing bugs", and people start depending on behaviors that, were you designing them from scratch, would be considered bugs.

For example, Joel Spolsky has a blog post called ["My First BillG review"](https://www.joelonsoftware.com/2006/06/16/my-first-billg-review/) where he explains that there's a peculiarity in the way Excel and Visual Basic handle datetime offsets — Excel uses January 1, 1900 as its "epoch" and Visual Basic uses December 31st, 1899, but for modern dates, the "offset from epoch" is always the same. It turns out that the reason for this is that Excel has a bug where it considers 1900 a leap year, but that this bug was not only not fixed but also *intentionally introduced* so that Excel could be compatible with Lotus 123 spreadsheets, which also had the same bug. Presumably the odd choice of epoch for Visual Basic was also made so that Visual Basic could be both correct for pre-1900 dates and also compatible with Excel for modern dates.

This is the flip side of having a large number of users — backwards compatibility concerns tend to dramatically curtail the available options you have for changing your interface.

--

<img src="images/bpo-37500-no-longer-optimized.png"
     alt="bugs.python.org issue #37500, where in if 0: is no longer optimized"
     />

Notes:

For example, going back to one of the obscure bugs we saw earlier. If you recall, we had a bug in CPython where optimizing out certain dead code branches would fail to catch certain syntax errors. Originally, this was fixed by changing the optimization so that the compiler would emit byte code for all the dead code, but it would have an unconditional jump that always skips over it — that way the byte code is still available for inspection, but you never execute it.

It turns out, even this minor change was noticed — and not because of whatever minor performance degradation you might see.

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

Notes:

You see, it turns out that `coverage.py` uses the emitted byte code to determine what lines are and are not covered by your tests. What this means is that if there's no byte code corresponding to a given line, `coverage.py` will consider that line "covered" and it won't show up as a miss. When the change went in in Python 3.8, people saw that their code coverage metrics went down and started complaining because their dead code was showing up as uncovered! Apparently some people use `if 0` or even worse, `__debug__`, which resolves to `True` or `False` at compile time, and apparently they don't want their code coverage numbers to change or to have to add a `# pragma: nocover` to their dead code statements.

So people were relying on this obscure bug based on an implementation detail of the way CPython chooses to optimize its code at compilation time. As Hyrum's law states, every observable feature will be depended on by *somebody*.

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

To see the kinds of problems this can cause, we should now take a journey back in time 20 years, to the beginning of the notion of creating Python packages. Prior to Python 2.0, the land of Python packaging was incredibly bleak, to put it mildly. There was no PyPI, no `pip install`, no `setuptools`, and prior to Python 2.0 there wasn't even a `distutils`. This is one reason that Python's "batteries included" philosophy was seen as such a strength — it was similarly painful to depend on third-party code in most if not all other languages, so the fact that basically all the useful modules tended to be incorporated into CPython core was incredibly convenient.

Things started to change when `distutils` was introduced. `distutils` was intended to be a standard way of converting Python projects into Linux distro packages (and later, Windows packages as well), and for sysadmins to install their projects.

Now, instead of having completely ad-hoc installation instructions that were different for every package, package authors could just write a `setup.py` file that runs `distutils.core.setup()` and a number of commands — including `build`, `install` and `test` — would be provided for users.

--

<img src="images/pypi-2003.png"
     alt="The PyPI website as of 2003."
     id="splash"
     />

Notes:

To solve the problem of distributing these packages, in 2002, Richard Jones (in collaboration with several others) created PyPI, as a more formalized version of a previous package index called the Vaults of Parnassus. The idea was that `distutils` would generate metadata in a specified format and PyPI would host the metadata. No packages were actually hosted on PyPI, the metadata just included a link to a place you could go and download the package. There was still no equivalent of `pip install` — you had to download the package, then read the metadata to figure out what other packages it depends on, then go back to PyPI and download those, then install them all manually in the right order.

--

<blockquote class="callout" style="font-size: 1.5em">
The sheer amount of features that Setuptools brings to the table must be stressed: namespace packages, optional dependencies, automatic manifest building by inspecting version control systems, web scraping to find packages in unusual places, recognition of complex version numbering schemes, and so on, and so on. Some of these features perhaps seem esoteric to many, but complex projects use many of them.
<footer><a href="https://blog.startifact.com/posts/older/a-history-of-python-packaging.html">Martin Faasen, A History of Python Packaging (2009)</a></footer>
</blockquote>

Notes:

So that sounds like a huge pain, and in 2004 Phillip Eby released a solution to this as part of `setuptools`. `setuptools` was basically extensions to `distutils` that brought in a huge number of features for building, installing and managing your packages. This included the utility `easy_install`, which worked a lot like `pip` — it would go to PyPI, download the package you want, then figure out what all of its dependencies are and download those, etc. This was also built directly into the `setup.py install` command. As you can imagine, this was a very popular extension, to the point where people started assuming it was installed, sometimes even without declaring any sort of dependency on it.

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

Notes:

Fast forward to 2008 and Ian Bicking introduces `pip`, which works a lot like `easy_install`, but is a lot more user-friendly, and I believe it did the dependency resolution at a slightly earlier stage in the process. Don't quote me on this, but I think it was around this time that PyPI started hosting packages directly, rather than simply acting as an index linking to files hosted elsewhere. 

--

<img src="external-images/gathering-storm.jpg"
     alt="Dark clouds gather over New York city"
     id="splash"
     />

Notes:
At this point, the Python packaging story is starting to take shape into something resembling the current state of things — the packaging landscape was looking better than ever with `pip`, PyPI, `setuptools`, `easy_install` and `distutils`, and a number of other innovations I haven't mentioned here, but there were dark clouds gathering on the horizon.

The problem is that most things here were being done in an ad hoc fashion. People were building on top of one another's work, but there was no clearly specified interface. The interface you were targeting was "works with what people are already doing", which leaves less and less room for innovation when you can't meaningfully compete without, for example, being bug-for-bug compatible with `setuptools`.

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
     alt="PEP 518 -- Specifying Minimum Build System Requirements for Python Projects, Created 10-May-2016"
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

Notes:

And now, because we have thousands or hundreds of thousands of packages depending on unspecified or under-specified characteristics of a complex inter-woven ecosystem of packages, we have a huge tangled mess to sort out and an extremely constrained design space. At the end of the day, we will need to break many assumptions that people have spent over a decade relying on, but the end goal is to start building inter-operability standards for packaging in Python that are better defined and allow the future of packaging in Python to evolve.

The biggest players here are PEP 518 and PEP 517, which allow you to declare that your package is built with a backend other than `setuptools`, and also define the interface between backends like `setuptools` and front-ends like `pip`. This has allowed other players like `flit` and `poetry` to enter the scene, but because of the crushing weight of backwards compatibility it's incredibly slow-going. It's been 5 years since PEP 517 was accepted, and only recently was its status as "provisional" changed to "final" — and there were many changes that could only be made *after* we got feedback from users that something about PEP 517 wasn't suitable for their use case.

Usually these complaints did not take the form of a kind note written in calligraphy on embroidered stationary. These PEPs are very carefully designed with maximum backwards compatibility in mind, and the changes required by end users are fairly minor, but still it's often disheartening to see the sort of anger it evokes in people that the PyPA would dare change something that already works (or at least seems to in most cases).

PyPA packages are partially so valuable because of the huge ecosystem they exist in, and the large number of users we have to give feedback. That huge number of users is also likely their greatest liability, because it builds an enormous amount of inertia into the system that makes it very difficult to make any changes without creating a lot of extra work for people or creating a lot of confusion as all of a sudden best practices in packaging keep changing.
