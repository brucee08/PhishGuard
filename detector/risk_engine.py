
# =========================================================
# PHISHGUARD - RISK ENGINE
# =========================================================


def calculate_risk(features, prediction):
    """
    Calculate a risk score from 0 to 100.

    The score combines:
    1. URL characteristics
    2. Machine learning prediction
    """

    score = 0


    # =====================================================
    # 1. URL LENGTH
    # =====================================================

    url_length = features.get(
        "url_length",
        0
    )

    if url_length > 100:

        score += 20

    elif url_length > 75:

        score += 15

    elif url_length > 50:

        score += 10

    elif url_length > 30:

        score += 5


    # =====================================================
    # 2. HTTPS
    # =====================================================

    # HTTPS alone does not guarantee that a website
    # is legitimate.

    has_https = features.get(
        "has_https",
        0
    )

    if has_https == 0:

        score += 10


    # =====================================================
    # 3. NUMBER OF DOTS
    # =====================================================

    num_dots = features.get(
        "num_dots",
        0
    )

    if num_dots >= 6:

        score += 15

    elif num_dots >= 4:

        score += 10

    elif num_dots >= 3:

        score += 5


    # =====================================================
    # 4. HYPHENS
    # =====================================================

    num_hyphens = features.get(
        "num_hyphens",
        0
    )

    if num_hyphens >= 5:

        score += 15

    elif num_hyphens >= 3:

        score += 10

    elif num_hyphens >= 1:

        score += 5


    # =====================================================
    # 5. DIGITS
    # =====================================================

    num_digits = features.get(
        "num_digits",
        0
    )

    if num_digits >= 10:

        score += 15

    elif num_digits >= 6:

        score += 10

    elif num_digits >= 3:

        score += 5


    # =====================================================
    # 6. SPECIAL CHARACTERS
    # =====================================================

    num_special_chars = features.get(
        "num_special_chars",
        0
    )

    if num_special_chars >= 15:

        score += 15

    elif num_special_chars >= 10:

        score += 10

    elif num_special_chars >= 5:

        score += 5


    # =====================================================
    # 7. SUBDOMAINS
    # =====================================================

    num_subdomains = features.get(
        "num_subdomains",
        0
    )

    if num_subdomains >= 5:

        score += 15

    elif num_subdomains >= 3:

        score += 10

    elif num_subdomains >= 2:

        score += 5


    # =====================================================
    # 8. MACHINE LEARNING PREDICTION
    # =====================================================

    if str(prediction).lower() == "phishing":

        score += 40


    # =====================================================
    # FINAL SCORE
    # =====================================================

    # Make sure the score stays between 0 and 100.

    score = max(
        0,
        min(score, 100)
    )


    return score



# =========================================================
# GENERATE EXPLANATION
# =========================================================

def generate_explanation(
    features,
    prediction,
    score
):
    """
    Generate a human-readable explanation
    for the calculated risk score.
    """

    reasons = []


    # =====================================================
    # 1. URL LENGTH
    # =====================================================

    url_length = features.get(
        "url_length",
        0
    )

    if url_length > 100:

        reasons.append(
            "The URL is extremely long, "
            "which can be a suspicious characteristic."
        )

    elif url_length > 75:

        reasons.append(
            "The URL is unusually long."
        )

    elif url_length > 50:

        reasons.append(
            "The URL is relatively long."
        )


    # =====================================================
    # 2. HTTPS
    # =====================================================

    has_https = features.get(
        "has_https",
        0
    )

    if has_https == 0:

        reasons.append(
            "The URL does not use HTTPS."
        )

    else:

        reasons.append(
            "The URL uses HTTPS, but HTTPS alone "
            "does not guarantee that a website is legitimate."
        )


    # =====================================================
    # 3. NUMBER OF DOTS
    # =====================================================

    num_dots = features.get(
        "num_dots",
        0
    )

    if num_dots >= 6:

        reasons.append(
            "The URL contains a very high number of dots."
        )

    elif num_dots >= 4:

        reasons.append(
            "The URL contains several dots."
        )


    # =====================================================
    # 4. HYPHENS
    # =====================================================

    num_hyphens = features.get(
        "num_hyphens",
        0
    )

    if num_hyphens >= 5:

        reasons.append(
            "The URL contains many hyphens."
        )

    elif num_hyphens >= 3:

        reasons.append(
            "The URL contains several hyphens."
        )


    # =====================================================
    # 5. DIGITS
    # =====================================================

    num_digits = features.get(
        "num_digits",
        0
    )

    if num_digits >= 10:

        reasons.append(
            "The URL contains a large number of digits."
        )

    elif num_digits >= 6:

        reasons.append(
            "The URL contains many digits."
        )


    # =====================================================
    # 6. SPECIAL CHARACTERS
    # =====================================================

    num_special_chars = features.get(
        "num_special_chars",
        0
    )

    if num_special_chars >= 15:

        reasons.append(
            "The URL contains a high number "
            "of special characters."
        )

    elif num_special_chars >= 10:

        reasons.append(
            "The URL contains several special characters."
        )


    # =====================================================
    # 7. SUBDOMAINS
    # =====================================================

    num_subdomains = features.get(
        "num_subdomains",
        0
    )

    if num_subdomains >= 5:

        reasons.append(
            "The URL contains a large number of subdomains."
        )

    elif num_subdomains >= 3:

        reasons.append(
            "The URL contains multiple subdomains."
        )


    # =====================================================
    # 8. MACHINE LEARNING RESULT
    # =====================================================

    if str(prediction).lower() == "phishing":

        reasons.append(
            "The machine learning model classified "
            "the URL as potentially phishing."
        )

    else:

        reasons.append(
            "The machine learning model classified "
            "the URL as potentially legitimate."
        )


    # =====================================================
    # 9. SCORE INTERPRETATION
    # =====================================================

    if score >= 70:

        reasons.append(
            "Overall, the URL has a high-risk score."
        )

    elif score >= 40:

        reasons.append(
            "Overall, the URL has a medium-risk score."
        )

    elif score > 0:

        reasons.append(
            "Overall, the URL has some potentially "
            "suspicious characteristics."
        )

    else:

        reasons.append(
            "No major suspicious URL characteristics "
            "were detected by the current rules."
        )


    # =====================================================
    # RETURN EXPLANATION
    # =====================================================

    return " ".join(reasons)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    test_features = {

        "url_length": 18,

        "has_https": 1,

        "num_dots": 1,

        "num_hyphens": 0,

        "num_slashes": 2,

        "num_digits": 0,

        "num_special_chars": 4,

        "num_subdomains": 0

    }


    test_prediction = "legitimate"


    test_score = calculate_risk(
        test_features,
        test_prediction
    )


    test_explanation = generate_explanation(
        test_features,
        test_prediction,
        test_score
    )


    print("======================================")
    print("       PHISHGUARD RISK ENGINE")
    print("======================================")

    print()

    print("Prediction:")
    print(test_prediction)

    print()

    print("Risk Score:")
    print(test_score)

    print()

    print("Explanation:")
    print(test_explanation)

    print()

    print("======================================")
