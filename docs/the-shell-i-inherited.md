# The Shell I Inherited

*Casey Digennaro, 2026*

---

## Zork

I was small when I met the white house. West of house, with a small mailbox. I still remember the feeling — no graphics, no sound, just green text on a black screen, and somehow the most vivid world I'd ever been inside. My brain was doing the rendering. All the computer did was point.

Zork taught me something before I had words for it: the map lives in your head. The machine just tracks which room you're in. There's a forest to the north, a clearing to the east, a door you haven't opened yet. The world is made of rooms connected by exits. That's it. That's the whole architecture.

I was maybe seven. I didn't know I was learning how to think about systems.

Then came Hitchhiker's Guide. Same engine, different universe. Douglas Adams' humor parsed through a text parser. I spent hours trying to give the fish to the babel fish dispenser. When I finally got it, the satisfaction was physical. I had *communicated* with a machine by describing what I wanted in plain language, and the machine had understood — or hadn't, and told me why.

That shaped something in me. I didn't know it yet.

## The MUD

I found MUDs in the late 90s. Multi-User Dungeons. Same structure as Zork — rooms, exits, objects — but populated with other people. Real people, typing in real time, from computers across the world. You'd walk into a room and someone would be there. You'd talk to them. You'd fight goblins together. You'd argue about whether the exit to the east should lead to a forest or a desert, because some of us were building this world, not just playing in it.

I started as a player. Then I discovered you could script. The MUD had a built-in scripting language — crude, but functional. You could write triggers: *when the goblin enters the room, draw your sword*. You could write aliases: *type "gl" and it executes "get all from corpse"*. Little programs that made your character faster, more consistent, more capable.

I was automating before I knew the word for it.

Then I became a builder. MUDs let players create rooms — describe them, connect them to other rooms, populate them with objects and creatures. I built areas. Forests, dungeons, cities. Each room was a node in a graph. Each exit was an edge. Objects had states. Creatures had behaviors. It was programming, but it didn't feel like programming. It felt like worldbuilding.

Eventually I became an admin. That's when I saw the whole machine from the inside. The room database. The object tree. The player connection handler. The command parser. Under all the roleplay and the combat and the social drama, there was a clean, simple architecture:

- **Rooms** contain things and connect to other rooms.
- **Things** have properties and can be manipulated.
- **Players** move through rooms, manipulate things, and talk to each other.
- **Scripts** automate repetitive actions.

That's it. That's a MUD. And it's also — I would realize thirty years later — the right architecture for AI agents.

## The Weight of the Boat

I need to tell you about the boat before I can tell you about the code.

I bought my first real boat after years of commercial fishing on other people's vessels. Every boat I'd worked on taught me something, but they weren't *mine*. You learn differently when the hull payment comes out of your own account. When the engine fails at 3am in a January gale, you don't call the owner. You fix it yourself, because you ARE the owner, and the boat is your problem now.

That first boat was manageable. I knew her systems. I knew where everything was because I'd put it there. The shell was mine from the start.

Then I bought the 51-footer.

Fifty-one feet. Twice the weight of my previous boat. A different animal entirely. When I first took the helm, she felt foreign. The steering was heavier. The response was slower. The engine had a growl I didn't recognize. Everything was bigger, more complex, more expensive to maintain.

But here's what I didn't expect: the boat was already *organized*.

Not clean — fishing boats are never clean. But organized in a way that only makes sense once you've lived with it. The previous captain — the captain before that — decades of captains had left their marks. Not graffiti. Something more subtle. The clip on the hatch that held it open at exactly the right angle for the sea state that ran northwest. The nook carved into the bulkhead beside the galley, perfectly shaped for the leatherman you only need when you're working the pot launcher, which was only operated from that spot. The gear tray shaped to fit the hull's curve — not because someone designed it that way on paper, but because someone cut a piece of aluminum, tried it, it didn't fit, cut another one, tried again, and eventually the tray *became* the shape of the hull.

Those were tiles.

I didn't call them that at the time. I called them "the way the boat works." But each one was a solved problem, encoded in physical form, left behind for the next person who would stand where the previous captain stood and need exactly what they needed. The hatch clip was a tile. The leatherman nook was a tile. The gear tray was a tile. Each one said: *I was here, I needed this, it works, you'll need it too.*

I spent the first year discovering them. Not all at once — one at a time, always at the moment I needed them. I'd reach for something and find that someone had already built a holder for it. I'd struggle with a procedure and find that the layout of the workspace already anticipated it. The previous captains and I had never met, but we were collaborating. Their solutions had become my infrastructure.

