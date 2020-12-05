<blockquote class="callout">
Given enough eyeballs, all bugs are shallow.
<footer>Linus's Law (from The Cathedral and the Bazaar)</footer>
</blockquote>

Notes:

Some of you are probably familiar with this saying popular in the open source community that given enough eyeballs, all bugs are shallow. From what I can tell, this is primarily used to mean that when you have a large community reviewing patches and source code, someone is bound to notice when something goes wrong and be able to fix it.

I think there's another reasonable way to interpret this, though, and it's one that resonates deeply with my experience — when you have a large number of *users* deploying your application or library or whatever, they'll eventually hit all your bugs — even the most obscure ones.

With another few orders of magnitude **more** users, they might even *report* those edge cases back to you in some useful format.

--

<img src="images/setuptools-obscure-bug.png"
     alt="An comment on setuptools issue #2129 from jaraco. The text reads: This might be a contender for one of the most obscure bugs I've seen. Not only does it depend on the fact that your last name begins with 'egg' but it also depends on the fact that the egg-prefixed name appears in the last segment of the pathname, and it depends on the fact that you're on Windows, which provides compatibility with the decades-old 8.3 convention. I suspect there's another factor at play too that's causing the 8.3 filename to be used instead of the proper full filename."/>

<br/>
<div class="caption">From <a href="https://github.com/pypa/setuptools/issues/2129"><tt>setuptools</tt> issue #2129.</a></div>

<br/>

<ul>
<li class="fragment">User's name is A. Eggenberger, so his username is <tt>a.eggenberger</tt></li>
<li class="fragment">Default temporary folder is <tt>C:\Users\A9447~1.EGG</tt></li>
<li class="fragment"><tt>pkg_resources</tt> considers a folder to be an "egg" if its name ends in <tt>.egg</tt></li>
</ul>

Notes:

I was recently reminded of an excellent example of this that came up on the `setuptools` project this year. `setuptools` is over 15 years old at this point and is downloaded something like 2 million times *every day*, and back in May someone reported a very strange bug that as far as I know had been present for a long time, but no one had ever hit it, or at least hit it and then reported it.

To summarize the issue, a user showed up and said that in an executable he was building, `pkg_resources` would fail on his workstation and only *his* workstation — it even worked on other user accounts on the same machine!

It turns out that this is a *razor thin* edge case, which depended on a bunch of strange conditions, one of which was his actual lastname.

You see, the user's name is A. Eggenberger and his username is `a.eggenberger` — I'm not sure which of these two related facts is the relevant one, but the consequence is that the default name of his temporary folder was this weird thing using the old 8.3 convention, where files and folders could only have 8 letters, followed by a dot, followed by a 3-letter extension. Because his last name is Eggenberger, that folder name ended with `.EGG`, which was, coincidentally, an extension that `pkg_resources` was using the detect whether it was currently in a Python "egg" package. Since his temporary folder is not actually an egg package, this caused `pkg_resources` to fail with an error.

--

<span style="font-size: 3.5em; font-weight: bold">
What's unusual about this situation is that we heard about it.
</span>

Notes:

The user was able to work around this by changing the name of his temporary folder, and Jason fixed the bug with some better egg detection routines, but you can imagine there are probably similar bugs lurking around out there all over the place, just waiting to frustrate people to no end. What's unusual about this situation is that we heard about it.

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
<!-- .element: class="fragment"  style="max-width: 60%; border: solid 1px"-->

Notes:

Another example of a fairly obscure bug is issue #1875 on CPython's bug tracker, first reported way back in 2008 and not actually fixed until Python 3.8 was released last year (2019). This was a fairly obscure issue, but it was independently reported several times over the years — in fact, I independently discovered it in 2019, and I didn't comment on the issue at the time, which goes to show you that most people who encounter bugs don't take the time to track them down to their origin, much less provide you with a report you could use to find and fix the cause in your code.

