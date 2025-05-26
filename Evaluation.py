from spellchecker import SpellChecker
import language_tool_python
from bert_score import score


def evaluate_answer(total_marks, model_answer, student_answer):
    spell = SpellChecker()

    spell_errors = spell.unknown(student_answer.split())
    spell_check_score = len(spell_errors) * 0.1

    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(student_answer)
    grammar_check_score = len(matches) * 0.1

    _, _, F1 = score([student_answer], [model_answer], lang="en", model_type="bert-base-uncased")
    similarity_score = F1.mean().item()

    if similarity_score == 1:
        final_score = total_marks
    elif similarity_score < 0.55:
        final_score = 0
    else:
        context_check_score = (1 - similarity_score) * 0.8
        total_deductions = spell_check_score + grammar_check_score + context_check_score
        final_score = total_marks - total_deductions

    final_score = max(final_score, 0)

    return final_score,grammar_check_score,spell_check_score


