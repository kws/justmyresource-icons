# justfile
set shell := ["bash", "-euo", "pipefail", "-c"]

# Install all packages in development mode
help:
    @just --list

install pack:
    @echo "Installing {{pack}}..."
    cd packs/{{pack}} && uv pip install -e . && cd ../..;


# Build all packages
# build-all:
#     @echo "Building core..."
#     @echo "Building packs..."
#     for pack in packs/*/; do \
#         echo "Building $(basename $pack)..."; \
#         cd "$pack" && python -m build && cd ../..; \
#     done

# Run tests for all packages
test-all:
    @echo "Testing core..."
    cd ../justmyresource && pytest
    @echo "Testing packs..."
    for pack in packs/*/; do \
        if [ -d "$pack/tests" ]; then \
            echo "Testing $(basename $pack)..."; \
            cd "$pack" && pytest && cd ../..; \
        fi; \
    done

# Lint all code
lint:
    ruff check .
    ruff format --check .

# Format all code
format:
    ruff check . --fix
    ruff format .

# Type check all code
typecheck:
    mypy ../justmyresource/src
    for pack in packs/*/src/*/; do \
        mypy "$pack"; \
    done

# Fetch upstream archive for a specific pack (downloads to cache/)
fetch pack:
    pack-tools fetch packs/{{pack}}

# Build pack (extracts from cache, generates icons.zip + manifest + README)
build pack:
    pack-tools build packs/{{pack}}

# Build distribution wheel
dist pack:
    pack-tools dist packs/{{pack}}

# Fetch all upstream sources
fetch-all:
    @for pack in lucide material-official material-community phosphor font-awesome heroicons; do \
        echo "Fetching $pack..."; \
        just fetch $pack; \
    done

# Build all packs
build-all:
    @for pack in lucide material-official material-community phosphor font-awesome heroicons; do \
        echo "Building $pack..."; \
        just build $pack; \
    done

# Generate README.md files for all packs
generate-readmes:
    @for pack in packs/*/; do \
        if [ -f "$$pack/upstream.toml" ]; then \
            python -c "from justmyresource_pack_tools.readme import generate_readme; from pathlib import Path; generate_readme(Path('$$pack'))"; \
        fi; \
    done