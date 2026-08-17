from enrichment.enricher import enrich_ioc


result = enrich_ioc(
    value="192.0.2.210",
    ioc_type="IP",
    occurrence_count=7,
    confidence="High",
    severity="High",
)


print("\nEnrichment Result")
print("=================")

for key, value in result.items():
    print(f"{key}: {value}")