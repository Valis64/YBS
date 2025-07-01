import logging
from pathlib import Path


def fetch_art(settings: dict, order_number: str, pair_num: int) -> Path:
    """Return the artwork path for ``order_number`` and ``pair_num``.

    The search checks the month folder followed by the main art directory.
    The first matching file found via ``Path.rglob`` is returned.
    """
    logger = logging.getLogger(__name__)
    order_number = str(order_number).strip()
    pair_suffix = f"#{pair_num}"
    candidates: list[Path] = []

    month_dir = settings.get("month_dir")
    if month_dir:
        order_root = Path(month_dir) / order_number
        candidates.extend([
            order_root / "art",
            order_root / "proof",
        ])

    art_root = settings.get("art_dir") or settings.get("art_server_path")
    if art_root:
        candidates.append(Path(art_root))

    patterns = [
        f"{order_number}.{pair_num}.pdf",
        f"*_{pair_suffix}.*",
    ]

    for base in candidates:
        if not base or not base.exists():
            continue
        for pattern in patterns:
            logger.info("Searching %s for pattern %s", base, pattern)
            for path in base.rglob(pattern):
                resolved = path.resolve()
                if "$recycle" in str(resolved).lower():
                    raise ValueError("Refusing…")
                logger.info("Found %s", resolved)
                return resolved
    raise FileNotFoundError(f"Art not found for order {order_number} pair {pair_num}")
