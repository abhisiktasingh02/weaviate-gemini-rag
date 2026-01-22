THRESHOLD = 0.5

def is_relevant(distance: float) -> bool:
    return distance <= THRESHOLD
