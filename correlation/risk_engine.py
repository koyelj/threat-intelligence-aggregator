def calculate_severity(feed_count):

    if feed_count >= 3:
        return "HIGH"

    elif feed_count == 2:
        return "MEDIUM"

    else:
        return "LOW"


def calculate_risk_score(
    feed_count,
    occurrence_count
):

    score = 0

    # Feed-based score

    if feed_count >= 3:
        score += 60

    elif feed_count == 2:
        score += 40

    else:
        score += 20

    # Occurrence-based score

    if occurrence_count >= 5:
        score += 40

    elif occurrence_count >= 3:
        score += 25

    elif occurrence_count >= 2:
        score += 15

    else:
        score += 5

    return min(score, 100)


if __name__ == "__main__":

    print("Risk Engine Test")
    print("----------------")

    print(
        "3 feeds:",
        calculate_severity(3)
    )

    print(
        "2 feeds:",
        calculate_severity(2)
    )

    print(
        "1 feed:",
        calculate_severity(1)
    )

    print(
        "Risk score:",
        calculate_risk_score(3, 5)
    )