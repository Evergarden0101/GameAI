"""
Generative AI Agent: an LLM-driven NPC  ·  生成式 AI 智能体（LLM 驱动的 NPC）
==========================================================================

Instead of a fixed dialogue tree, a *generative* NPC is powered by a Large
Language Model. It has:

  * a PERSONA (system prompt) that defines who it is,
  * MEMORY (the running conversation), and
  * TOOLS (function calling) so its words turn into real game actions -
    giving a quest, checking the shop inventory, changing how much it likes you.

This is the pattern behind LLM-NPC tech like NVIDIA ACE and Inworld, and the
research "Generative Agents" (Stanford's Smallville). The player can say
anything and the NPC responds in character and acts on the world.

This sample uses Anthropic's Claude (model `claude-opus-5`). If the `anthropic`
package or API credentials are missing, it automatically falls back to a small
OFFLINE MOCK that follows the exact same code path, so the file always runs and
demonstrates the architecture.

    pip install anthropic          # for the real model
    export ANTHROPIC_API_KEY=...   # or run `ant auth login`
    python generative_npc.py
"""

import json

MODEL = "claude-opus-5"

# --------------------------------------------------------------------------- #
# 1. PERSONA — the system prompt defines the character.
# --------------------------------------------------------------------------- #
SYSTEM = """You are Bram, a gruff but fair blacksmith in the village of Oakhollow.
Speak in character: short, earthy sentences, a little weary, warm underneath.
You run the forge and the shop. You can hand out odd jobs, check your wares,
and you keep track of how much you trust the traveller.
Use your tools to actually do these things rather than only talking about them.
Never break character or mention that you are an AI."""

# --------------------------------------------------------------------------- #
# 2. TOOLS — function calling maps the NPC's intent to game actions.
# --------------------------------------------------------------------------- #
TOOLS = [
    {
        "name": "give_quest",
        "description": "Offer the traveller a quest / odd job.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "reward_gold": {"type": "integer"},
            },
            "required": ["title", "reward_gold"],
        },
    },
    {
        "name": "check_inventory",
        "description": "Look up what the blacksmith currently has for sale.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "adjust_disposition",
        "description": "Change how much Bram trusts the traveller (-100..100).",
        "input_schema": {
            "type": "object",
            "properties": {"delta": {"type": "integer"}},
            "required": ["delta"],
        },
    },
]

# --------------------------------------------------------------------------- #
# 3. GAME STATE the tools read and write.
# --------------------------------------------------------------------------- #
GAME_STATE = {
    "disposition": 10,
    "shop": [
        {"item": "iron sword", "price": 40},
        {"item": "steel shield", "price": 65},
        {"item": "horseshoes (x4)", "price": 8},
    ],
    "active_quests": [],
}


def execute_tool(name, tool_input):
    """Run a tool call against the game world and return a result string."""
    if name == "give_quest":
        GAME_STATE["active_quests"].append(tool_input["title"])
        return (f"Quest accepted: '{tool_input['title']}' "
                f"for {tool_input['reward_gold']} gold.")
    if name == "check_inventory":
        return json.dumps(GAME_STATE["shop"])
    if name == "adjust_disposition":
        GAME_STATE["disposition"] = max(-100, min(
            100, GAME_STATE["disposition"] + int(tool_input["delta"])))
        return f"Disposition is now {GAME_STATE['disposition']}."
    return f"Unknown tool: {name}"


