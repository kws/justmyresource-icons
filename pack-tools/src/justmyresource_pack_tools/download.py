"""Download utilities for upstream archives."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from urllib.request import urlopen


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 checksum of a file.

    Args:
        file_path: Path to file.

    Returns:
        SHA-256 hex digest.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def verify_sha256(file_path: Path, expected_sha256: str) -> bool:
    """Verify file SHA-256 checksum.

    Args:
        file_path: Path to file to verify.
        expected_sha256: Expected SHA-256 hex digest.

    Returns:
        True if checksum matches, False otherwise.
    """
    computed = compute_sha256(file_path)
    return computed.lower() == expected_sha256.lower()


def download(url: str, dest: Path | None = None) -> Path:
    """Download a file from URL to a temporary or specified location.

    Args:
        url: URL to download from.
        dest: Optional destination path. If None, creates a temporary file.

    Returns:
        Path to downloaded file.

    Raises:
        OSError: If download fails.
    """
    if dest is None:
        # Determine suffix from URL
        suffix = ""
        if url.endswith(".tar.gz") or url.endswith(".tgz"):
            suffix = ".tar.gz"
        elif url.endswith(".zip"):
            suffix = ".zip"
        elif url.endswith(".tar"):
            suffix = ".tar"

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        dest = Path(tmp_file.name)
        tmp_file.close()

    dest.parent.mkdir(parents=True, exist_ok=True)

    with urlopen(url) as response:
        with open(dest, "wb") as f:
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                f.write(chunk)

    return dest


def download_with_cache(
    url: str,
    cache_dir: Path,
    expected_sha256: str | None = None,
) -> Path:
    """Download file with caching support.

    Checks if a cached version exists and validates it with SHA-256 if provided.
    If cache is valid, returns cached path. Otherwise downloads fresh copy to cache.

    Args:
        url: URL to download from.
        cache_dir: Directory for cache storage (e.g., packs/lucide/cache/).
        expected_sha256: Expected SHA-256. If provided and cache matches, reuse cache.

    Returns:
        Path to downloaded/cached file.

    Raises:
        ValueError: If downloaded file SHA-256 doesn't match expected_sha256.
        OSError: If download fails.
    """
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Derive filename from URL
    filename = url.split("/")[-1]
    cache_path = cache_dir / filename

    # Check cache
    if cache_path.exists():
        if expected_sha256:
            if verify_sha256(cache_path, expected_sha256):
                print(f"✓ Using cached {filename} (SHA-256 verified)")
                return cache_path
            else:
                print(f"⚠️  Cached {filename} SHA-256 mismatch, re-downloading...")
        else:
            print(f"✓ Using cached {filename} (no SHA-256 check)")
            return cache_path

    # Download to cache
    print(f"Downloading {filename}...")
    download(url, dest=cache_path)

    # Verify downloaded file if SHA-256 provided
    if expected_sha256:
        if not verify_sha256(cache_path, expected_sha256):
            computed = compute_sha256(cache_path)
            raise ValueError(
                f"Downloaded file SHA-256 mismatch!\n"
                f"  Expected: {expected_sha256}\n"
                f"  Computed: {computed}"
            )
        print(f"✓ SHA-256 verified")
    else:
        computed = compute_sha256(cache_path)
        print(f"⚠️  No SHA-256 in upstream.toml. Computed: {computed}")

    return cache_path


