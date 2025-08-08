from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    # Ensure backend root is on sys.path so imports like `money.schema` work
    if str(backend_root) not in sys.path:
        sys.path.insert(0, str(backend_root))

    # Default to local settings unless explicitly provided
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.local"),
    )

    import django

    django.setup()

    from money.schema import schema  # noqa: WPS433

    sdl = schema.as_str()
    output_path = backend_root / "schema.graphql"
    output_path.write_text(sdl, encoding="utf-8")
    print(f"Wrote schema to {output_path}")


if __name__ == "__main__":
    main()
