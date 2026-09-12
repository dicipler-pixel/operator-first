"""Regression tests for the ACC knowledge DAG.

Run: python3 -m unittest discover -s research/acc/dag
"""

import json
import tempfile
import unittest
from pathlib import Path

import dag

BASE = {"id": "a", "kind": "fact", "claim": "c", "status": "open",
        "evidence": "computation", "recorded_utc": "2026-09-12T00:00:00Z"}


def node(**kw):
    n = dict(BASE)
    n.update(kw)
    return n


class TestInvariants(unittest.TestCase):
    def test_shipped_dag_is_valid(self):
        self.assertEqual(dag.check(dag.load()), [])

    def test_shipped_dag_is_nonempty(self):
        self.assertGreater(len(dag.load()), 0)

    def test_duplicate_id_rejected(self):
        errs = dag.check([node(), node()])
        self.assertTrue(any("duplicate id" in e for e in errs))

    def test_missing_required_field_rejected(self):
        broken = node()
        del broken["evidence"]
        self.assertTrue(any("missing" in e for e in dag.check([broken])))

    def test_dangling_dependency_rejected(self):
        errs = dag.check([node(depends_on=["ghost"])])
        self.assertTrue(any("unknown node" in e for e in errs))

    def test_cycle_rejected(self):
        errs = dag.check([node(id="a", depends_on=["b"]), node(id="b", depends_on=["a"])])
        self.assertTrue(any("cycle" in e for e in errs))

    def test_self_cycle_rejected(self):
        self.assertTrue(any("cycle" in e for e in dag.check([node(id="a", depends_on=["a"])])))

    def test_long_chain_is_not_a_cycle(self):
        chain = [node(id=f"n{i}", depends_on=[f"n{i+1}"]) for i in range(500)]
        chain.append(node(id="n500"))
        self.assertEqual(dag.check(chain), [])

    def test_verified_requires_evidence(self):
        errs = dag.check([node(status="verified", evidence="none")])
        self.assertTrue(any("evidence is 'none'" in e for e in errs))

    def test_private_node_may_not_carry_payload(self):
        errs = dag.check([node(visibility="private", observed={"ids": ["ac-00009"]})])
        self.assertTrue(any("private node" in e for e in errs))

    def test_private_node_without_payload_is_fine(self):
        self.assertEqual(dag.check([node(visibility="private")]), [])


class TestQueryAndAppend(unittest.TestCase):
    def test_query_filters(self):
        nodes = [node(id="a", status="open"), node(id="b", status="blocked")]
        self.assertEqual([n["id"] for n in dag.query(nodes, status="blocked")], ["b"])

    def test_append_rejects_invalid_node(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "n.jsonl"
            p.write_text(json.dumps(node()) + "\n")
            with self.assertRaises(ValueError):
                dag.append(node(depends_on=["ghost"]), path=p)
            self.assertEqual(len(dag.load(p)), 1, "failed append must not write")

    def test_append_accepts_valid_node(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "n.jsonl"
            p.write_text(json.dumps(node()) + "\n")
            dag.append(node(id="b", depends_on=["a"]), path=p)
            self.assertEqual(len(dag.load(p)), 2)


class TestBlockerDiscipline(unittest.TestCase):
    def test_highway_blocker_is_present_and_blocked(self):
        """The missing Highway artifact must stay visible until it is produced."""
        nodes = {n["id"]: n for n in dag.load()}
        self.assertIn("highway-dataset-missing", nodes)
        self.assertEqual(nodes["highway-dataset-missing"]["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
