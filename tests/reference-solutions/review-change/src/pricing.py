def final_total(subtotal_cents: int, is_member: bool) -> int:
    if subtotal_cents < 0:
        raise ValueError("subtotal_cents must be non-negative")
    if is_member:
        return subtotal_cents * 90 // 100
    return subtotal_cents
