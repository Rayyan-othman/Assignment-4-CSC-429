import unittest
from engine import ForwardChainingEngine, Rule
from kb_loader import load_rules
from pathlib import Path

RULES = load_rules(str(Path(__file__).resolve().parents[1] / "kb" / "laptop_rules.json"))


class ExpertSystemTests(unittest.TestCase):
    def check_case(self, facts, expected):
        engine = ForwardChainingEngine(RULES)
        engine.assert_facts(facts)
        engine.run()
        self.assertIn(expected, engine.facts)
        return engine

    def test_premium_ultrabook(self):
        self.check_case(["budget_high", "portable", "long_battery"], "recommend:premium_ultrabook")

    def test_budget_ultrabook(self):
        self.check_case(["budget_low", "office_only", "portable"], "recommend:budget_ultrabook")

    def test_midrange_gaming(self):
        self.check_case(["gaming", "budget_medium"], "recommend:midrange_gaming_laptop")

    def test_high_end_gaming(self):
        self.check_case(["gaming", "budget_high"], "recommend:high_end_gaming_laptop")

    def test_creative_ram(self):
        self.check_case(["creative_work", "portable"], "spec:ram_16_plus")

    def test_creative_display(self):
        self.check_case(["creative_work", "large_screen"], "spec:display_15_plus_color_accurate")

    def test_travel_battery(self):
        self.check_case(["travel_often", "long_battery"], "spec:battery_60wh_plus")

    def test_macos(self):
        self.check_case(["pref_os_macos"], "spec:macos_required")

    def test_ai_accel(self):
        self.check_case(["needs_ai_accel"], "spec:gpu_with_tensor_cores")

    def test_linux(self):
        self.check_case(["pref_os_linux", "office_only"], "spec:linux_friendly_hw")

    def test_no_match(self):
        engine = self.check_case(["budget_low"], "budget_low")
        self.assertEqual(engine.conclusions()["recommendations"], [])
        self.assertEqual(engine.trace, [])

    def test_priority_and_chain(self):
        rules = [Rule(["start"], "step", 1, "First"), Rule(["step"], "recommend:done", 3, "Second")]
        engine = ForwardChainingEngine(rules)
        engine.assert_facts(["start"])
        engine.run()
        self.assertEqual(engine.conclusions()["recommendations"], ["done"])
        self.assertEqual(len(engine.trace), 2)
        engine.run()
        self.assertEqual(len(engine.trace), 2)

    def test_all_antecedents_required(self):
        engine = ForwardChainingEngine([Rule(["a", "b"], "recommend:yes")])
        engine.assert_facts(["a"])
        engine.run()
        self.assertFalse(engine.trace)


if __name__ == "__main__":
    unittest.main()