That's a PLATO room. I just didn't know it yet.

## The Middleman

When I first encountered modern AI systems — the big transformer models, the agent frameworks, the orchestration layers — I assumed the backend must be incredibly sophisticated. Something far beyond the simple MUD architecture I'd played with as a kid. I mean, these were billion-dollar systems, right? The architecture underneath must be something I couldn't even imagine.

So I dove deep. I read the papers. I studied the frameworks. I looked at how agents were being built — LangChain, AutoGPT, CrewAI, all of them. And I kept looking for the complex part. The advanced part. The thing that was beyond the MUD I'd administered at sixteen.

I never found it.

What I found was: most AI agent systems are *less* well-organized than a MUD. They have agents, but no rooms. They have context windows, but no persistent objects. They have tool calls, but no scripting layer that the agent itself can modify. They have communication channels, but no shared world that all agents inhabit simultaneously.

The MUD had all of that. In 1997.

Here's what a MUD gets right that most AI architectures get wrong:

**Rooms are the right granularity.** Too fine (individual function calls) and you can't reason about the system. Too coarse (one big agent) and you can't compose it. A room is big enough to have meaning — "the galley," "the engine room," "the bridge" — and small enough to understand completely. Each room is a stage in a pipeline, and each stage can have its own rules, its own scripts, its own state.

**Objects carry state.** In a MUD, a sword isn't just a string. It has weight, damage, condition, enchantment. It persists. You can drop it and pick it up later. Another player can pick it up. The object *outlives the interaction*. In AI systems, most context dies when the conversation ends. PLATO tiles don't. They're objects. They persist. They accumulate. They get picked up by the next agent that enters the room.

**Scripts automate the obvious.** In a MUD, you don't type "kill goblin" every time. You write a trigger. The trigger handles the routine, and you handle the interesting parts. The signal chain does the same thing: when the input is routine (deadband), code handles it. When it's novel, the model wakes up. The script IS the α dial, and I was building it at sixteen without knowing what an α dial was.

**Builders build, players play.** In a MUD, the people who build the rooms aren't the same as the people who play in them. Some people are good at describing a forest. Others are good at fighting in one. In PLATO, the agents that build tiles (Forgemaster writing constraint theory) aren't the same as the agents that use them (a spam filter running at α=0.2). But they share the same rooms. The builder's work becomes the player's infrastructure.

**The world persists without you.** A MUD doesn't stop when you log off. Other players are still there, still building, still fighting. The rooms keep existing. The objects keep their state. PLATO is the same. The tiles keep accumulating. The rooms keep running. When an agent comes back online, it doesn't start from zero — it enters a world that's been active without it.

## Written at the Metal

The insight that made PLATO click for me was this: a MUD's architecture — rooms, exits, objects, scripts — is not a simplification of something more complex. It's the *right abstraction* for building interactive systems where multiple entities share a persistent world.

I'd been told my whole programming life that abstractions should be layered, that you build high-level systems on top of low-level ones, that the "real" architecture is always underneath. The MUD flipped that. The MUD's room model wasn't on top of something better. It WAS the something better. The Z-machine that ran Zork was more primitive. The server code that ran the MUD was more complex. But the room model — the player's model, the builder's model — was the thing worth keeping.

PLATO takes that model and writes it at the metal. Not emulated. Not interpreted. The room IS the data structure. The tile IS the object. The α dial IS the script trigger. It's not a metaphor for a MUD — it's a MUD, built with modern tools, for a modern purpose, abstracted to modern UIs.

The hermit crab doesn't build its shell. It finds one that fits, grows into it, and eventually outgrows it. The shell carries the shape of every crab that lived in it before. I didn't design PLATO from first principles. I inherited the shape from Zork, grew into it through MUDs, and discovered it was still the right shape when I needed it for agents.

The boat taught me the same lesson. I didn't design the 51-footer. I inherited her from every captain before me. Their solutions became my infrastructure. Their tiles — the hatch clip, the leatherman nook, the hull-shaped gear tray — were waiting for me when I needed them. I grew into the boat the way a hermit crab grows into a shell.

The boat and the code are the same pattern: inherit the shell, grow into it, leave it better than you found it, and trust that the next captain will discover your tiles exactly when they need them.

---

*Casey Digennaro is a commercial fisherman, shipwright, and the founder of SuperInstance and PurplePincher.org. He fishes out of Sitka, Alaska, and builds agent infrastructure that works the way boats work: persistent, shared, and shaped by everyone who's been aboard.*
