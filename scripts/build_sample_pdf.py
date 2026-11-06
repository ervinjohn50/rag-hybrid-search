"""Regenerate sample_docs/warranty-and-returns.pdf. Run from the project root."""

from pathlib import Path

from tests.pdf_factory import make_pdf

PAGES = [
    """Larkfield Warranty and Returns Policy (fictional sample content)

Limited warranty
The LF-200 gateway is covered for 24 months from the date of purchase
against defects in materials and workmanship. The power adapter and
patch lead are covered for 12 months. Keep your proof of purchase,
because a claim cannot be processed without it.

What the warranty does not cover
The warranty does not cover damage from lightning or power surges,
liquid damage, opened or altered units, or normal wear to the case.
Replacing firmware with software not supplied by Larkfield also ends
the warranty.""",
    """Returning a product you changed your mind about
You may return an unused product within 30 days of delivery for a full
refund. It must be in the original packaging with all accessories. You
pay the postage for this kind of return. Refunds are issued to the
original payment method within 10 working days of receiving the item.

Faulty units
To claim for a faulty unit, request a return authorisation number,
which has the format RMA-LF followed by six digits, for example
RMA-LF204417. Write this number on the outside of the parcel. Larkfield
pays the postage for approved faulty returns, and sends a replacement
within 5 working days of receiving the faulty unit.""",
    """Replacement units
A replacement unit is covered for the rest of the original warranty,
or for 90 days, whichever is longer. Before sending a unit back, save
your settings with Download Settings and then perform a factory reset,
because returned units are not guaranteed to be kept and any personal
settings on them will be erased.

Contacting support
Support is available from 08:00 to 20:00, Monday to Saturday. Have your
serial number ready, which begins with LFK and is printed on the label
underneath the unit.""",
]


def main() -> None:
    Path("sample_docs/warranty-and-returns.pdf").write_bytes(make_pdf(PAGES))


if __name__ == "__main__":
    main()
