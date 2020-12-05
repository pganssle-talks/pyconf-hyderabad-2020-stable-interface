# The Stable Interface Paradox
<br/>

<blockquote class="callout">
The smaller the user base, the harder it is to design an appropriate interface, but the larger the user base, the harder it is to change your interface.
</blockquote>

Notes:

What I'd like to talk to you about today is what I'm calling "the stable interface paradox". It's a phenomenon that I've observed in my open source work, but I think the phenomenon applies widely. The paradox is that the smaller your user base, the harder it is to design an appropriate interface, but the larger the user base, the harder it is to *change* that interface. This means that you are almost always best able to implement decisions about your interface *before* you have sufficient information to *make* those decisions. It means that a lot of interface design ends up as educated guesswork. It also means that you will almost always make some wrong decisions that will be very hard to change in the future.

--

<span style="font-size: 3.5em; font-weight: bold">
Users want stable interfaces!
</span>

Notes:

I think there are two main phenomena that drive the stable interface paradox. The first is that users want stable interfaces! I'm sure that this is intuitive to almost all of us, because we all use dozens of interfaces per day. It would be *supremely annoying* to wake up one day and find that you can't buy keyboards in your preferred layout anymore. If someone was offering an API endpoint, but they said that they would randomly change the interface at least once a month, there would need to be something extremely valuable at that endpoint for you to build anything on top of it, since it would be a significant maintenance burden to be constantly re-implementing your client.

Even smaller changes can be problematic, because as I mentioned, we're all surrounded by interfaces, and lots of small changes add up quickly. If you use 200 interfaces daily and each one of them breaks something once every 3 years, that means something you rely on is breaking *at least once a week*!

--

<span style="font-size: 3.5em; font-weight: bold">
Good interfaces are the product of user feedback.
</span>

Notes:

The other side of this tension is possibly less intuitive, and that's that you usually don't have enough information to design your interface until you have a lot of users. The reason for this is that almost all products do or should measure their success in user satisfaction. Whether it's an open source library or paid software, you should want to provide a useful and enjoyable experience, and the best way to find out if you're providing something useful is to observe, listen to and learn from the people using it.

And the thing is, this is not something you can solve with a few focus groups. I would argue that you need a fairly large user base to truly understand how well-designed your interface is.
