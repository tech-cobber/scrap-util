from collections import Counter


def keywords(data: str) -> str:
    '''Find Top-3 keywords on the page'''
    # Super dummy
    counter = Counter(data)
    commons = dict(counter.most_common(3))
    return '\n' + '\n'.join(
            [f'\t{key}: {value}' for key, value in commons.items()])
