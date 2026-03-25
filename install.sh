#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir="$repo_root/skills"
target_dir="$HOME/.claude/skills"

log() {
  printf '[install] %s\n' "$1"
}

error() {
  printf '[install] error: %s\n' "$1" >&2
}

log "starting install from $source_dir to $target_dir"

if [ -d "$target_dir" ]; then
  log "target directory already exists: $target_dir"
else
  log "creating target directory: $target_dir"
  mkdir -p "$target_dir"
fi

find "$source_dir" -mindepth 1 -maxdepth 1 -type d | sort | while IFS= read -r skill_dir; do
  skill_name=$(basename "$skill_dir")
  link_path="$target_dir/$skill_name"

  if [ -L "$link_path" ]; then
    current_target=$(readlink "$link_path")
    if [ "$current_target" = "$skill_dir" ]; then
      log "already linked: $link_path"
      continue
    fi
    error "existing symlink points elsewhere: $link_path -> $current_target"
    exit 1
  fi

  if [ -e "$link_path" ]; then
    error "existing path blocks symlink: $link_path"
    exit 1
  fi

  ln -s "$skill_dir" "$link_path"
  log "linked $skill_name -> $skill_dir"
done
