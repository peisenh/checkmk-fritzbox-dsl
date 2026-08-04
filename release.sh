#!/usr/bin/env bash
# Reads the top-most released version from CHANGELOG.md, creates an
# annotated tag and pushes it. The version lives only in the CHANGELOG;
# the tag is derived from it — no double bookkeeping.
#
# Usage:  ./release.sh [remote ...]     (default remote: origin)
set -euo pipefail

VERSION=$(grep -oP '^## \[\K[0-9]+\.[0-9]+\.[0-9]+' CHANGELOG.md | head -1)

if [ -z "${VERSION:-}" ]; then
  echo "No version found in CHANGELOG.md." >&2
  exit 1
fi

TAG="v$VERSION"

if git rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
  echo "Tag $TAG already exists." >&2
  exit 1
fi

git tag -a "$TAG" -m "Release $VERSION"

for remote in "${@:-origin}"; do
  git push "$remote" "$TAG"
done

echo "Tagged and pushed: $TAG"
