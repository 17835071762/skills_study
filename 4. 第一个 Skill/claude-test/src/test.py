from enum import Enum
from decimal import Decimal
from dataclasses import dataclass


class UserLevel(Enum):
    NORMAL = 1  # 普通会员
    VIP = 2     # VIP 会员
    SVIP = 3    # 超级会员


@dataclass
class User:
    level: UserLevel
    total_spent: Decimal = Decimal("0")


@dataclass
class DiscountResult:
    original_amount: Decimal
    final_amount: Decimal
    discount_amount: Decimal
    discount_rate: str


def _internal_calculate_discount(user: User, amount: Decimal) -> DiscountResult:
    """Calculate discount amount for a user based on their level and total spending.

    - NORMAL: no discount
    - VIP: 10% off
    - SVIP: 20% off
    - If total spending >= 10000, extra 5% off (max 50% total discount)
    """   
    if amount <= 0:
        return DiscountResult(
            original_amount=amount,
            final_amount=Decimal("0"),
            discount_amount=Decimal("0"),
            discount_rate="0%",
        )

    rate = {
        UserLevel.NORMAL: Decimal("1.00"),
        UserLevel.VIP: Decimal("0.90"),
        UserLevel.SVIP: Decimal("0.80"),
    }.get(user.level, Decimal("1.00"))

    if user.total_spent >= Decimal("10000"):
        rate = max(rate - Decimal("0.05"), Decimal("0.50"))

    final = (amount * rate).quantize(Decimal("0.01"))
    discount = amount - final

    return DiscountResult(
        original_amount=amount,
        final_amount=final,
        discount_amount=discount,
        discount_rate=f"{(1 - rate) * 100:.0f}%",
    )


def main():
    tests = [
        (UserLevel.NORMAL, Decimal("500"), Decimal("0")),
        (UserLevel.VIP, Decimal("500"), Decimal("0")),
        (UserLevel.SVIP, Decimal("500"), Decimal("0")),
        (UserLevel.VIP, Decimal("500"), Decimal("15000")),
    ]

    for level, amount, spent in tests:
        r = _internal_calculate_discount(User(level=level, total_spent=spent), amount)
        print(
            f"等级={level.name:6s} | 累计={str(spent):>7s} | "
            f"原价={str(amount):>7s} | 折后={str(r.final_amount):>7s} | "
            f"省={str(r.discount_amount):>6s} | {r.discount_rate}"
        )


if __name__ == "__main__":
    main()

