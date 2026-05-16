import unittest
from agents.risk_agent import score_risk
from agents.value_agent import score_value
from agents.decision_synthesizer import synthesize


class TestRiskAgent(unittest.TestCase):

    def test_low_risk_returns_low_average(self):
        scores = score_risk("sandbox test automation workflow")
        self.assertLessEqual(scores["average"], 3.0)

    def test_high_risk_returns_high_average(self):
        scores = score_risk("production outage unsafe non-compliant breach unreliable")
        self.assertGreaterEqual(scores["average"], 4.0)

    def test_all_dimension_scores_in_range(self):
        scores = score_risk("deploy AI to production with sensitive GDPR data prototype")
        for k, v in scores.items():
            if k != "average":
                self.assertGreaterEqual(v, 1)
                self.assertLessEqual(v, 5)

    def test_average_key_present(self):
        scores = score_risk("some workflow")
        self.assertIn("average", scores)

    def test_average_is_mean_of_dimensions(self):
        scores = score_risk("sandbox test automation")
        dims = [v for k, v in scores.items() if k != "average"]
        expected = round(sum(dims) / len(dims), 2)
        self.assertEqual(scores["average"], expected)


class TestValueAgent(unittest.TestCase):

    def test_high_value_returns_high_average(self):
        scores = score_value("automate customer revenue growth company-wide strategic")
        self.assertGreaterEqual(scores["average"], 3.5)

    def test_low_value_returns_low_average(self):
        scores = score_value("minor change with no clear benefit")
        self.assertLessEqual(scores["average"], 2.0)

    def test_all_dimension_scores_in_range(self):
        scores = score_value("streamline budget process for the team pipeline")
        for k, v in scores.items():
            if k != "average":
                self.assertGreaterEqual(v, 1)
                self.assertLessEqual(v, 5)

    def test_average_key_present(self):
        scores = score_value("some workflow")
        self.assertIn("average", scores)

    def test_average_is_mean_of_dimensions(self):
        scores = score_value("automate team budget workflow")
        dims = [v for k, v in scores.items() if k != "average"]
        expected = round(sum(dims) / len(dims), 2)
        self.assertEqual(scores["average"], expected)


class TestSynthesizer(unittest.TestCase):

    def _risk(self, avg):
        return {"operational": 1, "safety": 1, "compliance": 1, "reliability": 1, "average": avg}

    def _value(self, avg):
        return {"business_value": 1, "efficiency": 1, "cost_reduction": 1, "deployment_upside": 1, "average": avg}

    def test_approve_verdict(self):
        result = synthesize(self._risk(1.0), self._value(4.0))
        self.assertEqual(result["verdict"], "APPROVE")

    def test_reject_verdict(self):
        result = synthesize(self._risk(5.0), self._value(1.0))
        self.assertEqual(result["verdict"], "REJECT")

    def test_revise_verdict_mid_scores(self):
        result = synthesize(self._risk(3.0), self._value(3.0))
        self.assertEqual(result["verdict"], "REVISE")

    def test_revise_when_risk_low_but_value_too_low(self):
        result = synthesize(self._risk(2.0), self._value(2.0))
        self.assertEqual(result["verdict"], "REVISE")

    def test_reject_boundary_at_4(self):
        result = synthesize(self._risk(4.0), self._value(5.0))
        self.assertEqual(result["verdict"], "REJECT")

    def test_approve_boundary(self):
        result = synthesize(self._risk(2.5), self._value(3.5))
        self.assertEqual(result["verdict"], "APPROVE")

    def test_result_has_required_keys(self):
        result = synthesize(self._risk(2.0), self._value(4.0))
        for key in ["verdict", "confidence", "rationale", "avg_risk", "avg_value"]:
            self.assertIn(key, result)

    def test_confidence_is_numeric(self):
        result = synthesize(self._risk(1.0), self._value(5.0))
        self.assertIsInstance(result["confidence"], float)

    def test_confidence_in_valid_range(self):
        for avg in [1.0, 2.5, 3.0, 4.0, 5.0]:
            result = synthesize(self._risk(avg), self._value(avg))
            self.assertGreaterEqual(result["confidence"], 0)
            self.assertLessEqual(result["confidence"], 100)


if __name__ == "__main__":
    unittest.main()