This one was a fairly benign one, which is probably why it took so long to get fixed. The problem was that if you put certain types of syntax error in certain dead code branches of a program, they wouldn't get detected. So for example, it is a syntax error to have `break` outside of a loop, so this code *should* fail to compile, but prior to Python 3.8 it worked just fine. The reason for that has to do with the fact that it wasn't (maybe still isn't) possible to define this syntax error in the grammar due to the fact that the grammar had fairly strict limitations about how much it could know about the context of a given token. The way they fixed this is that the syntactic validity of a given Python program was checked twice — once when the program is parsed into bytecode, and then a second pass is made to ensure that no invalid bytecode operations were defined.

This bug is caused because during the first step — when the bytecode is compiled — it also goes through an optimization step, and if you use `if 0` or `while False` or any other sort of conditional with a literal false value, the optimizer knows that it's dead code and simply removes it — it emits no byte code, and as such it misses that second check for syntactic validity.

--


<span style="font-size: 3.5em; font-weight: bold">
Some bugs only show up once you've built an ecosystem.
</span>

Notes:

The thing about this kind of bug, though, is that really the only people who noticed it were people trying to implement their own versions of Python, or other rather abstruse things that depend on Python having such a large number of people that it would make sense for two people to implement the same protocol, or to build the other kinds of things — parsers, linters, code formatters, etc — where you'd actually notice this kind of thing.

--

<img src="images/bpo-35364-fromtimestamp-ignores-inheritance.png"
     alt="bugs.python.org issue #35364, wherein fromtimestamp() ignores inheritance if the time zone specified is not None"
     />

```python
>>> from datetime import datetime, timedelta, timezone
>>> class DatetimeSubclass(datetime): pass
...

>>> DatetimeSubclass.fromtimestamp(1607167800.0)
DatetimeSubclass(2020, 12, 5, 6, 30)

>>> DatetimeSubclass.fromtimestamp(1607167800.0, timezone.utc)
datetime.datetime(2020, 12, 5, 11, 30, tzinfo=datetime.timezone.utc)
```
<!-- .element: class="fragment" style="max-width: 60%; border: solid 1px" -->

Notes:

The last example bug is also from CPython. The problem here was that the `.fromtimestamp()` constructor, when called on a subclass of `datetime`, was inconsistent about whether it returned an instance of the subclass or an instance of the base class, `datetime`. If you called it without a time zone, it would give you the subclass, but if you gave it a time zone, it would return the base class.

This was happening because `.fromtimestamp()` uses datetime arithmetic if it needs to calculate UTC offsets, and at the time, `datetime` arithmetic *always* returned a `datetime.datetime`, even in subclasses. You had to explicitly override the arithmetic dunder methods to get them to return your subclass, and there were a bunch of places where it was hard to predict what you were getting, so you ended up having to implement all the methods of `datetime` just to get them to always return your subclass.

The thing is, the root of this bug turned out to be a *deliberate design decision*. In the standard library, most classes and builtins that offer alternate constructors will return an instance of the base class, not the derived class. One of the reasons for this is that subclasses are allowed to change their constructor, and so the base class can't know how to construct the subclass. The recommendation is that if you want the alternate constructors to return an instance of your subclass, you should explicitly override them.

--

<span style="font-size: 3.5em; font-weight: bold">
Predicting user priorities is difficult.
</span>

Notes:

But what I've found, at least in the case of `datetime`, is that people find it *really annoying* to re-implement the base class's entire interface just to make sure their subclass's type is persistent, and they don't actually seem to care when you call the class constructor as if it's the base class. This is just one particularly unusual manifestation of a wider problem that people were constantly reporting (or working around), but in all the time we've had interfaces that return instances of the subclass, I've only ever seen one class broken by it, and that was fairly easy to work around.


The people who originally designed Python and this system in general are extremely careful thinkers, and have exquisite design sensibilities. They got an enormous amount right, but they didn't predict that this would be a usability concern from their users until we got feedback from long tail users. That is a very humbling lesson.

--

<blockquote class="callout">
<span class="fragment disappearing-fragment nospace-fragment fade-out" data-fragment-index="0">No battle plan survives contact with the enemy.</span>
<span class="fragment nospace-fragment fade-in" data-fragment-index="0">[N]o plan of operations extends with any certainty beyond the first contact with the main hostile force.</span>
<footer>Helmuth von  Moltke the Elder</footer>
</blockquote>

Notes:

That brings me to my next point, which is that we sort of know this. It has often been said that No battle plan survives contact with the enemy, and the same goes for the code we release to our users. Interestingly, it also apparently goes for pithy sayings, because although I've attributed this to Helmuth von Moltke, this is *actually* a paraphrasing. The original quote is in German, but from what I can tell, a much closer translation is, "No plan of operations extends with any certainty beyond the first contact with the main hostile force." Evidently as soon as "the enemy" got a hold of that particular phrasing, they chopped it up and used it for parts.

And the same thing will happen to the programs you write when they hit your users. It's even spawned a whole genre of memes!

--

<img src="external-images/fair-use/cats-bowls.jpeg"
     alt="An image of three bowls of cat food neatly laid out labeled 'Developer: Makes a simple, intuitive UI' above an image of three cats climbing on top of one another to eat out of the bowls at odd angles and obviously interfering with one another, labeled 'Users'"
     class = "fragment nospace-fragment fade-out disappearing-fragment"
     data-fragment-index="0"
     style="height: 800px"
     />

<img src="external-images/fair-use/licking-cup.gif"
     alt="An animated image of a cartoon man trying to drink from the bottom of a cup, then lick the side of it, then drink from it without his arms, all failing to get any water in a comedic way"
     class = "fragment nospace-fragment fade-in disappearing-fragment"
     data-fragment-index="0"
     style="height: 600px"
     />

Notes:

The general idea behind these memes is that no matter how well you design your program, your users will do horrible things to it. They'll drill holes in your product and use it as a bong. They'll use it in the least efficient way possible, like these cats.

Or, like this guy, they'll seem to do everything *except* use your product as intended. I think sometimes the undercurrent is, "look how stupid our users are", but I prefer to see them as saying, "We should be humble about our ability to understand and predict our users' needs, because they'll often surprise us.

--

# Desire paths

<img src="external-images/desire-path-modified.jpg"
     alt="A paved path diverges from a 'desire path' — an area of grass worn from use"
     id="splash"
     />

Notes:

We can take a lesson from our users "using it wrong". I'm sure many of you have seen something like this before — it's called a desire path or sometimes a desire line. Someone builds this perfectly good sidewalk, and everyone sees that it's slightly longer than cutting across the grass, so they cut across the grass and all of a sudden there's a new, more convenient path dug into the grass.

This isn't people being stupid and not realizing that you're supposed to walk on the concrete. It's people being smart and efficient and showing you where you should have put the concrete in the first place. Ideally, you would keep an eye out for indications that a desire path is developing and try and lean into it — or try and add some more guard rails if it's really important that they stay within the lines!

--

<!-- .slide: data-visibility="hidden" -->

# The Curse of Knowledge

<img src="external-images/charades-modified.jpg"
     alt="A woman making some sort of claw gesture with her hands during a game of charades"
     id="splash"
     />

Notes:

Another theme I see in these memes is that no one reads the documentation. You're constantly answering questions that anyone could easily find in the documentation, or finding that people are failing to do something that's so basic it's in your repo's `README`.

Some of this is, of course, down to the fact that people don't read documentation, but some of it is what's called the Curse of Knowledge. This is a cognitive bias in which experts find it hard to predict what non-experts will find challenging, because they don't know (or remember) what it's like to not be an expert. You've probably experienced some form of this in a limited but visceral way if you've ever played charades. To you, your flailing and pointing and such *obviously* represents *Fast and the Furious: Tokyo Drift*, but that's because you've already got the necessary context, whereas the people on the couch think you're running around trying to get an incontinent cat to its litter box.

This is something that in a sense *only* new users are qualified to tell you about — they don't have the context or the expertise to understand whatever it is you are trying to explain to them, but if you pay attention to the ways that they fail, you'll be better able to design both your documentation and your product in a way that's truly intuitive, not just intuitive for you, the world's expert in your product.

--

# Unfamiliar environments

<center>
<video autoplay="true" loop="true" muted="true" width="720">
   <source src="external-images/fair-use/rtl-broken-whatsapp.mp4" type="video/mp4"> Your browser does not support the video tag.
</video>
</center>

From <a href="https://twitter.com/_saljam/status/1255197629123878914?s=20">@_saljam's April 2020 Twitter Thread</a> on RTL bugs.


Notes:

One last benefit I'd like to highlight about having a large user base is that as the size of your user base gets bigger, you start seeing problems that you may never have thought to test for, because they're not something you would experience in your daily life — but they are the reality for many people. For example, apparently when your WhatsApp interface is set to a language that is written right-to-left, playing a voice message makes the progress bar move in *both directions*. Evidently one of these indicators is implemented in something sensitive to RTL markers and the other isn't.

Maybe you've thought to test for this, and maybe you've thought to test that your thing works with a screen reader, and that it's colorblind-friendly, but the world is a wide and varied place, and likely you'll find that your users are telling you about some interesting way of being human that you've overlooked.

