#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir="$repo_root/skills"
target_dir="$HOME/.claude/skills"

log() {
  printf '[uninstall] %s\n' "$1"
}

error() {
  printf '[uninstall] error: %s\n' "$1" >&2
}

log "starting uninstall from $target_dir"

if [ ! -d "$target_dir" ]; then
  log "target directory does not exist: $target_dir"
  exit 0
fi

if [ ! -d "$source_dir" ]; then
  error "source directory does not exist: $source_dir"
  exit 1
fi

find "$source_dir" -mindepth 1 -maxdepth 1 -type d | sort | while IFS= read -r skill_dir; do
  skill_name=$(basename "$skill_dir")
  link_path="$target_dir/$skill_name"

  if [ -L "$link_path" ]; then
    current_target=$(readlink "$link_path")
    if [ "$current_target" = "$skill_dir" ]; then
      rm "$link_path"
      log "removed link: $link_path"
    else
      log "skipped unrelated link: $link_path"
    fi
  fi
done

find "$target_dir" -mindepth 1 -maxdepth 1 -type l | while IFS= read -r link_path; do
  link_name=$(basename "$link_path")
  expected_path="$source_dir/$link_name"
  current_target=$(readlink "$link_path")

  [ "$current_target" = "$expected_path" ] && continue

  log "skipped unrelated link: $link_path"
done
