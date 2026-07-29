"""Whitelist-only expression interpreter for deterministic trading rules."""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable, Mapping
from typing import Any


class ExpressionError(ValueError):
    """Raised when a rule expression is invalid, unsafe, or cannot be evaluated."""


_BINARY_OPERATORS: dict[type[ast.operator], Callable[[Any, Any], Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[Any], Any]] = {
    ast.Not: operator.not_,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_COMPARE_OPERATORS: dict[type[ast.cmpop], Callable[[Any, Any], bool]] = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Is: operator.is_,
    ast.IsNot: operator.is_not,
}


class SafeExpressionEvaluator:
    """Parse and evaluate a constrained expression without dynamic Python execution."""

    def __init__(self, functions: Mapping[str, Callable[..., Any]] | None = None) -> None:
        self._functions = dict(functions or {})

    def evaluate(self, expression: str, variables: Mapping[str, Any]) -> Any:
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ExpressionError(f"Invalid expression syntax: {exc.msg}") from exc
        return self._visit(tree.body, variables)

    def _visit(self, node: ast.AST, variables: Mapping[str, Any]) -> Any:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (str, int, float, bool, type(None))):
                return node.value
            raise ExpressionError(f"Unsupported constant type: {type(node.value).__name__}")

        if isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id]
            raise ExpressionError(f"Unknown name: {node.id}")

        if isinstance(node, ast.BoolOp):
            if isinstance(node.op, ast.And):
                return all(bool(self._visit(value, variables)) for value in node.values)
            if isinstance(node.op, ast.Or):
                return any(bool(self._visit(value, variables)) for value in node.values)
            raise ExpressionError(f"Unsupported boolean operator: {type(node.op).__name__}")

        if isinstance(node, ast.BinOp):
            function = _BINARY_OPERATORS.get(type(node.op))
            if function is None:
                raise ExpressionError(f"Unsupported binary operator: {type(node.op).__name__}")
            return function(self._visit(node.left, variables), self._visit(node.right, variables))

        if isinstance(node, ast.UnaryOp):
            function = _UNARY_OPERATORS.get(type(node.op))
            if function is None:
                raise ExpressionError(f"Unsupported unary operator: {type(node.op).__name__}")
            return function(self._visit(node.operand, variables))

        if isinstance(node, ast.Compare):
            left = self._visit(node.left, variables)
            for op_node, comparator_node in zip(node.ops, node.comparators, strict=True):
                function = _COMPARE_OPERATORS.get(type(op_node))
                if function is None:
                    raise ExpressionError(f"Unsupported comparison operator: {type(op_node).__name__}")
                right = self._visit(comparator_node, variables)
                if not function(left, right):
                    return False
                left = right
            return True

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ExpressionError("Only direct calls to registered functions are allowed")
            if node.func.id not in self._functions:
                raise ExpressionError(f"Unknown or unregistered function: {node.func.id}")
            if node.keywords:
                raise ExpressionError("Keyword arguments are not supported")
            arguments = [self._visit(argument, variables) for argument in node.args]
            try:
                return self._functions[node.func.id](*arguments)
            except Exception as exc:
                raise ExpressionError(f"Function {node.func.id} failed: {exc}") from exc

        raise ExpressionError(f"Unsupported syntax: {type(node).__name__}")
