__author__ = 'marc'

def remove_duplicates(articles, field):
    results = []

    for article in articles:
        if not results:
            results.append(article)
        if article[field] not in [result[field] for result in results]:
            results.append(article)

    return results
