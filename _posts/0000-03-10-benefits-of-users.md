<blockquote class="callout">
Given enough eyeballs, all bugs are shallow.
<footer>Linus's Law (from The Cathedral and the Bazaar)</footer>
</blockquote>

--

<img src="images/setuptools-obscure-bug.png"
     alt="An comment on setuptools issue #2129 from jaraco. The text reads: This might be a contender for one of the most obscure bugs I've seen. Not only does it depend on the fact that your last name begins with 'egg' but it also depends on the fact that the egg-prefixed name appears in the last segment of the pathname, and it depends on the fact that you're on Windows, which provides compatibility with the decades-old 8.3 convention. I suspect there's another factor at play too that's causing the 8.3 filename to be used instead of the proper full filename."/>

<span style="font-size: 0.5em">From <a href="https://github.com/pypa/setuptools/issues/2129">`setuptools` issue #2129.</a></span>

--

<img src="images/bpo-1875-syntax-error.png"
     alt="bugs.python.org issue #1875, wherein if 0: return outside of a function does not raise a SyntaxError"
     />

```python
>>> def f():
...     if 0:
...         break  # This is a syntax error!
...     print("Hello")
... 
>>> f()
Hello
```
<!-- .element: class="fragment"  style="max-width: 60%"-->

--

<img src="images/bpo-35364-fromtimestamp-ignores-inheritance.png"
     alt="bugs.python.org issue #35364, wherein fromtimestamp() ignores inheritance if the time zone specified is not None"
     />


Notes:

- Requires user to have subclassed `datetime.datetime`
- Happens because:
    - `.fromutc()` uses datetime artihmetic
    - datetime arithmetic (used to) always return `datetime.datetime`, even in subclasses

--

<blockquote class="callout">
<span class="fragment disappearing-fragment nospace-fragment fade-out" data-fragment-index="0">No battle plan survives contact with the enemy.</span>
<span class="fragment nospace-fragment fade-in" data-fragment-index="0">[N]o plan of operations extends with any certainty beyond the first contact with the main hostile force.</span>
<footer>Helmuth von  Moltke the Elder</footer>
</blockquote>

--

<img src="external-images/fair-use/cats-bowls.jpeg"
     alt="An image of three bowls of cat food neatly laid out labeled 'Developer: Makes a simple, intuitive UI' above an image of three cats climbing on top of one another to eat out of the bowls at odd angles and obviously interfering with one another, labeled 'Users'"
     class = "fragment nospace-fragment fade-out disappearing-fragment"
     data-fragment-index="0"
     style="height: 800px"
     />

<img src="external-images/fair-use/dog-on-house.jpg"
     alt="Text on top reads 'Don't worry, it's super intuitive, the user will know how to use it.' Below that there is a picture of a dog laying sideways on top of the slanted roof of an empty dog house. The dog is labeled 'The user'"
     class = "fragment nospace-fragment fade-in-and-out disappearing-fragment"
     data-fragment-index="0"
     style="height:600px"
     />

<img src="external-images/fair-use/licking-cup.gif"
     alt="An animated image of a cartoon man trying to drink from the bottom of a cup, then lick the side of it, then drink from it without his arms, all failing to get any water in a comedic way"
     class = "fragment nospace-fragment fade-in disappearing-fragment"
     data-fragment-index="1"
     style="height: 600px"
     />

--

# Desire paths

<img src="external-images/desire-path-modified.jpg"
     alt="A paved path diverges from a 'desire path' — an area of grass worn from use"
     id="splash"
     />

--

# The Curse of Knowledge

<img src="external-images/charades-modified.jpg"
     alt="A woman making some sort of claw gesture with her hands during a game of charades"
     id="splash"
     />

--

# Unfamiliar environments

<center>
<video autoplay="true" loop="true" muted="true" width="720">
   <source src="external-images/fair-use/rtl-broken-whatsapp.mp4" type="video/mp4"> Your browser does not support the video tag.
</video>
</center>

From <a href="https://twitter.com/_saljam/status/1255197629123878914?s=20">@_saljam's April 2020 Twitter Thread</a> on RTL bugs.
