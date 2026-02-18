# justfile
set shell := ["bash", "-euo", "pipefail", "-c"]

# ---------- configuration ----------

PACKS := "lucide material-official material-community phosphor font-awesome heroicons"

# ---------- public recipes ----------

help:
    @just --list

# Install a pack in development mode
install pack:
    @echo "Installing {{pack}}..."
    cd packs/{{pack}} && uv pip install -e . && cd ../..;

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
    @for pack in {{PACKS}}; do \
        echo "Fetching $pack..."; \
        just fetch $pack; \
    done

# Build all packs
build-all:
    @for pack in {{PACKS}}; do \
        echo "Building $pack..."; \
        just build $pack; \
    done

# Build distribution wheels for all packs
dist-all:
    @for pack in {{PACKS}}; do \
        echo "Distributing $pack..."; \
        just dist $pack; \
    done

# Run tests for all packages
test-all:
    @echo "Testing packs..."
    for pack in {{PACKS}}; do \
        if [ -d "packs/$pack/tests" ]; then \
            echo "Testing $pack..."; \
            cd "packs/$pack" && pytest && cd ../..; \
        fi; \
    done
