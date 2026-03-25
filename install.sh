#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir="$repo_root/skills"

log() {
  printf '[install] %s\n' "$1"
}

error() {
  printf '[install] error: %s\n' "$1" >&2
}

prompt_target() {
  printf 'Select install target:\n' >&2
  printf '1) claude\n' >&2
  printf '2) codex\n' >&2
  printf '3) agent\n' >&2
  printf '4) all\n' >&2
  printf '> ' >&2
  IFS= read -r choice

  case "$choice" in
    1) printf 'claude\n' ;;
    2) printf 'codex\n' ;;
    3) printf 'agent\n' ;;
    4) printf 'all\n' ;;
    *) error "invalid selection: $choice"; exit 1 ;;
  esac
}

resolve_target_dir() {
  case "$1" in
    claude) printf '%s\n' "$HOME/.claude/skills" ;;
    codex) printf '%s\n' "$HOME/.codex/skills" ;;
    agent) printf '%s\n' "$HOME/.agents/skills" ;;
    *) error "unknown target: $1"; exit 1 ;;
  esac
}

install_into_target() {
  target_name=$1
  target_dir=$(resolve_target_dir "$target_name")

  log "selected target: $target_name ($target_dir)"
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
}

selection=${1:-}
[ -n "$selection" ] || selection=$(prompt_target)

case "$selection" in
  claude|codex|agent)
    install_into_target "$selection"
    ;;
  all)
    install_into_target claude
    install_into_target codex
    install_into_target agent
    ;;
  *)
    error "unknown target: $selection"
    exit 1
    ;;
esac
