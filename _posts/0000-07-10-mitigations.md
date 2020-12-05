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

Notes:

So, I've given you some problems, and maybe some advice about listening to your users — which of course I tempered with the dispiriting notion that even if you listen to your users you can't respond to their feedback anyway, so what do I think you should do?

Well, I've got my eye on this bunker where we can all hide out as we wait for the inevitable downfall of civilization when the mad fever dream that was the general purpose computer finally comes to an end.

But no, more seriously, I don't think that this is an apocalyptic vision. In fact, I don't even think it's particularly new.

--

<img src="external-images/carriages-modified.jpg"
     alt="A road occupied by horses and carriages"
     id="splash"
     />

<div class="caption">Roads were originally designed for a primitive form of car propelled by some sort of a four-legged ungulate.</div>

Notes:

Backwards compatibility and technical debt have existed since long before computers existed. There are thousands of miles of railroads laid with specific gauges all around the world that it would be incredibly expensive to change. At some point a network of roads originally designed for horses and carriages had to be retrofitted to accommodate cars and trucks.

I don't think I have any one answer for you, but I can give you a few heuristics that I imagine most maintainers of large projects have internalized at least to some degree.

--

<span style="font-size: 3.5em; font-weight: bold">
Design for change.
</span>

--

<span style="font-size: 3.5em; font-weight: bold">
Avoid tight coupling.
</span>

--

<span style="font-size: 3.5em; font-weight: bold">
Minimize your public interface.
</span>

--

<span style="font-size: 3.5em; font-weight: bold">
Be decisive.
</span>

--

<img src="external-images/vermeer-woman-with-a-balance-modified.jpg"
     alt="A cropped version of Johannes Vermeer's Woman with a Balance; a painting of a seemingly pregnant woman holding a small balance scale. (Scholarly opinion is that she is not supposed to be pregnant for various reasons, but to modern eyes she looks heavily pregnant)."
     id="splash"
     />

Notes:

At the end of the day, though, the real lesson to be taken from the stable interface paradox is that because keeping a stable interface and responding to user feedback are in tension, there is no one right answer to how to run a project. These heuristics will help, but you will get into an uncomfortable position where you must balance stability against responding to user feedback.

--

# Churn budget

<img src="external-images/piggy-bank.jpg"
     alt="A smashed piggy bank with a UK £20 note and some coins inside"
     style="height: 600px"
     id="splash"
     />

- How important is the change?
+ How many people will it affect?
+ How painful will it be for affected users?
+ How much goodwill have you spent recently?

