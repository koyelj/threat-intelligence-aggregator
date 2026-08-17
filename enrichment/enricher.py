from datetime import datetime, timezone


def enrich_ioc(
    value,
    ioc_type,
    occurrence_count=1,
    confidence="Medium",
    severity="Low",
):
    now = datetime.now(timezone.utc)

    return {
        "value": value,
        "ioc_type": ioc_type,
        "occurrence_count": occurrence_count,
        "confidence": confidence,
        "severity": severity,
        "enriched_at": now,
        "context": {
            "is_high_frequency": occurrence_count >= 5,
            "is_high_severity": severity.lower() == "high",
            "is_high_confidence": confidence.lower() == "high",
        },
    }