# utils/score_utils.py
from models.score_model import get_scores_for_performance
from models.user_model import get_weightage

def calculate_cumulative_scores(performance_id):
    cumulative_scores = {f"Category_{i}": 0 for i in range(1, 6)}
    judge_scores = get_scores_for_performance(performance_id)
    for item in judge_scores:
        scores = item['category_scores']
        weight = get_weightage(item['user_id'])
        for category, score in scores.items():
            print(f'{category=},{score=},{weight=}')
            cumulative_scores[category] += score * weight

    print(cumulative_scores)
    return cumulative_scores
