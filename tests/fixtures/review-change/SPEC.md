# Member discount

Update `final_total(subtotal_cents, is_member)` with these requirements:

- Reject a negative subtotal with `ValueError`.
- Return the subtotal unchanged for a non-member.
- Return exactly 90% of integer cents for a member, rounded down to an integer cent.
- Preserve the existing public function signature; the discount is fixed policy, not caller configuration.
