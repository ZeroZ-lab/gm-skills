#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir="$repo_root/skills"

log() {
  printf '[uninstall] %s\n' "$1"
}

error() {
  printf '[uninstall] error: %s\n' "$1" >&2
}

prompt_target() {
  printf 'Select uninstall target:\n' >&2
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

uninstall_from_target() {
  target_name=$1
  target_dir=$(resolve_target_dir "$target_name")

  log "selected target: $target_name ($target_dir)"
  log "starting uninstall from $target_dir"

  if [ ! -d "$target_dir" ]; then
    log "target directory does not exist: $target_dir"
    return 0
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
}

selection=${1:-}
[ -n "$selection" ] || selection=$(prompt_target)

case "$selection" in
  claude|codex|agent)
    uninstall_from_target "$selection"
    ;;
  all)
    uninstall_from_target claude
    uninstall_from_target codex
    uninstall_from_target agent
    ;;
  *)
    error "unknown target: $selection"
    exit 1
    ;;
esac
