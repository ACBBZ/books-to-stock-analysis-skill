"""Trading-book knowledge compiler and deterministic skill runtime."""

from books_to_stock_analysis_skill.domain.models import TradingSkill
from books_to_stock_analysis_skill.runtime.evaluator import EvaluationResult, SkillEvaluator

__all__ = ["EvaluationResult", "SkillEvaluator", "TradingSkill"]
__version__ = "0.1.0"
