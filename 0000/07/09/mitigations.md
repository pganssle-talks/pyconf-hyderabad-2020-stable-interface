<span style="font-size: 5em; font-weight: bold">What should we do?</span>

--

# UX Research

<img src="images/pip-ux-design.png"
     alt="Screenshot from pip's documentation about the UX design research they are undertaking"
     />

<div class="caption"><tt>pip</tt> is undertaking <a href="https://pip.pypa.io/en/stable/ux_research_design/">UX Research</a> to anticipate user needs.</div>


--

# Pre-releases

<img src="external-images/python-release-cadence.png"
     alt="A chart from PEP 602 illustrating Python's annual release cadence, including pre-alpha, alpha and beta phases."
     style="max-height: 750px"
     />

<div class="caption">CPython makes extensive use of pre-releases.</div>

--

# Provisional interfaces

<div style="display: flex; flex-direction: column;">

<img src="images/asyncio-provisional.png"
     alt="The asyncio module was considered provisional in Python 3.5"
     />

<img src="images/pep484-type-hints.png"
     alt="PEP 484: Type Hints, which was created in September 2014 but is still Provisional"
     />

<div class="caption">Marking an interface as provisional is a variation on pre-releases.</div>

</div>

--

# Deprecations

<img src="images/easy_install_deprecated.png"
     alt="A warning on the `easy_install` documentation indicating it is deprecated"
     style="width: 1000px"
     />
<br/>
<br/>
<img src="images/setup-py-test-deprecated.png"
     alt="A warning on the documentation for setup.py test indicating that it is deprecated"
     style="width: 1000px"
     />

<br/>

```
$ python2.7 -m pip list
DEPRECATION: Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python
as Python 2.7 is no longer maintained. pip 21.0 will drop support for Python 2.7 in January 2021. More
details about Python 2 support in pip, can be found at
https://pip.pypa.io/en/latest/development/release-process/#python-2-support

Package    Version
---------- ------------
pip        20.1.1
setuptools 39.0.1
```

--

# Deprecations

<img src="images/hn-comment-packaging.png"
     alt="HN Comment, text reads: Python Packaging is not hard anymore \n Would you tell us which is the 'right way to do it' nowadays? Possibly, in a maintainable, kind-of-officially supported way that doesn't change or disappear in a few months? \n Please note​: I use Python professionally since 2005, I've been involved in a lot of Python packaging for production apps (including giving some talks on the bad state of Python packaging at Europython around 2010) and I had followed closely the then-failed distutils2 effort. And I still don't know what's the 'right and easy way to do it'."
     />
     <br/>
     <br/>

<img src="images/victor-stinner-twitter-20y.png"
     alt="Tweet from Victor Stinner: I'm using Python for 20 years and I only know 'python http://setup.py install' or 'pip install something' commands. Hopefully, I didn't learn setup.cfg or pyproject.toml new things, since it seems like the latest hype packaging project is deprecated 6 months later :-)"
     />

--


<div style="font-size: 5em; font-weight: bold"
     class="fragment fade-out disappearing-fragment nospace-fragment"
     data-fragment-index="0"
    >
What should we do?
</div>


<img src="external-images/bunker-entrance-modified.jpg"
     alt="The entrance to a bunker in the woods"
     id="splash"
     class="fragment disappearing-fragment nospace-fragment"
     data-fragment-index="0"
     />

<div class="caption fragment disappearing-fragment nospace-fragment"
     data-fragment-index="0"
     >
A secret bunker in Sweden where we can hide out from the consequences of our hubris.</div>
</div>

