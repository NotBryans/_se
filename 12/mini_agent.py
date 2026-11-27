import datetime
import json
import os


# ============================================================
# 1. Tools: Giving the LLM real-world capabilities
# ============================================================
def tool_get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def tool_calculate(expr):
    allowed = set("0123456789+-*/(). ")
    if not all(ch in allowed for ch in expr):
        return "Error: invalid characters in expression"
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"


def tool_list_files(path="."):
    try:
        return ", ".join(sorted(os.listdir(path)))
    except Exception as e:
        return f"Error: {e}"


TOOLS = {
    "get_time": tool_get_time,
    "calculate": tool_calculate,
    "list_files": tool_list_files,
}


# ============================================================
# 2. Simulated LLM API (Demonstrates stateless messages -> JSON)
#    Replace this function with OpenAI / Gemini API calls in prod.
# ============================================================
def call_llm_api(messages):
    last_msg = messages[-1]["content"]

    # Step 1: User asks a multi-step question
    if messages[-1]["role"] == "user":
        return json.dumps({
            "thought": "I need to calculate 128 * 32 first using the calculate tool.",
            "action": "calculate",
            "args": {"expr": "128 * 32"}
        })

    # Step 2: After receiving calculation observation, check current time
    if "4096" in last_msg and not any("TIME_RESULT:" in m["content"] for m in messages):
        return json.dumps({
            "thought": "Now I know 128 * 32 = 4096. Next I should get the current system time.",
            "action": "get_time",
            "args": {}
        })

    # Step 3: All observations gathered -> produce Final Answer
    return json.dumps({
        "thought": "I have both the calculation result and the current time. Ready to answer.",
        "final_answer": f"128 * 32 = 4096. Latest observation: {last_msg}"
    })


# ============================================================
# 3. The ReAct Agent Loop (Thought -> Action -> Observation)
# ============================================================
def run_agent(user_query, max_steps=5):
    messages = [
        {"role": "system", "content": "You are a helpful ReAct agent with tools: get_time, calculate, list_files."},
        {"role": "user", "content": user_query},
    ]
    print(f"User: {user_query}\n" + "-" * 50)

    for step in range(1, max_steps + 1):
        raw_reply = call_llm_api(messages)
        messages.append({"role": "assistant", "content": raw_reply})
        parsed = json.loads(raw_reply)

        print(f"[Step {step}] Thought: {parsed.get('thought')}")

        if "final_answer" in parsed:
            print(f"\nFinal Answer: {parsed['final_answer']}")
            return parsed["final_answer"]

        action = parsed.get("action")
        args = parsed.get("args", {})
        print(f"[Step {step}] Action:  {action}({args})")

        if action in TOOLS:
            result = TOOLS[action](**args)
            obs = f"TIME_RESULT: {result}" if action == "get_time" else f"RESULT: {result}"
        else:
            obs = f"Error: Unknown tool '{action}'"

        print(f"[Step {step}] Observ.: {obs}\n")
        messages.append({"role": "tool", "content": obs})

    print("Reached max_steps without a final answer.")
    return None


if __name__ == "__main__":
    run_agent("Calculate 128 * 32 and tell me the current time.")
