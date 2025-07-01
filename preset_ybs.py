import logging
from pathlib import Path
import re


def fetch_art(settings: dict, order_number: str, pair_num: int) -> Path:
    """Return the artwork path for ``order_number`` and ``pair_num``.

    The search first checks the configured month directory which may include a
    company subfolder. If a ``proof`` folder exists it is searched for pair
    files. Otherwise the order directory itself is scanned for PDFs containing
    ``proof`` with version suffixes (``v1``, ``v2`` ...); the highest version is
    returned. If nothing is found there, the main art directory is searched next.
    """
    logger = logging.getLogger(__name__)
    order_number = str(order_number).strip()
    pair_suffix = f"#{pair_num}"
    company = settings.get("company", "").strip()
    candidates: list[Path] = []

    month_dir = settings.get("month_dir")
    order_root: Path | None = None
    if month_dir:
        order_root = Path(month_dir)
        if company:
            order_root = order_root / company / order_number
        else:
            order_root = order_root / order_number
        proof_dir = order_root / "proof"
        if proof_dir.exists():
            candidates.append(proof_dir)
        candidates.extend([order_root / "art", order_root])

    art_root = settings.get("art_dir") or settings.get("art_server_path")
    if art_root:
        candidates.append(Path(art_root))

    patterns = [f"{order_number}.{pair_num}.pdf", f"*_{pair_suffix}.*"]

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

    # Fallback: search order directory for highest proof version
    if order_root and order_root.exists():
        best: Path | None = None
        best_version = -1
        for path in order_root.glob("*.pdf"):
            name = path.name.lower()
            if "proof" not in name:
                continue
            m = re.search(r"v(\d+)", name)
            version = int(m.group(1)) if m else 0
            if version > best_version:
                best_version = version
                best = path.resolve()
        if best:
            if "$recycle" in str(best).lower():
                raise ValueError("Refusing…")
            logger.info("Selected %s", best)
            return best

    raise FileNotFoundError(f"Art not found for order {order_number} pair {pair_num}")
