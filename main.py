from pathlib import Path
from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = Path(__file__).resolve().parent / "kb" / "laptop_rules.json"


def ask_yes_no(question):
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def collect_initial_facts():
    facts = []
    while True:
        budget = input("What is your budget? (low/medium/high): ").strip().lower()
        if budget in ("low", "medium", "high"):
            facts.append("budget_" + budget)
            break
        print("Please enter low, medium, or high.")

    questions = [
        ("Is portability important?", "portable"),
        ("Do you need long battery life?", "long_battery"),
        ("Will you use the laptop for gaming?", "gaming"),
        ("Will you use it for creative work?", "creative_work"),
        ("Will you use it mainly for office tasks?", "office_only"),
        ("Do you need a large screen?", "large_screen"),
        ("Do you travel often?", "travel_often"),
        ("Do you need AI acceleration?", "needs_ai_accel"),
    ]
    for question, fact in questions:
        if ask_yes_no(question):
            facts.append(fact)

    while True:
        os_choice = input("Preferred OS? (windows/macos/linux/none): ").strip().lower()
        if os_choice in ("windows", "macos", "linux", "none"):
            if os_choice != "none":
                facts.append("pref_os_" + os_choice)
            break
        print("Please enter windows, macos, linux, or none.")
    return facts


def main():
    print("Laptop Advisor Expert System")
    rules = load_rules(str(KB_PATH))
    engine = ForwardChainingEngine(rules)
    engine.assert_facts(collect_initial_facts())
    engine.run()
    results = engine.conclusions()

    print("\nRecommendations:")
    for item in results["recommendations"]:
        print(" -", item)
    if not results["recommendations"]:
        print(" - No recommendation matched the given facts.")

    print("\nSuggested specifications:")
    for item in results["specs"]:
        print(" -", item)
    if not results["specs"]:
        print(" - None inferred.")

    print("\nRules fired (explanations):")
    for step in engine.trace:
        print(" - {}: {} -> {}".format(step["rule"], " AND ".join(step["antecedents"]), step["consequent"]))
    if not engine.trace:
        print(" - No rules fired.")


if __name__ == "__main__":
    main()
