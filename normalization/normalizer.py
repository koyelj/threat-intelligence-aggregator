def normalize_indicator(value, ioc_type):
    value = value.strip()

    if ioc_type == "UNKNOWN":
        return None

    if ioc_type == "DOMAIN":
        value = value.lower()

    elif ioc_type == "EMAIL":
        value = value.lower()

    elif ioc_type == "URL":
        value = value.lower()

    return value
def remove_duplicates(indicators):
    unique_indicators = []
    seen = set()

    for indicator in indicators:

        normalized_value = normalize_indicator(
            indicator["value"],
            indicator["type"]
        )

        if normalized_value is None:
            continue

        key = (
            normalized_value,
            indicator["type"]
        )

        if key in seen:
            continue

        seen.add(key)

        unique_indicators.append(
            {
                **indicator,
                "value": normalized_value,
            }
        )

    return unique_indicators