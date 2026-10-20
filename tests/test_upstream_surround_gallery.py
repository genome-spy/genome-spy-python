"""Keep Python authoring equivalent to the published surround examples."""

import ast
from functools import cache
import json
from pathlib import Path
import runpy
import shutil
import subprocess
from typing import Any

import pytest

pytestmark = pytest.mark.docs
ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = [
    ("pisa_interaction_matrix", "bpreveal-pisa-matrix"),
    ("upset_mutations", "upsetr-mutations"),
    ("clustered_heatmap", "clustered-heatmap"),
]


@cache
def _specs(example: str, upstream: str) -> tuple[dict, dict]:
    chart = runpy.run_path(str(ROOT / "docs" / "examples" / f"{example}.py"))["chart"]
    reference = json.loads(
        (
            ROOT / "tests" / "fixtures" / "upstream_examples" / f"{upstream}.json"
        ).read_text()
    )
    return chart.to_dict(), reference


def _structure(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "<expression>" if key == "expr" else _structure(child)
            for key, child in value.items()
            if key not in {"$schema", "description"}
        }
    if isinstance(value, list):
        return [_structure(child) for child in value]
    return value


def _expressions(value: Any, path: str = "") -> dict[str, str]:
    if isinstance(value, dict):
        return {
            key: expression
            for name, child in value.items()
            for key, expression in (
                {f"{path}/expr": child}
                if name == "expr"
                else _expressions(child, f"{path}/{name}")
            ).items()
        }
    if isinstance(value, list):
        return {
            key: expression
            for i, child in enumerate(value)
            for key, expression in _expressions(child, f"{path}/{i}").items()
        }
    return {}


@pytest.mark.parametrize(("example", "upstream"), EXAMPLES)
def test_python_reproduces_upstream_surround_structure(
    example: str, upstream: str
) -> None:
    spec, reference = _specs(example, upstream)
    assert _structure(spec) == _structure(reference)


@pytest.mark.parametrize(("example", "upstream"), EXAMPLES)
def test_python_expressions_match_upstream_results(example: str, upstream: str) -> None:
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node.js is required to compare JavaScript expression results")
    spec, reference = _specs(example, upstream)
    actual = _expressions(spec)
    expected = _expressions(reference)
    assert actual.keys() == expected.keys()
    pairs = [
        [path, expression, expected[path]]
        for path, expression in actual.items()
        if expression != expected[path]
    ]
    result = subprocess.run(
        [node, "-e", _COMPARE_EXPRESSIONS],
        input=json.dumps(pairs),
        text=True,
        capture_output=True,
        timeout=20,
        check=False,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("example", [example for example, _ in EXAMPLES])
def test_examples_author_expressions_with_python_objects(example: str) -> None:
    tree = ast.parse((ROOT / "docs" / "examples" / f"{example}.py").read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "expr":
            assert not isinstance(node.value, ast.Constant), f"{example}:{node.lineno}"
        if not isinstance(node, ast.Call) or not node.args:
            continue
        name = ast.unparse(node.func)
        argument = node.args[0]
        if not isinstance(argument, ast.Constant) or not isinstance(
            argument.value, str
        ):
            continue
        if name.endswith(".transform_filter"):
            pytest.fail(f"{example}:{node.lineno}: use a Python filter expression")
        if name in {"gs.Expression", "gs.expr"}:
            assert argument.value.isidentifier(), f"{example}:{node.lineno}"


_COMPARE_EXPRESSIONS = r"""
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const pairs = JSON.parse(fs.readFileSync(0, 'utf8'));
for (let i = 0; i < 96; i++) {
    const domain = channel => {
        const start = channel === 'x' ? 15646649 : 15646499;
        const values = [start, start + (i % 2 ? 1 : 601)];
        return i % 3 ? values : values.reverse();
    };
    const context = {
        width: [30, 600, 900][i % 3], height: [16, 300, 600][i % 3],
        labelVisibilityXSpan: 40, labelVisibilityYSpan: 30,
        labelXBinSize: 10, labelYBinSize: 15, showCellLabels: Boolean(i & 2),
        labelXStart: 15646650, labelXEnd: 15646670,
        labelYStart: 15646500, labelYEnd: 15646530,
        setCursor: {values: {y: [null, 0, 1.2, 4][i % 4]}},
        datum: {
            track: ['importance', 'prediction', 'other'][i % 3],
            name: ['m1bp', 'gaga', 'zelda', 'unknown'][i % 4],
            position: 15646649 + i % 2,
            input: [15646649, 15646650, 15646660, 15646669, 15646670][i % 5],
            output: [15646499, 15646500, 15646515, 15646529, 15646530][(i >> 1) % 5],
            member: Boolean(i & 1), setIndex: i % 5, profileNumber: i % 3,
            profileDegree: i % 3 - 1, profileContainsHoveredSet: (i >> 1) % 2,
            profileSize: 37, value: i - 20, sdLog2Tpm: 2.5, meanLog2Tpm: 5,
        },
        domain, span: a => a[a.length - 1] - a[0],
        bandstep: channel => channel === 'x' ? 1 / 72 : 1 / 60,
        isValid: value => value != null && !Number.isNaN(value),
        if_: (test, thenValue, elseValue) => test ? thenValue : elseValue,
        abs: Math.abs, min: Math.min, max: Math.max,
        floor: Math.floor, ceil: Math.ceil, round: Math.round,
    };
    for (const [path, actual, expected] of pairs) {
        const evaluate = source => vm.compileFunction(
            `return (${source.replace(/\bif\(/g, 'if_(')});`, Object.keys(context)
        )(...Object.values(context));
        assert.deepEqual(evaluate(actual), evaluate(expected), `${path}, case ${i}`);
    }
}
"""
