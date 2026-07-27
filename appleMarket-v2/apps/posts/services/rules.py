import re

def parse_nutrition(lines):
    full_text = ' '.join(lines)

    return {
        'calorie': _find_calorie(full_text),
        'carbohydrate': _find_gram_value(full_text, '탄수화물'),
        'protein': _find_gram_value(full_text, '단백질'),
        'fat': _find_gram_value(full_text, '지방'),
    }

def _find_calorie(text):
    candidates = []
    for match in re.finditer(r'([\d,]+)\s*[kK]cal', text):
        start, end = match.span()
        context = text[max(0, start - 15):end + 15]
        if '기준' in context or '비율' in context:
            continue
        candidates.append(float(match.group(1).replace(',', '')))

    if candidates:
        return min(candidates)

    for kw in ['열량', '칼로리']:
        match = re.search(rf'{kw}\D{{0,10}}?([\d,]+)', text)
        if match:
            return float(match.group(1).replace(',', ''))

    return None

def _find_gram_value(text, keyword):
    match = re.search(rf'{keyword}\D{{0,10}}?([\d.]+)\s*(mg|g)', text)
    if not match:
        return None
    value = float(match.group(1))
    if match.group(2) == 'mg':
        value = value / 1000
    return round(value, 2)