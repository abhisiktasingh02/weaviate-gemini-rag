from weaviate.classes.query import Filter

def build_filters(parsed):
    filters = None
    if parsed["modality"] != "any":
        filters = Filter.by_property("modality").equal(parsed["modality"])
    return filters
