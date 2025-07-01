import logging
from pathlib import Path
import re


def fetch_art(settings: dict, order_number: str, pair_num: int) -> Path:
    """Return the artwork path for ``order_number`` and ``pair_num``.

    The search first checks the configured month directory. Any folder named
    after the ``order_number`` is considered the order root regardless of the
    company path above it. If a ``proof`` subfolder exists it is searched for
    pair files. Otherwise the order directory itself is scanned for PDFs
    containing ``proof`` with version suffixes (``v1``, ``v2`` ...); the highest
    version is returned. If nothing is found there, the main art directory is
    searched next.
    """
    logger = logging.getLogger(__name__)
    order_number = str(order_number).strip()
    pair_suffix = f"#{pair_num}"
    candidates: list[Path] = []
    order_roots: list[Path] = []

    month_dir = settings.get("month_dir")
    if month_dir:
        base = Path(month_dir)
        if base.exists():
            for p in base.rglob(order_number):
                if p.is_dir():
                    order_roots.append(p)
                    proof_dir = p / "proof"
                    if proof_dir.exists():
                        candidates.append(proof_dir)
                    candidates.extend([p / "art", p])

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

    # Fallback: search order directories for highest proof version
    for root in order_roots:
        best: Path | None = None
        best_version = -1
        for path in root.glob("*.pdf"):
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