# --------------------------------------------------------------------------- #
# 4. The conversation loop — identical for the real API and the mock.
# --------------------------------------------------------------------------- #
def talk(client, history, user_text):
    """Send a player line, run any tool calls, return the NPC's spoken reply."""
    history.append({"role": "user", "content": user_text})

    while True:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM,
            tools=TOOLS,
            messages=history,
        )
        # Always append the full assistant content (may contain tool_use blocks).
        history.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason == "tool_use":
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    print(f"      [tool] {block.name}({json.dumps(block.input)}) "
                          f"-> {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            history.append({"role": "user", "content": tool_results})
            continue  # let the model see the results and finish its turn

        return "".join(b.text for b in resp.content if b.type == "text")


# --------------------------------------------------------------------------- #
# 5a. Real Anthropic client (used when available).
# --------------------------------------------------------------------------- #
def make_real_client():
    import anthropic
    client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY / profile
    # A cheap probe so we can fall back cleanly if credentials are missing.
    client.models.retrieve(MODEL)
    return client


# --------------------------------------------------------------------------- #
# 5b. Offline mock — same interface as the real client, deterministic replies.
# --------------------------------------------------------------------------- #
class _Block:
    def __init__(self, type, **kw):
        self.type = type
        for k, v in kw.items():
            setattr(self, k, v)


class _Resp:
    def __init__(self, content, stop_reason):
        self.content = content
        self.stop_reason = stop_reason


class _MockMessages:
    _counter = 0

    def create(self, model, max_tokens, system, tools, messages):
        last = messages[-1]
        # If we're being handed tool results, wrap up the turn with flavour text.
        if last["role"] == "user" and isinstance(last["content"], list):
            kind = last["content"][0].get("type")
            if kind == "tool_result":
                res = last["content"][0]["content"]
                return _Resp([_Block("text",
                    text=f"*wipes his hands* There. {res} Anything else, traveller?")],
                    "end_turn")

        text = last["content"] if isinstance(last["content"], str) else ""
        low = text.lower()

        if any(w in low for w in ("job", "quest", "work", "help you")):
            _MockMessages._counter += 1
            return _Resp([
                _Block("text", text="Aye, there's always work. "
                                    "Wolves at the north pasture, if you're able."),
                _Block("tool_use", name="give_quest", id=f"t{self._counter}",
                       input={"title": "Cull the pasture wolves", "reward_gold": 30}),
            ], "tool_use")

        if any(w in low for w in ("buy", "sell", "shop", "wares", "have", "inventory")):
            _MockMessages._counter += 1
            return _Resp([
                _Block("text", text="Take a look at what's on the rack."),
                _Block("tool_use", name="check_inventory",
                       id=f"t{self._counter}", input={}),
            ], "tool_use")

        if any(w in low for w in ("thank", "friend", "cheers", "appreciate")):
            _MockMessages._counter += 1
            return _Resp([
                _Block("text", text="*grunts, almost a smile* Don't mention it."),
                _Block("tool_use", name="adjust_disposition",
                       id=f"t{self._counter}", input={"delta": 8}),
            ], "tool_use")

        return _Resp([_Block("text",
            text="Hmph. Speak plainly — I've iron in the fire.")], "end_turn")


class MockClient:
    def __init__(self):
        self.messages = _MockMessages()


# --------------------------------------------------------------------------- #
# 6. Demo conversation
# --------------------------------------------------------------------------- #
def main():
    try:
        client = make_real_client()
        mode = f"LIVE  (Anthropic {MODEL})"
    except Exception as e:                    # ImportError, auth, network...
        client = MockClient()
        mode = f"OFFLINE MOCK  (reason: {type(e).__name__})"

    print("Generative NPC demo — talking to Bram the blacksmith")
    print(f"mode: {mode}")
    print("=" * 60)

    history = []
    player_lines = [
        "Evening. Got any work for a traveller?",
        "What have you got for sale?",
        "Thanks, Bram — you're a good sort.",
    ]
    for line in player_lines:
        print(f"\nPLAYER: {line}")
        reply = talk(client, history, line)
        print(f"BRAM  : {reply}")

    print("\n" + "-" * 60)
    print(f"Final game state: disposition={GAME_STATE['disposition']}, "
          f"active_quests={GAME_STATE['active_quests']}")
    print("The NPC improvised in-character dialogue AND drove real game state "
          "through tool calls — the core of a generative-agent NPC.")


if __name__ == "__main__":
    main()
