#!/usr/bin/env bash

# --- Shell guard (POSIX-compatible) -------------------------------------------
# The body of this script is bash (arrays, [[ ]], local, =~). When invoked under
# any other shell — sh/dash (e.g. "curl ... | sh" on Ubuntu 24) or zsh (the macOS
# default login shell, e.g. "curl ... | zsh") — it re-launches itself under bash
# so the same one-liner works regardless of the user's shell. This block uses
# only POSIX syntax so it parses cleanly in sh, dash, zsh, and bash.
if [ -z "${BASH_VERSION:-}" ]; then
  if ! command -v bash >/dev/null 2>&1; then
    echo "Error: This script requires bash, which was not found." >&2
    echo "       Install bash and re-run:  curl -fsSL https://temps.sh/deploy.sh | bash" >&2
    exit 1
  fi
  # Running from a real file (e.g. "zsh deploy.sh" / "sh deploy.sh") — re-exec
  # bash on the file directly. Guard against "$0" being the shell name itself
  # ("-zsh", "sh") which can happen for piped/login invocations.
  if [ -f "$0" ] 2>/dev/null && [ "$0" != "sh" ] && [ "$0" != "zsh" ] && [ "$0" != "-zsh" ]; then
    exec bash "$0" "$@"
  fi
  # Piped via stdin (e.g. "curl ... | zsh" or "curl ... | sh"). zsh and dash read
  # the whole pipe into memory before executing, so the rest of the script is
  # still on stdin here — buffer it to a temp file and re-exec bash on that. The
  # re-exec'd bash run removes the temp file via the EXIT trap below.
  _temps_reexec=$(mktemp "${TMPDIR:-/tmp}/temps-deploy.XXXXXX" 2>/dev/null) || _temps_reexec="${TMPDIR:-/tmp}/temps-deploy.$$"
  cat > "$_temps_reexec" || {
    echo "Error: failed to buffer script for bash re-exec." >&2
    echo "       Re-run with:  curl -fsSL https://temps.sh/deploy.sh | bash" >&2
    exit 1
  }
  TEMPS_REEXEC_CLEANUP="$_temps_reexec" exec bash "$_temps_reexec" "$@"
fi
# ------------------------------------------------------------------------------

set -euo pipefail

# When we re-exec'd from a non-bash shell via a buffered temp file (see the guard
# above), delete that temp file on exit so we don't litter $TMPDIR.
if [ -n "${TEMPS_REEXEC_CLEANUP:-}" ]; then
  trap 'rm -f "$TEMPS_REEXEC_CLEANUP"' EXIT
fi

# ============================================================================
#  Temps Provisioning Wizard
#  A beautiful TUI to set up Docker, TimescaleDB, SSL certificates, and Temps
# ============================================================================

# Wrap in block to ensure bash reads entire script before executing (needed for curl | bash)
{

# ---------------------------------------------------------------------------
# TUI Framework: Colors, Symbols, Drawing
# ---------------------------------------------------------------------------

BOLD='' DIM='' RESET='' UNDERLINE=''
RED='' GREEN='' YELLOW='' BLUE='' CYAN='' MAGENTA='' WHITE=''
BG_BLUE='' BG_GREEN='' BG_RED='' BG_YELLOW=''

if [[ -t 1 ]]; then
  BOLD='\033[1m'       DIM='\033[2m'        RESET='\033[0m'
  UNDERLINE='\033[4m'
  RED='\033[0;31m'     GREEN='\033[0;32m'   YELLOW='\033[0;33m'
  BLUE='\033[0;34m'    CYAN='\033[0;36m'    MAGENTA='\033[0;35m'
  WHITE='\033[0;37m'
  BG_BLUE='\033[44m'   BG_GREEN='\033[42m'  BG_RED='\033[41m'
  BG_YELLOW='\033[43m'
fi

# Symbols
CHECK="${GREEN}✓${RESET}"
CROSS="${RED}✗${RESET}"
ARROW="${CYAN}→${RESET}"
BULLET="${DIM}•${RESET}"
SPINNER_CHARS='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'

# ---------------------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------------------
OS="$(uname -s)"
ARCH="$(uname -m)"
IS_MACOS=false
IS_LINUX=false

case "$OS" in
  Darwin) IS_MACOS=true ;;
  Linux)  IS_LINUX=true ;;
  *)      echo "Unsupported OS: $OS"; exit 1 ;;
esac

# Home directory — /root on Linux servers running as root, $HOME otherwise
if [[ "$IS_LINUX" == "true" ]] && [[ $EUID -eq 0 ]]; then
  HOME_DIR="/root"
else
  HOME_DIR="${HOME:-$( eval echo ~"$(whoami)" )}"
fi

# Sudo prefix — empty when root, "sudo" when non-root
SUDO=""
RUN_USER="$(whoami)"
if [[ $EUID -ne 0 ]]; then
  SUDO="sudo"
fi

# Portable sed in-place: GNU sed uses -i, BSD (macOS) sed uses -i ''
if [[ "$IS_MACOS" == "true" ]]; then
  sed_i() { sed -i '' "$@"; }
else
  sed_i() { sed -i "$@"; }
fi

# Portable lowercase: Bash 4+ has ${var,,}, Bash 3.2 (macOS default) does not
to_lower() {
  echo "$1" | tr '[:upper:]' '[:lower:]'
}

# State directory for idempotency
STATE_DIR="$HOME_DIR/.temps/.wizard-state"

# Terminal width
term_width() {
  tput cols 2>/dev/null || echo 80
}

# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

hr() {
  local w
  w=$(term_width)
  printf "${DIM}"
  printf '%.0s─' $(seq 1 "$w")
  printf "${RESET}\n"
}

banner() {
  # Only clear a real terminal. Without one (`ssh host 'cmd'`, cloud-init, CI)
  # TERM is unset, `clear` exits non-zero, and under `set -e` that killed the
  # whole installer before it printed anything but "TERM environment variable
  # not set."
  if [[ -t 1 ]]; then clear 2>/dev/null || true; fi
  echo ""
  hr
  printf "${BOLD}${CYAN}"
  cat << 'LOGO'

   ████████╗███████╗███╗   ███╗██████╗ ███████╗
   ╚══██╔══╝██╔════╝████╗ ████║██╔══██╗██╔════╝
      ██║   █████╗  ██╔████╔██║██████╔╝███████╗
      ██║   ██╔══╝  ██║╚██╔╝██║██╔═══╝ ╚════██║
      ██║   ███████╗██║ ╚═╝ ██║██║     ███████║
      ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝

LOGO
  printf "${RESET}"
  printf "   ${DIM}Self-hosted deployment platform${RESET}\n"
  printf "   ${DIM}https://temps.sh${RESET}\n"
  hr
  echo ""
}

step_header() {
  local step_num="$1" total="$2" title="$3"
  local w
  w=$(term_width)
  echo ""
  printf "  ${BG_BLUE}${BOLD}${WHITE} STEP %s/%s ${RESET}  ${BOLD}%s${RESET}\n" "$step_num" "$total" "$title"
  printf "  ${DIM}"
  printf '%.0s─' $(seq 1 $((w - 4)))
  printf "${RESET}\n"
  echo ""
}

info()    { printf "  ${BULLET} %b\n" "$*"; }
success() { printf "  ${CHECK} ${GREEN}%b${RESET}\n" "$*"; }
warn()    { printf "  ${YELLOW}! %b${RESET}\n" "$*"; }
error()   { printf "  ${CROSS} ${RED}%b${RESET}\n" "$*"; }
fatal()   { error "$@"; echo ""; exit 1; }

# Download with a few retries. A single DNS or network blip otherwise ends the
# install at step 3, after Docker and the database are already set up.
# (`curl --retry` alone does not retry "Could not resolve host", and
# --retry-all-errors needs curl 7.71+, newer than some supported distros.)
download_with_retry() {
  local url="$1" out="$2" attempt
  for attempt in 1 2 3 4; do
    if curl --fail --location --progress-bar --output "$out" "$url"; then
      return 0
    fi
    if [[ $attempt -lt 4 ]]; then
      warn "Download failed (attempt $attempt of 4), retrying in $((attempt * 3))s..."
      sleep $((attempt * 3))
    fi
  done
  return 1
}

# port_in_use PORT
# Returns 0 (true) if something is already listening on TCP PORT on localhost.
# Tries lsof, then ss, then netstat — whichever exists. If none are available
# we cannot tell, so we return 1 (false) rather than block the install.
port_in_use() {
  local port="$1"
  if command -v lsof >/dev/null 2>&1; then
    lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1 && return 0
    return 1
  fi
  if command -v ss >/dev/null 2>&1; then
    ss -ltn 2>/dev/null | grep -qE "[:.]${port}[[:space:]]" && return 0
    return 1
  fi
  if command -v netstat >/dev/null 2>&1; then
    netstat -an 2>/dev/null | grep -qE "[:.]${port}[[:space:]].*LISTEN" && return 0
    return 1
  fi
  return 1
}

# port_holder PORT
# Best-effort description of what is listening on PORT (for diagnostics only).
# Prints a human-readable line or nothing. Never fails the caller.
port_holder() {
  local port="$1"
  if command -v lsof >/dev/null 2>&1; then
    lsof -nP -iTCP:"$port" -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print "    "$1" (pid "$2")"}' | sort -u | head -3
  fi
}

# next_free_port START [MAX_TRIES]
# Prints the first free TCP port at or after START. Scans up to MAX_TRIES
# consecutive ports (default 20). Prints nothing and returns 1 if none are
# free in range — the caller decides how to handle that.
next_free_port() {
  local start="$1" tries="${2:-20}" p
  for ((p = start; p < start + tries; p++)); do
    if ! port_in_use "$p"; then
      printf '%s' "$p"
      return 0
    fi
  done
  return 1
}

# container_db_host_port NAME
# Prints the host port that container NAME publishes for postgres (5432/tcp),
# or nothing if it can't be determined. Used to recover DB_PORT on a re-run
# when the wizard state was lost but the container still exists.
container_db_host_port() {
  local name="$1"
  $DOCKER_SUDO docker inspect -f \
    '{{range $p, $conf := .NetworkSettings.Ports}}{{if eq $p "5432/tcp"}}{{(index $conf 0).HostPort}}{{end}}{{end}}' \
    "$name" 2>/dev/null | head -1
}

# prompt_input LABEL DEFAULT VARNAME
# Reads user input and writes it to the named global variable.
# All output goes to stderr (/dev/tty) so it's safe in subshells,
# and we use printf -v instead of eval for safety.
# require_tty LABEL — fail with an actionable message when no controlling
# terminal is available (e.g. `ssh host 'bash deploy.sh'` or CI), instead of
# dying with bash's cryptic "/dev/tty: No such device or address" mid-prompt.
require_tty() {
  local label="$1"
  if ! { : < /dev/tty; } 2>/dev/null; then
    fatal "Interactive prompt '$label' needs a terminal. Re-run from a terminal (over SSH: ssh -t), or headless with --yes plus --email/--domain — see --help."
  fi
}

prompt_input() {
  local label="$1" default="${2:-}" var_name="$3"
  local _input
  if [[ "$ASSUME_YES" == "true" ]]; then
    if [[ -n "$default" ]]; then
      info "${DIM}--yes:${RESET} ${label} ${ARROW} ${BOLD}${default}${RESET}" >&2
      printf -v "$var_name" '%s' "$default"
      return 0
    fi
    fatal "'$label' has no default answer and cannot be skipped with --yes. Provide it via a flag (--email / --domain, see --help) or run interactively."
  fi
  require_tty "$label"
  if [[ -n "$default" ]]; then
    printf "  ${ARROW} ${BOLD}%s${RESET} ${DIM}[%s]${RESET}: " "$label" "$default" >&2
  else
    printf "  ${ARROW} ${BOLD}%s${RESET}: " "$label" >&2
  fi
  read -r _input < /dev/tty
  _input="${_input:-$default}"
  printf -v "$var_name" '%s' "$_input"
}

# prompt_secret LABEL VARNAME
# Reads input one character at a time, printing * for each keystroke.
prompt_secret() {
  local label="$1" var_name="$2"
  local _input="" _char
  if [[ "$ASSUME_YES" == "true" ]]; then
    fatal "'$label' is a secret prompt and cannot be answered with --yes. Run this step interactively."
  fi
  require_tty "$label"
  printf "  ${ARROW} ${BOLD}%s${RESET}: " "$label" >&2
  while IFS= read -rs -n1 _char < /dev/tty; do
    # Enter (empty read) terminates input
    if [[ -z "$_char" ]]; then
      break
    fi
    # Backspace / Delete
    if [[ "$_char" == $'\x7f' || "$_char" == $'\b' ]]; then
      if [[ -n "$_input" ]]; then
        _input="${_input%?}"
        printf '\b \b' >&2
      fi
      continue
    fi
    _input+="$_char"
    printf '*' >&2
  done
  echo "" >&2
  printf -v "$var_name" '%s' "$_input"
}

prompt_yesno() {
  local label="$1" default="${2:-y}"
  local hint answer
  if [[ "$ASSUME_YES" == "true" ]]; then
    info "${DIM}--yes:${RESET} ${label} ${ARROW} ${BOLD}${default}${RESET}"
    [[ "$default" == "y" ]]
    return
  fi
  require_tty "$label"
  if [[ "$default" == "y" ]]; then hint="Y/n"; else hint="y/N"; fi
  printf "  ${ARROW} ${BOLD}%s${RESET} ${DIM}[%s]${RESET}: " "$label" "$hint"
  read -r answer < /dev/tty
  answer="${answer:-$default}"
  local lower
  lower=$(to_lower "$answer")
  [[ "$lower" == "y" || "$lower" == "yes" ]]
}

# prompt_choice VARNAME LABEL DEFAULT OPTION1 OPTION2 ...
# Writes the numeric choice (1, 2, ...) into the named global variable.
# Prints menu to stdout directly — never call this inside $().
# DEFAULT is the 1-based option number to auto-pick under --yes, or "" if
# this menu has no safe unattended answer (e.g. the DNS retry menus, whose
# choices depend on state --yes can't observe — those must stay fatal).
prompt_choice() {
  local var_name="$1" label="$2" default="$3"
  shift 3
  local options=("$@")
  if [[ "$ASSUME_YES" == "true" ]]; then
    if [[ -n "$default" ]]; then
      info "${DIM}--yes:${RESET} ${label} ${ARROW} ${BOLD}${options[$((default - 1))]}${RESET}"
      printf -v "$var_name" '%s' "$default"
      return
    fi
    fatal "'$label' is a menu prompt and cannot be answered with --yes. Run this step interactively (over SSH: ssh -t)."
  fi
  require_tty "$label"
  echo ""
  printf "  ${BOLD}%s${RESET}\n" "$label"
  echo ""
  local i=1
  for opt in "${options[@]}"; do
    printf "    ${CYAN}%d)${RESET}  %s\n" "$i" "$opt"
    ((i++))
  done
  echo ""
  local _choice
  printf "  ${ARROW} ${BOLD}Enter choice${RESET} ${DIM}[1-%d]${RESET}: " "${#options[@]}"
  read -r _choice < /dev/tty
  printf -v "$var_name" '%s' "$_choice"
}

# Spinner — runs a command with an animated spinner
spinner() {
  local msg="$1"
  shift
  local pid i=0

  # Run command in background (stdin from /dev/null to prevent subprocesses
  # from consuming the script pipe when running under curl | bash)
  "$@" < /dev/null > /tmp/temps-wizard-cmd-out.log 2>&1 &
  pid=$!

  # Animate
  printf "  "
  while kill -0 "$pid" 2>/dev/null; do
    local char="${SPINNER_CHARS:$i:1}"
    printf "\r  ${CYAN}%s${RESET} %s" "$char" "$msg"
    i=$(( (i + 1) % ${#SPINNER_CHARS} ))
    sleep 0.1
  done

  # Check exit status
  wait "$pid"
  local exit_code=$?
  if [[ $exit_code -eq 0 ]]; then
    printf "\r  ${CHECK} %s\n" "$msg"
  else
    printf "\r  ${CROSS} %s ${RED}(failed)${RESET}\n" "$msg"
  fi
  return $exit_code
}

# Progress bar
progress_bar() {
  local current="$1" total="$2" label="${3:-}"
  local tw pct label_len bar_width filled empty bar_str

  tw=$(term_width)
  pct=$(( current * 100 / total ))

  # Fixed visible overhead: "  [" (3) + "]" (1) + " " (1) + "NNN%" (4) = 9 chars
  # Plus label: " " (1) + label text
  label_len=${#label}
  if [[ $label_len -gt 0 ]]; then
    bar_width=$(( tw - 10 - label_len ))
  else
    bar_width=$(( tw - 9 ))
  fi

  # If terminal too narrow for label, drop it
  if [[ $bar_width -lt 10 ]]; then
    label=""
    label_len=0
    bar_width=$(( tw - 9 ))
    [[ $bar_width -lt 10 ]] && bar_width=10
  fi

  filled=$(( current * bar_width / total ))
  empty=$(( bar_width - filled ))

  # Build the bar with ASCII characters (#, -)
  local fill_str="" empty_str=""
  [[ $filled -gt 0 ]] && fill_str=$(printf '%*s' "$filled" '' | tr ' ' '#')
  [[ $empty -gt 0 ]]  && empty_str=$(printf '%*s' "$empty" '' | tr ' ' '-')

  # \r\033[K = carriage return + erase to end of line (prevents stacking/overflow ghosts)
  printf "\r\033[K  %b[%b%s%b%s%b]%b %b%3d%%%b" \
    "$DIM" "$GREEN" "$fill_str" "$DIM" "$empty_str" "$RESET$DIM" "$RESET" "$BOLD" "$pct" "$RESET"
  # Same set -e footgun as recover_db_port: this is the LAST statement, so an
  # empty label (cond false) would make progress_bar's own return status 1 —
  # every call site invokes it as a bare statement, so that would silently
  # kill the whole installer. `return 0` keeps the return status well-defined.
  if [[ -n "$label" ]]; then
    printf " %b%s%b" "$DIM" "$label" "$RESET"
  fi
  return 0
}

summary_row() {
  local label="$1" value="$2"
  printf "  ${DIM}%-22s${RESET} ${BOLD}%s${RESET}\n" "$label" "$value"
}

# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

generate_password() {
  if check_command openssl; then
    openssl rand -base64 24 | tr -d '/+=' | head -c 32
  else
    head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n' | head -c 32
  fi
}

# Simple alphanumeric password (hex chars only, easy to copy/paste)
generate_admin_password() {
  if check_command openssl; then
    openssl rand -hex 12
  else
    head -c 12 /dev/urandom | od -An -tx1 | tr -d ' \n' | head -c 24
  fi
}

require_root() {
  if [[ "$IS_MACOS" == "true" ]]; then
    # macOS: running as regular user is fine, sudo used when needed
    return 0
  fi
  if [[ $EUID -ne 0 ]]; then
    # Non-root on Linux: check that sudo is available
    if ! command -v sudo &>/dev/null; then
      fatal "This script must be run as root or with sudo available. Try: ${BOLD}sudo bash deploy.sh${RESET}"
    fi
    # Validate sudo access — use "sudo true" instead of "sudo -v" because
    # "sudo -v" prompts for a password even with NOPASSWD rules (it updates
    # the credential timestamp, not a command, so NOPASSWD doesn't apply).
    info "Running as ${BOLD}$RUN_USER${RESET} — sudo will be used for privileged operations."
    if ! sudo true 2>/dev/null; then
      fatal "Could not acquire sudo privileges. Try: ${BOLD}sudo bash deploy.sh${RESET}"
    fi
  fi
}

check_command() {
  command -v "$1" &>/dev/null
}

# ensure_selinux_exec_context PATH
# On SELinux hosts (Fedora/RHEL family), files under $HOME default to the
# user_home_t label, which systemd (running as init_t) is not allowed to
# execute — the denial is `dontaudit`'d by the targeted policy, so nothing
# shows up in `ausearch -m avc` and the service just crash-loops with a bare
# "Permission denied" / status=203/EXEC. Prefer a persistent `semanage
# fcontext` rule (survives a later `restorecon`/`fixfiles onboot`/policy
# relabel) and fall back to a direct, non-persistent `chcon` otherwise.
# `restorecon` alone is a no-op here without a matching fcontext rule first —
# it just reapplies the *existing* (still user_home_t) policy default, which
# is why this only calls restorecon after a successful semanage write, never
# as an independent fallback. `semanage` requires policycoreutils-python-utils,
# which a stock Fedora Cloud image does NOT ship (only plain policycoreutils
# — chcon/restorecon/getenforce — is preinstalled), so the chcon fallback is
# the common case on a fresh install, not an edge case. No-op on non-Linux,
# on hosts without SELinux tooling at all, and when SELinux is Disabled.
ensure_selinux_exec_context() {
  local bin_path="$1"
  [[ "$IS_LINUX" == "true" ]] || return 0
  check_command getenforce || return 0
  [[ "$(getenforce 2>/dev/null)" == "Disabled" ]] && return 0

  if check_command semanage && check_command restorecon; then
    if $SUDO semanage fcontext -a -t bin_t "$bin_path" 2>/dev/null || \
       $SUDO semanage fcontext -m -t bin_t "$bin_path" 2>/dev/null; then
      $SUDO restorecon "$bin_path" 2>/dev/null || true
      return 0
    fi
  fi

  if check_command chcon; then
    $SUDO chcon -t bin_t "$bin_path" 2>/dev/null || \
      warn "Could not set an executable SELinux context on ${BOLD}$bin_path${RESET} — the background service may fail to start under SELinux enforcing. Install ${BOLD}policycoreutils-python-utils${RESET} (for a persistent fix) or move the binary outside \$HOME."
  else
    warn "No chcon/semanage found — could not set an executable SELinux context on ${BOLD}$bin_path${RESET}. The background service may fail to start under SELinux enforcing."
  fi
}

# sudo_notice REASON
# Announce why an upcoming privileged command needs sudo, so the macOS/Linux
# `Password:` prompt is never unexplained. Only prints when sudo will actually
# be used (non-root and sudo's cached credentials may have expired); a no-op
# when running as root ($SUDO is empty).
sudo_notice() {
  local reason="$1"
  [[ -z "$SUDO" ]] && return 0
  # Skip the notice if sudo still has a valid (cached) timestamp — no prompt
  # will appear, so explaining one would be noise.
  sudo -n true 2>/dev/null && return 0
  info "${YELLOW}sudo needed:${RESET} $reason"
}

# Persist a key=value pair to wizard state (for idempotency across re-runs)
state_set() {
  mkdir -p "$STATE_DIR"
  printf '%s' "$2" > "$STATE_DIR/$1"
  chmod 600 "$STATE_DIR/$1"
}

# Read a persisted value (returns empty string if not found)
state_get() {
  local file="$STATE_DIR/$1"
  if [[ -f "$file" ]]; then
    cat "$file"
  fi
}

# Portable way to extract JSON string value (no jq dependency)
# Usage: json_value '{"key":"val"}' "key"
json_value() {
  local json="$1" key="$2"
  echo "$json" | sed -n 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1
}

# Ensure the acme.sh Let's Encrypt account is registered with the given email.
# acme.sh only stores the email at install time, so a stale/bad ACCOUNT_EMAIL
# in ~/.acme.sh/account.conf survives across retries. Always (re-)register the
# account with the current email and, if an account already exists, update it.
# Usage: acme_ensure_account "user@example.com"
acme_ensure_account() {
  local email="$1"
  local acme_bin="$HOME_DIR/.acme.sh/acme.sh"
  local account_conf="$HOME_DIR/.acme.sh/ca/acme-v02.api.letsencrypt.org/directory/account.conf"

  [[ -z "$email" ]] && return 0
  [[ -x "$acme_bin" ]] || return 0

  # Register the account with the current email. This is idempotent: if no
  # account exists yet it creates one; if one exists with the same email it is
  # a no-op. Let's Encrypt rejects an invalid email here, surfacing the real
  # error early instead of hiding it behind a token-extraction failure later.
  if ! "$acme_bin" --register-account -m "$email" --server letsencrypt 2>&1 \
       | while IFS= read -r line; do printf "  ${DIM}  %s${RESET}\n" "$line"; done; then
    return 1
  fi

  # If account.conf still carries a different ACCOUNT_EMAIL (set on a previous
  # run with a bad address), push the corrected email to the existing account.
  if [[ -f "$account_conf" ]] && ! grep -q "ACCOUNT_EMAIL='${email}'" "$account_conf"; then
    "$acme_bin" --update-account -m "$email" --server letsencrypt > /dev/null 2>&1 || true
  fi

  return 0
}

TOTAL_STEPS=5

# Setup mode — chosen on the first screen (or via --mode flag):
#   local    — run on this machine via 127.0.0.1.sslip.io, HTTP only (dogfooding)
#   quick    — sslip.io domain from the public IP. The console and apps get
#              real Let's Encrypt certs automatically via on-demand TLS (ADR-018,
#              HTTP-01) the first time each host is hit — no real domain needed.
#   advanced — your own domain + wildcard Let's Encrypt cert via manual DNS
SETUP_MODE=""

# Release channel for the Temps binary: "stable", "beta" (default), or
# "nightly". CLI-flag-only by design (no env-var fallback), matching `temps
# upgrade --channel` and install.sh:
#   stable  -> GitHub /releases/latest (newest non-prerelease)
#   beta    -> newest tag across /releases (paginated) that is NOT a nightly
#              build (excludes `-nightly.` tags, so beta never silently
#              resolves to an automated nightly)
#   nightly -> newest tag across /releases (paginated) that IS a nightly
#              build (`-nightly.` tag), cut once a day from `main` by CI
CHANNEL="beta"

# Pinned release tag for the Temps binary, e.g. "v0.1.0-beta.30". Empty means
# "newest on $CHANNEL". A pinned version ignores the channel entirely, matching
# install.sh's positional version argument. Set via --version <tag>.
TEMPS_VERSION=""

# Anonymous product telemetry. Temps reports anonymous usage events (e.g.
# "an instance attempted a deploy" vs "an instance deployed successfully") so
# the maintainers can tell whether the product is working for self-hosters.
# It is anonymous by design — no PII, repo names, domains, or secrets — and
# enabled by default (opt-in). Operators can opt out with --no-telemetry, which
# sets TEMPS_TELEMETRY=0 in the service so the binary never reports anything.
TELEMETRY_OPTOUT="false"

# Pre-answered prompt values for scripted/headless installs (set via --domain,
# --email, --yes). --domain pre-fills the advanced-mode domain prompt; --email
# pre-fills the Let's Encrypt contact and admin-login email prompts; --yes
# (alias -y, --non-interactive) accepts every confirmation's DEFAULT answer so
# quick mode can run unattended. Quick + --yes requires --email (ACME needs a
# real contact address and there is no fallback). Advanced mode still needs a
# terminal: manual DNS-01 validation pauses for the operator to add TXT records,
# unless a DNS provider (--dns-provider + credentials) makes it fully automatic.
FLAG_DOMAIN=""
FLAG_EMAIL=""
ASSUME_YES="false"

# Advanced-mode wildcard cert: optional DNS provider for fully-automatic
# DNS-01 validation via acme.sh's native API plugin, instead of the manual
# paste-a-TXT-record flow. Same provider names and env var fallbacks as
# `temps setup --dns-provider` for a consistent credential story across the
# installer and the binary. DNS_API_PLUGIN is the acme.sh plugin name
# ("dns_cf"/"dns_aws"/"dns_dgon") resolved by select_dns_validation_method,
# or "" for the manual flow.
FLAG_DNS_PROVIDER=""
FLAG_CLOUDFLARE_TOKEN="${CLOUDFLARE_API_TOKEN:-}"
FLAG_AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-}"
FLAG_AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-}"
FLAG_AWS_REGION="${AWS_REGION:-us-east-1}"
FLAG_DIGITALOCEAN_TOKEN="${DIGITALOCEAN_API_TOKEN:-}"
DNS_API_PLUGIN=""

# sslip.io wildcard domain for local/quick modes, e.g. "1.2.3.4.sslip.io"
# (or "127.0.0.1.sslip.io" in local mode). The console is reachable at
# console.<SSLIP_DOMAIN>; apps at <app>.<SSLIP_DOMAIN>.
SSLIP_DOMAIN=""
SERVER_IP=""

# HTTP port the proxy binds in local/quick modes. Local mode tries 80
# and falls back to 8080 when binding the privileged port fails (e.g. macOS,
# non-root); when the port is not 80 it is shown in console/app URLs.
LOCAL_PORT=80

# Console/admin API port (`--console-address`). Used for the health probe and
# the management UI. Resolved to a free port by resolve_service_ports so a
# second Temps install (or any other process on :8081) doesn't collide.
CONSOLE_PORT=8081

# resolve_service_ports HTTP_PREF TLS_PREF
# Pick free host ports for the proxy HTTP/TLS listeners and the console API,
# preferring the passed defaults and falling back to the next free port when
# one is taken — the same conflict-avoidance the DB port already uses. The
# chosen values land in LOCAL_PORT / TLS_PORT / CONSOLE_PORT and are persisted
# to wizard state so re-runs stay consistent. A running Temps server (which
# holds 8080/8443/8081) therefore no longer blocks a second install.
TLS_PORT=443
# Space-separated list of ports already claimed in THIS run, so the three
# listeners don't pick the same free port as each other (next_free_port only
# sees OS-bound sockets, not ports we've just decided to use).
_RESOLVED_PORTS=""

# resolve_one_port OUTVAR LABEL PREFERRED FALLBACK_START
# Choose a free port: PREFERRED if free, else scan up from FALLBACK_START.
# "Free" means neither OS-bound nor already claimed this run ($_RESOLVED_PORTS).
# Writes the result to the named OUTVAR and appends it to $_RESOLVED_PORTS in
# the CURRENT shell (no command substitution — a $(...) subshell would lose the
# _RESOLVED_PORTS accumulation and two listeners could pick the same port).
resolve_one_port() {
  local _outvar="$1" label="$2" pref="$3" fallback_start="$4" chosen="$3"
  _port_taken() { port_in_use "$1" || [[ " $_RESOLVED_PORTS " == *" $1 "* ]]; }
  if _port_taken "$pref"; then
    local p chosen_set=false
    for ((p = fallback_start; p < fallback_start + 50; p++)); do
      if ! _port_taken "$p"; then chosen="$p"; chosen_set=true; break; fi
    done
    [[ "$chosen_set" == "true" ]] || fatal "No free port near ${pref} for ${label}"
    warn "Port ${BOLD}${pref}${RESET} (${label}) is in use — using ${BOLD}${chosen}${RESET} instead."
  fi
  _RESOLVED_PORTS+=" $chosen"
  printf -v "$_outvar" '%s' "$chosen"
}

resolve_service_ports() {
  local http_pref="${1:-80}" tls_pref="${2:-443}"
  _RESOLVED_PORTS=""

  # Reuse ports chosen on a previous run when they're still free (or still ours).
  local saved_http saved_tls saved_console
  saved_http="$(state_get http_port)"
  saved_tls="$(state_get tls_port)"
  saved_console="$(state_get console_port)"
  [[ -n "$saved_http" ]] && http_pref="$saved_http"
  [[ -n "$saved_tls" ]] && tls_pref="$saved_tls"
  [[ -n "$saved_console" ]] && CONSOLE_PORT="$saved_console"

  # A taken sub-1024 preference jumps into the 8080/8443 range; otherwise scan up.
  resolve_one_port LOCAL_PORT   "HTTP"    "$http_pref"    "$(( http_pref < 1024 ? 8080 : http_pref + 1 ))"
  resolve_one_port TLS_PORT     "HTTPS"   "$tls_pref"     "$(( tls_pref < 1024 ? 8443 : tls_pref + 1 ))"
  resolve_one_port CONSOLE_PORT "console" "$CONSOLE_PORT" "$(( CONSOLE_PORT + 1 ))"

  state_set http_port "$LOCAL_PORT"
  state_set tls_port "$TLS_PORT"
  state_set console_port "$CONSOLE_PORT"
}

# resolve_channel_version
# Prints the tag name for the newest release on the selected $CHANNEL.
#   stable  -> /releases/latest (GitHub returns the newest non-prerelease)
#   beta    -> /releases, first tag that is NOT a nightly build
#   nightly -> /releases, first tag that IS a nightly build
# Mirrors `temps upgrade`: beta tracks the freshest non-nightly version;
# nightly tracks only automated builds cut from main.
#
# Pagination: nightlies are cut once a day from `main`, so a gap of more
# than one page's worth of days since the last beta release (or, in
# principle, since the last nightly) means the desired tag isn't on page 1.
# Walk up to 5 pages of 100 releases (500 releases of headroom) and stop as
# soon as a match is found or the API runs out of releases.
resolve_channel_version() {
  local ver="" page=1 page_tags
  if [[ "$CHANNEL" == "stable" ]]; then
    ver=$(curl -fsSL "https://api.github.com/repos/gotempsh/temps/releases/latest" 2>/dev/null \
      | grep '"tag_name":' | head -1 | cut -d'"' -f4)
  else
    while [[ -z "$ver" && $page -le 5 ]]; do
      page_tags=$(curl -fsSL "https://api.github.com/repos/gotempsh/temps/releases?per_page=100&page=$page" 2>/dev/null \
        | grep -oE '"tag_name": *"[^"]*"' | cut -d'"' -f4)
      [[ -z "$page_tags" ]] && break

      if [[ "$CHANNEL" == "nightly" ]]; then
        ver=$(echo "$page_tags" | grep -- '-nightly\.' | head -1)
      else
        ver=$(echo "$page_tags" | grep -v -- '-nightly\.' | head -1)
      fi

      page=$((page + 1))
    done
  fi
  echo "$ver"
}

# Docker may need sudo for non-root users not in the docker group.
# DOCKER_SUDO is set after Docker is confirmed working in step_docker().
DOCKER_SUDO=""

# diagnose_setup_failure LOG_FILE
# `temps setup` can fail for several distinct reasons that all surface as a
# nonzero exit code. Match the captured output against known failure classes
# and print the specific fix instead of one generic hint that fits none of
# them well. Falls back to the original generic checklist when nothing matches.
diagnose_setup_failure() {
  local log_file="$1" log_content=""
  [[ -f "$log_file" ]] && log_content=$(cat "$log_file" 2>/dev/null)

  if printf '%s' "$log_content" | grep -qi "connection refused"; then
    info "Troubleshooting (database connection refused):"
    info "  The setup wizard connects via ${BOLD}127.0.0.1:${DB_PORT}${RESET} — if that's"
    info "  refused, the container isn't actually listening there right now."
    info "  1. Confirm it's up:        ${BOLD}docker ps | grep timescale${RESET}"
    info "  2. Check for a crash loop: ${BOLD}docker logs temps-timescaledb --tail 50${RESET}"
    info "  3. Confirm Postgres is ready: ${BOLD}docker exec temps-timescaledb pg_isready -U temps${RESET}"
    info "  4. Test the exact address: ${BOLD}nc -zv 127.0.0.1 ${DB_PORT}${RESET}"
    info "  Once fixed, re-run: ${BOLD}curl -fsSL https://temps.sh/deploy.sh | bash -s -- --channel=${CHANNEL}${RESET}"
  elif printf '%s' "$log_content" | grep -qi "password authentication failed"; then
    info "Troubleshooting (database password mismatch):"
    info "  The temps-db-data volume was initialized with a different password"
    info "  than the one this run generated (common after a prior partial install)."
    info "  Remove the stale volume to start clean (${RED}destroys existing data${RESET}):"
    info "    ${BOLD}docker rm -f temps-timescaledb && docker volume rm temps-db-data${RESET}"
    info "  Then re-run: ${BOLD}curl -fsSL https://temps.sh/deploy.sh | bash -s -- --channel=${CHANNEL}${RESET}"
  elif printf '%s' "$log_content" | grep -qi "exec format error\|cannot execute binary"; then
    info "Troubleshooting (wrong-architecture binary):"
    info "  A previous run left an incompatible binary on disk. Clear it and retry:"
    info "    ${BOLD}rm -rf $HOME_DIR/.temps/bin && curl -fsSL https://temps.sh/deploy.sh | bash -s -- --channel=${CHANNEL}${RESET}"
  else
    info "Troubleshooting:"
    info "  1. Verify database is running:  ${BOLD}docker ps | grep timescale${RESET}"
    info "  2. Check database connectivity: ${BOLD}docker exec temps-timescaledb pg_isready -U temps${RESET}"
    info "  3. Re-run this script to retry: ${BOLD}curl -fsSL https://temps.sh/deploy.sh | bash -s -- --channel=${CHANNEL}${RESET}"
  fi
}

# ---------------------------------------------------------------------------
# Step 1: Docker
# ---------------------------------------------------------------------------

step_docker() {
  step_header 1 $TOTAL_STEPS "Docker Engine"

  # Helper: check if docker daemon is reachable (directly or via sudo)
  docker_is_ready() {
    if docker info &>/dev/null; then
      DOCKER_SUDO=""
      return 0
    elif [[ -n "$SUDO" ]] && $SUDO docker info &>/dev/null; then
      DOCKER_SUDO="$SUDO"
      return 0
    fi
    return 1
  }

  if check_command docker && docker_is_ready; then
    local docker_version
    docker_version=$($DOCKER_SUDO docker --version 2>/dev/null | head -1)
    success "Docker is already installed"
    info "${DIM}$docker_version${RESET}"
    if [[ -n "$DOCKER_SUDO" ]]; then
      info "Using ${BOLD}sudo${RESET} for docker commands"
    fi
    echo ""
    return 0
  fi

  if check_command docker && ! docker_is_ready; then
    warn "Docker is installed but the daemon is not running"
    info "Attempting to start Docker..."
    if [[ "$IS_LINUX" == "true" ]]; then
      $SUDO systemctl start docker 2>/dev/null || true
    elif [[ "$IS_MACOS" == "true" ]]; then
      open -a Docker 2>/dev/null || true
      info "Waiting for Docker Desktop to start..."
      for _i in $(seq 1 30); do
        docker_is_ready && break
        sleep 2
      done
    fi
    sleep 2
    if docker_is_ready; then
      success "Docker daemon started"
      if [[ -n "$DOCKER_SUDO" ]]; then
        info "Using ${BOLD}sudo${RESET} for docker commands"
      fi
      echo ""
      return 0
    fi
  fi

  warn "Docker is not installed"
  echo ""

  if [[ "$IS_MACOS" == "true" ]]; then
    if check_command brew; then
      if ! prompt_yesno "Install Docker via Homebrew?" "y"; then
        fatal "Docker is required. Install Docker Desktop from ${UNDERLINE}https://docker.com/products/docker-desktop${RESET} and re-run."
      fi
      echo ""
      if spinner "Installing Docker via Homebrew" brew install --cask docker; then
        echo ""
        info "Starting Docker Desktop..."
        open -a Docker 2>/dev/null || true
        # Wait for Docker to become ready
        local docker_ready=false
        for _i in $(seq 1 30); do
          if docker_is_ready; then docker_ready=true; break; fi
          sleep 2
        done
        if [[ "$docker_ready" == "true" ]]; then
          success "Docker Desktop installed and running"
          echo ""
        else
          warn "Docker Desktop installed but not yet ready."
          info "Open Docker Desktop manually and re-run the wizard."
          fatal "Docker daemon not responding."
        fi
      else
        fatal "Docker installation failed. Install Docker Desktop manually from ${UNDERLINE}https://docker.com/products/docker-desktop${RESET}"
      fi
    else
      fatal "Docker is required. Install Docker Desktop from ${UNDERLINE}https://docker.com/products/docker-desktop${RESET} and re-run."
    fi
  else
    if ! prompt_yesno "Install Docker now?" "y"; then
      fatal "Docker is required to continue. Install it manually and re-run the wizard."
    fi

    echo ""
    info "Installing Docker via ${UNDERLINE}https://get.docker.com${RESET}..."
    sudo_notice "to install the Docker Engine system-wide"
    echo ""

    if spinner "Downloading and installing Docker" bash -c "curl -fsSL https://get.docker.com | $SUDO sh"; then
      echo ""
      # Add current user to docker group so subsequent runs don't need sudo for docker
      if [[ -n "$SUDO" ]] && [[ "$IS_LINUX" == "true" ]]; then
        $SUDO usermod -aG docker "$RUN_USER" 2>/dev/null || true
        info "Added ${BOLD}$RUN_USER${RESET} to docker group (takes effect on next login)"
      fi

      # Enable and start Docker
      $SUDO systemctl enable docker &>/dev/null || true
      $SUDO systemctl start docker &>/dev/null || true
      sleep 2

      if docker_is_ready; then
        local docker_version
        docker_version=$($DOCKER_SUDO docker --version 2>/dev/null | head -1)
        success "Docker installed and running"
        info "${DIM}$docker_version${RESET}"
        if [[ -n "$DOCKER_SUDO" ]]; then
          info "Using ${BOLD}sudo${RESET} for docker commands"
        fi
        echo ""
      else
        fatal "Docker installed but failed to start. Check: ${BOLD}${SUDO:+sudo }systemctl status docker${RESET}"
      fi
    else
      fatal "Docker installation failed. Check /tmp/temps-wizard-cmd-out.log for details."
    fi
  fi
}

# ---------------------------------------------------------------------------
# Step 2: TimescaleDB
# ---------------------------------------------------------------------------

DB_PASSWORD=""
# Host port the TimescaleDB container publishes on. Defaults to 5432, but if
# 5432 is already taken by another process (e.g. a host PostgreSQL or another
# Temps install) we fall back to the next free port so the install still
# succeeds. Recovered from wizard state on re-run; threaded into every
# connection string and `temps setup`.
DB_PORT="5432"

# reconcile_db_password
# Ensure the `temps` role's password inside the container matches $DB_PASSWORD.
# Needed because Postgres ignores POSTGRES_PASSWORD when the data volume already
# exists, so a reused volume keeps its OLD password — the deploy → undeploy →
# deploy cycle hits this every time (undeploy keeps the volume, deploy generates
# a fresh password the volume never adopts).
#
# Strategy: ALWAYS ALTER the role over the container's LOCAL socket, then verify
# the result over a path that genuinely exercises scram/md5.
#
# We do NOT short-circuit on "does the password already work?" because every
# probe we can run from inside the container connects via 127.0.0.1 or the unix
# socket, which match the `trust` lines in pg_hba.conf and succeed REGARDLESS of
# the password — so such a probe can never detect (let alone fix) a mismatch.
# `temps serve` runs on the host and reaches Postgres through the published port,
# which arrives from the Docker bridge gateway IP and falls through to the
# `scram-sha-256` rule, so it is the only connection that truly checks the
# password. Unconditionally resetting the role is idempotent and always correct.
#
# Returns 0 on success, 1 if the password still doesn't authenticate over a
# password-checked path.
reconcile_db_password() {
  local escaped="${DB_PASSWORD//\'/\'\'}"
  local attempt
  # The timescaledb-ha image restarts Postgres once during first init, so a
  # command can transiently hit "system is shutting down / starting up" or a
  # refused socket — retry across that window before giving up.
  for attempt in $(seq 1 30); do
    if $DOCKER_SUDO docker exec temps-timescaledb \
         psql -U temps -d temps -v ON_ERROR_STOP=1 \
         -c "ALTER USER temps WITH PASSWORD '${escaped}';" &>/dev/null; then
      # Verify over a connection that actually checks the password. Connecting
      # to the container's published host port (DB_PORT → 5432) arrives from the
      # bridge gateway, matching the scram-sha-256 hba rule — exactly the path
      # `temps serve` uses. Fall back to an in-container probe only if the host
      # has no psql; the in-container probe is trust-gated and merely confirms
      # the server is reachable, but the ALTER above is what makes it correct.
      if command -v psql &>/dev/null; then
        if PGPASSWORD="$DB_PASSWORD" psql -h 127.0.0.1 -p "$DB_PORT" \
             -U temps -d temps -tAc 'SELECT 1' &>/dev/null; then
          return 0
        fi
      else
        # No host psql: trust the ALTER succeeded. Confirm the server answers.
        if $DOCKER_SUDO docker exec temps-timescaledb \
             pg_isready -U temps &>/dev/null; then
          return 0
        fi
      fi
    fi
    sleep 1
  done
  return 1
}

# db_has_admin_user
# Returns 0 if the temps database already contains at least one user, 1 if it is
# empty (or unreachable). Used to decide whether `temps setup` still needs to
# seed the admin account.
#
# Why this matters: the deploy → undeploy → deploy cycle decouples two pieces of
# state that the idempotency guard used to conflate. The encryption key lives in
# the HOST data dir ($HOME_DIR/.temps/data), but the admin USER lives in the
# Postgres VOLUME (temps-db-data). If the volume is reset (fresh DB, 0 users)
# while the host data dir survives, the old "encryption_key exists ⇒ already
# configured" check skips seeding — then `temps serve` finds no users, drops
# into an interactive admin-email prompt, and dies under launchd/systemd (no
# TTY). Checking the actual user table closes that gap.
#
# Queries over the container's local socket (trusted in these images), so it
# does not depend on the host password being reconciled yet.
db_has_admin_user() {
  $DOCKER_SUDO docker ps --format '{{.Names}}' 2>/dev/null \
    | grep -q '^temps-timescaledb$' || return 1
  local count
  count=$($DOCKER_SUDO docker exec temps-timescaledb \
    psql -U temps -d temps -h /var/run/postgresql -tAc \
    'SELECT count(*) FROM users' 2>/dev/null | tr -d '[:space:]')
  # Empty/non-numeric (table missing, query failed) ⇒ treat as "no admin" so we
  # run the full seeding setup rather than silently skipping it.
  [[ "$count" =~ ^[0-9]+$ ]] && [[ "$count" -gt 0 ]]
}

# recover_db_port
# Resolve the DB host port for an EXISTING container: prefer the value saved in
# wizard state, fall back to the container's actual published port, then 5432.
# Persists the result so later steps and re-runs stay consistent.
recover_db_port() {
  DB_PORT="$(state_get db_port)"
  if [[ -z "$DB_PORT" ]]; then
    DB_PORT="$(container_db_host_port temps-timescaledb)"
  fi
  [[ -z "$DB_PORT" ]] && DB_PORT="5432"
  state_set db_port "$DB_PORT"
  # `[[ cond ]] && cmd` as the LAST statement of a function makes the
  # function's own return status track `cond` — under `set -e`, calling this
  # function as a bare statement (as step_timescaledb does) then silently
  # kills the whole script whenever DB_PORT is the default "5432", since
  # `cond` is false and nothing prints. `return 0` pins the real return value.
  if [[ "$DB_PORT" != "5432" ]]; then
    info "Database port: ${BOLD}${DB_PORT}${RESET}"
  fi
  return 0
}

step_timescaledb() {
  step_header 2 $TOTAL_STEPS "TimescaleDB Database"

  # Check if container already exists and is running
  if $DOCKER_SUDO docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^temps-timescaledb$'; then
    if $DOCKER_SUDO docker exec temps-timescaledb pg_isready -U temps &>/dev/null; then
      success "TimescaleDB is already running"
      info "Container: ${BOLD}temps-timescaledb${RESET}"
      echo ""

      # Recover the published host port: wizard state first, then the running
      # container's actual port mapping, then default to 5432.
      recover_db_port

      # Recover password from wizard state first, then from docker inspect
      DB_PASSWORD=$(state_get db_password)
      if [[ -z "$DB_PASSWORD" ]]; then
        # Try docker inspect: look for POSTGRES_PASSWORD env var
        DB_PASSWORD=$($DOCKER_SUDO docker inspect temps-timescaledb 2>/dev/null \
          | sed -n 's/.*"POSTGRES_PASSWORD=\([^"]*\)".*/\1/p' | head -1 || true)
      fi

      if [[ -z "$DB_PASSWORD" ]]; then
        warn "Could not recover existing database password — generating a new one"
        DB_PASSWORD=$(generate_password)
      fi
      # The recovered/generated password may not match what's actually in the
      # data volume; force it to match so `temps setup` can authenticate.
      if ! reconcile_db_password; then
        fatal "Could not reconcile the database password on the running container"
      fi
      state_set db_password "$DB_PASSWORD"
      return 0
    fi
  fi

  # Check if container exists but is stopped
  if $DOCKER_SUDO docker ps -a --format '{{.Names}}' 2>/dev/null | grep -q '^temps-timescaledb$'; then
    warn "TimescaleDB container exists but is stopped"
    info "Starting existing container..."
    $DOCKER_SUDO docker start temps-timescaledb &>/dev/null

    sleep 3
    if $DOCKER_SUDO docker exec temps-timescaledb pg_isready -U temps &>/dev/null; then
      success "TimescaleDB container restarted"
      echo ""
      recover_db_port
      DB_PASSWORD=$(state_get db_password)
      if [[ -z "$DB_PASSWORD" ]]; then
        DB_PASSWORD=$($DOCKER_SUDO docker inspect temps-timescaledb 2>/dev/null \
          | sed -n 's/.*"POSTGRES_PASSWORD=\([^"]*\)".*/\1/p' | head -1 || true)
      fi
      if [[ -z "$DB_PASSWORD" ]]; then
        warn "Could not recover existing database password — generating a new one"
        DB_PASSWORD=$(generate_password)
      fi
      if ! reconcile_db_password; then
        fatal "Could not reconcile the database password on the restarted container"
      fi
      state_set db_password "$DB_PASSWORD"
      return 0
    fi
  fi

  # Fresh install. Reuse a port chosen on a previous run if we have one.
  DB_PORT="$(state_get db_port)"
  [[ -z "$DB_PORT" ]] && DB_PORT="5432"

  # 5432 being busy is NOT fatal — it may be a host PostgreSQL or another Temps
  # instance, which we must not disturb. Bind our container to the next free
  # port instead, and thread that port through every connection string below.
  if port_in_use "$DB_PORT"; then
    local holder
    holder="$(port_holder "$DB_PORT")"
    warn "Port ${BOLD}${DB_PORT}${RESET} is already in use — likely another PostgreSQL or Temps instance."
    if [[ -n "$holder" ]]; then
      info "Currently listening on ${DB_PORT}:"
      printf "%b\n" "$holder"
    fi
    local fallback
    if ! fallback="$(next_free_port 5433)"; then
      error "Could not find a free port in the range 5433–5452."
      info "Free a port (e.g. stop the conflicting service) and re-run the installer."
      fatal "Cannot continue without a free host port for the database"
    fi
    DB_PORT="$fallback"
    info "Using ${BOLD}${DB_PORT}${RESET} for the Temps database instead."
  fi
  state_set db_port "$DB_PORT"

  info "Pulling ${BOLD}timescale/timescaledb-ha:pg18${RESET}..."

  DB_PASSWORD=$(generate_password)
  state_set db_password "$DB_PASSWORD"

  spinner "Pulling TimescaleDB image" $DOCKER_SUDO docker pull timescale/timescaledb-ha:pg18 || \
    fatal "Failed to pull TimescaleDB image"
  echo ""

  info "Starting TimescaleDB container..."
  echo ""

  # Capture stderr so a failure (e.g. port bind, missing image) surfaces the
  # real reason instead of silently falling through into the readiness loop.
  local run_err
  if ! run_err=$($DOCKER_SUDO docker run -d \
    --name temps-timescaledb \
    --restart unless-stopped \
    --shm-size=2g \
    -e POSTGRES_USER=temps \
    -e POSTGRES_PASSWORD="$DB_PASSWORD" \
    -e POSTGRES_DB=temps \
    -p 127.0.0.1:"$DB_PORT":5432 \
    -v temps-db-data:/home/postgres/pgdata/data \
    timescale/timescaledb-ha:pg18 2>&1); then
    echo ""
    error "Failed to start the TimescaleDB container."
    info "Docker reported:"
    printf "    ${DIM}%b${RESET}\n" "$run_err"
    if printf '%s' "$run_err" | grep -qiE "address already in use|port is already allocated|bind"; then
      info "Port ${BOLD}${DB_PORT}${RESET} could not be bound — another process took it"
      info "between our check and container start. Re-run the installer to pick"
      info "a different port."
    fi
    fatal "Cannot continue without a working database"
  fi

  # Wait for database readiness
  local ready=false
  for i in $(seq 1 30); do
    progress_bar "$i" 30 "Waiting for database..."
    if $DOCKER_SUDO docker exec temps-timescaledb pg_isready -U temps &>/dev/null; then
      ready=true
      break
    fi
    sleep 1
  done
  progress_bar 30 30 "Waiting for database..."
  echo ""

  if [[ "$ready" == "true" ]]; then
    # Postgres only applies POSTGRES_PASSWORD when it initializes an EMPTY data
    # dir. If the temps-db-data volume already existed (e.g. a prior install),
    # the container keeps the OLD password and silently ignores the new env var
    # — so the freshly generated DB_PASSWORD we hand to `temps setup` would fail
    # with "password authentication failed". Force the role password now over
    # the container's local socket (trusted) so the DB always matches our state.
    if ! reconcile_db_password; then
      echo ""
      error "Could not set the database password on the temps role."
      info "The data volume ${BOLD}temps-db-data${RESET} may hold a database whose"
      info "password we cannot reset automatically. Inspect with:"
      info "  ${BOLD}docker exec -it temps-timescaledb psql -U temps -d temps${RESET}"
      info "or remove the stale volume to start clean (DESTROYS existing data):"
      info "  ${BOLD}docker rm -f temps-timescaledb && docker volume rm temps-db-data${RESET}"
      fatal "Cannot continue with a mismatched database password"
    fi

    success "TimescaleDB is ready"
    info "Container: ${BOLD}temps-timescaledb${RESET}"
    info "Port:      ${BOLD}127.0.0.1:${DB_PORT}${RESET}"
    info "User:      ${BOLD}temps${RESET}"
    info "Database:  ${BOLD}temps${RESET}"
    info "Password:  ${DIM}(auto-generated, stored securely)${RESET}"
    echo ""
  else
    echo ""
    warn "TimescaleDB failed to become ready within 30 seconds."
    info "Troubleshooting steps:"
    info "  1. Check Docker is running:  ${BOLD}docker ps${RESET}"
    info "  2. Check container logs:     ${BOLD}docker logs temps-timescaledb${RESET}"
    info "  3. Check available disk:     ${BOLD}df -h${RESET}"
    info "  4. Restart and retry:        ${BOLD}docker restart temps-timescaledb${RESET}"
    fatal "Cannot continue without a working database"
  fi
}

# ---------------------------------------------------------------------------
# Step 3: Domain & SSL Certificate
# ---------------------------------------------------------------------------

DOMAIN=""
WILDCARD_DOMAIN=""
CERT_DIR="$HOME_DIR/.temps/certs"
FULLCHAIN_PATH=""
KEY_PATH=""

# Optional ClickHouse backend for proxy logs, analytics, and traces (advanced
# mode only). When enabled, the four TEMPS_CLICKHOUSE_* env vars are injected
# into the service so `temps serve` activates the ClickHouse storage backends
# automatically (no settings change needed). Resource metrics stay on
# TimescaleDB — that path additionally gates on `monitoring.store`, which this
# installer does not set. Empty CLICKHOUSE_URL means "not enabled".
CLICKHOUSE_ENABLED="false"
CLICKHOUSE_URL=""
CLICKHOUSE_DATABASE=""
CLICKHOUSE_USER=""
CLICKHOUSE_PASSWORD=""

step_domain_ssl() {
  step_header 3 $TOTAL_STEPS "Domain & SSL Certificate"

  # Idempotency: check if valid certs already exist
  FULLCHAIN_PATH="$CERT_DIR/fullchain.pem"
  KEY_PATH="$CERT_DIR/key.pem"
  DOMAIN=$(state_get domain)

  if [[ -n "$DOMAIN" ]] \
    && [[ -f "$FULLCHAIN_PATH" ]] \
    && [[ -f "$KEY_PATH" ]] \
    && openssl x509 -in "$FULLCHAIN_PATH" -noout -checkend 86400 &>/dev/null; then
    WILDCARD_DOMAIN="*.$DOMAIN"
    success "SSL certificate already provisioned and valid"
    info "Domain:    ${BOLD}$DOMAIN${RESET}"
    info "Wildcard:  ${BOLD}$WILDCARD_DOMAIN${RESET}"
    echo ""

    local cert_exp
    cert_exp=$(openssl x509 -in "$FULLCHAIN_PATH" -noout -enddate 2>/dev/null | sed 's/.*=//' || true)
    info "Expires:   ${BOLD}$cert_exp${RESET}"

    if ! prompt_yesno "Re-provision certificate?" "n"; then
      return 0
    fi
  fi

  # Reset for fresh provisioning
  DOMAIN=""
  WILDCARD_DOMAIN=""

  # Self-hosted setup uses your own domain with a wildcard Let's Encrypt
  # certificate, validated by adding DNS TXT records yourself.
  domain_manual

  # Persist domain for idempotency
  state_set domain "$DOMAIN"
}

domain_manual() {
  echo ""
  info "We'll use ${BOLD}acme.sh${RESET} to provision a wildcard Let's Encrypt"
  info "certificate for your domain via DNS-01 validation."
  echo ""
  info "${DIM}You'll need:${RESET}"
  info "  1. A domain you own"
  info "  2. Either a Cloudflare/Route53/DigitalOcean API token (fully"
  info "     automatic), or access to your DNS provider to add a TXT record"
  info "     by hand"
  echo ""

  if [[ -n "$FLAG_DOMAIN" ]]; then
    DOMAIN="$FLAG_DOMAIN"
    info "Using domain from ${BOLD}--domain${RESET}: ${BOLD}$DOMAIN${RESET}"
  else
    prompt_input "Your domain (e.g. example.com)" "" DOMAIN
  fi

  if [[ -z "$DOMAIN" ]]; then
    fatal "Domain is required"
  fi

  WILDCARD_DOMAIN="*.$DOMAIN"

  local admin_email="$FLAG_EMAIL"
  if [[ -n "$admin_email" ]]; then
    info "Using Let's Encrypt email from ${BOLD}--email${RESET}: ${BOLD}$admin_email${RESET}"
  else
    prompt_input "Email for Let's Encrypt notifications" "" admin_email
  fi

  if [[ -z "$admin_email" ]]; then
    fatal "Email is required for Let's Encrypt"
  fi

  echo ""
  info "Provisioning wildcard certificate for ${BOLD}$DOMAIN${RESET}..."
  echo ""

  # Install acme.sh if not present
  if [[ ! -f $HOME_DIR/.acme.sh/acme.sh ]]; then
    spinner "Installing acme.sh" bash -c \
      "curl -fsSL https://get.acme.sh | sh -s email='$admin_email'" || \
      fatal "Failed to install acme.sh"
  else
    success "acme.sh already installed"
  fi

  # Set default CA
  $HOME_DIR/.acme.sh/acme.sh --set-default-ca --server letsencrypt > /dev/null 2>&1 || true

  # Register/refresh the Let's Encrypt account with the email entered above.
  # acme.sh keeps the email from its first install, so without this an invalid
  # address from an earlier attempt would persist and block issuance.
  info "Registering ACME account (${BOLD}$admin_email${RESET})..."
  acme_ensure_account "$admin_email" || \
    fatal "ACME account registration failed. Verify the email address is valid."

  mkdir -p "$CERT_DIR"

  select_dns_validation_method
  if [[ -n "$DNS_API_PLUGIN" ]]; then
    provision_cert_via_dns_api "$DNS_API_PLUGIN"
  else
    provision_cert_manual_dns
  fi

  install_acme_cert
}

# Decide how to satisfy the wildcard certificate's DNS-01 challenge: fully
# automatic via a DNS provider's API (acme.sh's native plugin creates and
# removes the TXT record itself — no copy/paste, no propagation wait), or the
# original manual flow where the operator pastes a TXT record by hand. Sets
# the global DNS_API_PLUGIN to the acme.sh plugin name ("dns_cf", "dns_aws",
# "dns_dgon") when automatic, or "" for manual — and exports that plugin's
# credential env vars as a side effect. Never call this inside $(...): it
# calls prompt_choice/prompt_input, which print menus straight to stdout.
select_dns_validation_method() {
  DNS_API_PLUGIN=""
  local provider="$FLAG_DNS_PROVIDER"

  if [[ -z "$provider" ]]; then
    # No provider given via --dns-provider. With --yes there's no terminal to
    # ask, so fall through silently to the manual path — it has its own clear
    # fatal() explaining exactly which flags to add for a headless run.
    [[ "$ASSUME_YES" == "true" ]] && return 0

    local method_choice=""
    prompt_choice method_choice "How should we validate domain ownership for the wildcard certificate?" "" \
      "Automatic — provision via my DNS provider's API (Cloudflare, Route53, or DigitalOcean)" \
      "Manual     — I'll add the TXT record(s) myself"
    [[ "$method_choice" != "1" ]] && return 0

    local provider_choice=""
    prompt_choice provider_choice "Which DNS provider?" "" \
      "Cloudflare" "AWS Route53" "DigitalOcean"
    case "$provider_choice" in
      1) provider="cloudflare" ;;
      2) provider="route53" ;;
      3) provider="digitalocean" ;;
      *) fatal "Invalid choice" ;;
    esac
  fi

  case "$provider" in
    cloudflare)
      if [[ -z "$FLAG_CLOUDFLARE_TOKEN" ]]; then
        [[ "$ASSUME_YES" == "true" ]] && \
          fatal "--cloudflare-token (or CLOUDFLARE_API_TOKEN) is required for --dns-provider cloudflare with --yes."
        prompt_input "Cloudflare API token (Zone:DNS:Edit permission)" "" FLAG_CLOUDFLARE_TOKEN
      fi
      [[ -z "$FLAG_CLOUDFLARE_TOKEN" ]] && fatal "A Cloudflare API token is required for automatic DNS-01 validation."
      export CF_Token="$FLAG_CLOUDFLARE_TOKEN"
      DNS_API_PLUGIN="dns_cf"
      ;;
    route53)
      if [[ -z "$FLAG_AWS_ACCESS_KEY_ID" || -z "$FLAG_AWS_SECRET_ACCESS_KEY" ]]; then
        [[ "$ASSUME_YES" == "true" ]] && \
          fatal "--aws-access-key-id and --aws-secret-access-key (or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY) are required for --dns-provider route53 with --yes."
        [[ -z "$FLAG_AWS_ACCESS_KEY_ID" ]] && prompt_input "AWS access key ID" "" FLAG_AWS_ACCESS_KEY_ID
        [[ -z "$FLAG_AWS_SECRET_ACCESS_KEY" ]] && prompt_secret "AWS secret access key" FLAG_AWS_SECRET_ACCESS_KEY
      fi
      if [[ -z "$FLAG_AWS_ACCESS_KEY_ID" || -z "$FLAG_AWS_SECRET_ACCESS_KEY" ]]; then
        fatal "AWS access key ID and secret access key are required for automatic DNS-01 validation via Route53."
      fi
      export AWS_ACCESS_KEY_ID="$FLAG_AWS_ACCESS_KEY_ID"
      export AWS_SECRET_ACCESS_KEY="$FLAG_AWS_SECRET_ACCESS_KEY"
      export AWS_DEFAULT_REGION="$FLAG_AWS_REGION"
      DNS_API_PLUGIN="dns_aws"
      ;;
    digitalocean)
      if [[ -z "$FLAG_DIGITALOCEAN_TOKEN" ]]; then
        [[ "$ASSUME_YES" == "true" ]] && \
          fatal "--digitalocean-token (or DIGITALOCEAN_API_TOKEN) is required for --dns-provider digitalocean with --yes."
        prompt_input "DigitalOcean API token" "" FLAG_DIGITALOCEAN_TOKEN
      fi
      [[ -z "$FLAG_DIGITALOCEAN_TOKEN" ]] && fatal "A DigitalOcean API token is required for automatic DNS-01 validation."
      export DO_API_KEY="$FLAG_DIGITALOCEAN_TOKEN"
      DNS_API_PLUGIN="dns_dgon"
      ;;
    *)
      fatal "Invalid --dns-provider '$provider'. Valid providers: cloudflare, route53, digitalocean"
      ;;
  esac
}

# Fully automatic DNS-01: acme.sh's DNS plugin creates, verifies, and removes
# the TXT record itself via the provider's API (credentials already exported
# by select_dns_validation_method), so none of provision_cert_manual_dns's
# copy/paste/press-enter/propagation-poll UX applies. Falls back to the
# manual flow on repeated failure when a terminal is available.
provision_cert_via_dns_api() {
  local plugin="$1"
  info "Requesting and validating the wildcard certificate via ${BOLD}${plugin#dns_}${RESET} (fully automatic)..."
  echo ""

  local attempt=0 max_attempts=3
  while true; do
    attempt=$((attempt + 1))
    local acme_output acme_exit=0
    acme_output=$($HOME_DIR/.acme.sh/acme.sh --issue \
      -d "$DOMAIN" \
      -d "$WILDCARD_DOMAIN" \
      --dns "$plugin" \
      --force 2>&1) || acme_exit=$?

    while IFS= read -r line; do
      printf "  ${DIM}  %s${RESET}\n" "$line"
    done <<< "$acme_output"

    local acme_cert_dir="$HOME_DIR/.acme.sh/${DOMAIN}_ecc"
    [[ ! -f "$acme_cert_dir/fullchain.cer" ]] && acme_cert_dir="$HOME_DIR/.acme.sh/${DOMAIN}"

    if [[ -f "$acme_cert_dir/fullchain.cer" ]]; then
      echo ""
      success "Certificate issued by Let's Encrypt via ${plugin#dns_} DNS-01"
      echo ""
      return 0
    fi

    echo ""
    if [[ $attempt -ge $max_attempts ]]; then
      error "Automatic DNS-01 validation failed after $max_attempts attempt(s) (acme.sh exit $acme_exit)."
      info "Check that the API credentials are valid and have DNS-edit permission for ${BOLD}$DOMAIN${RESET}."
      if [[ "$ASSUME_YES" == "true" ]]; then
        fatal "Cannot proceed without a certificate."
      fi
      if prompt_yesno "Fall back to manual DNS-01 (paste a TXT record yourself)?" "y"; then
        provision_cert_manual_dns
        return 0
      fi
      fatal "Cannot proceed without a certificate."
    fi
    warn "Attempt $attempt of $max_attempts failed — retrying in 10s..."
    sleep 10
  done
}

# Original manual DNS-01 flow: create an ACME order, show the operator the
# TXT record(s) to paste into their DNS provider by hand, wait, poll for
# propagation, then validate. Used when no DNS provider API credentials are
# available (select_dns_validation_method left DNS_API_PLUGIN empty), or as
# the fallback when provision_cert_via_dns_api gives up.
provision_cert_manual_dns() {
  # --- Retry loop: create ACME order, show TXT records, validate ---
  local attempt=0
  local max_attempts=5

  while true; do
    attempt=$((attempt + 1))

    if [[ $attempt -gt $max_attempts ]]; then
      fatal "Maximum attempts ($max_attempts) reached. Please verify your DNS setup and try again."
    fi

    if [[ $attempt -gt 1 ]]; then
      echo ""
      warn "Attempt $attempt of $max_attempts"
      echo ""
    fi

    # Step 1: Request ACME challenge tokens (manual DNS mode)
    info "Requesting ACME challenge tokens..."

    local acme_output
    acme_output=$($HOME_DIR/.acme.sh/acme.sh --issue \
      -d "$DOMAIN" \
      -d "$WILDCARD_DOMAIN" \
      --dns \
      --yes-I-know-dns-manual-mode-enough-go-ahead-please \
      --force 2>&1 || true)

    # Extract TXT record name and values from acme.sh output
    local txt_name="_acme-challenge.$DOMAIN"
    local tokens=()
    while IFS= read -r line; do
      local tkn
      tkn=$(echo "$line" | sed -n "s/.*TXT value: *'\([^']*\)'.*/\1/p")
      if [[ -n "$tkn" ]]; then
        tokens+=("$tkn")
      fi
    done <<< "$acme_output"

    if [[ ${#tokens[@]} -eq 0 ]]; then
      error "Failed to extract ACME challenge tokens from acme.sh output"
      echo ""
      info "${DIM}acme.sh output:${RESET}"
      while IFS= read -r line; do
        printf "  ${DIM}  %s${RESET}\n" "$line"
      done <<< "$acme_output"
      echo ""
      if prompt_yesno "Retry with a new order?" "y"; then
        continue
      else
        fatal "Cannot proceed without ACME challenge tokens."
      fi
    fi

    success "Got ${#tokens[@]} ACME challenge token(s)"
    echo ""

    # Step 2: Display the TXT records the user needs to add
    hr
    printf "\n"
    printf "  ${BOLD}${YELLOW}ACTION REQUIRED:${RESET} ${BOLD}Add the following DNS TXT record(s)${RESET}\n"
    printf "\n"
    printf "  Go to your DNS provider and create these TXT records:\n"
    printf "\n"

    local token_idx=0
    for tkn in "${tokens[@]}"; do
      token_idx=$((token_idx + 1))
      if [[ ${#tokens[@]} -gt 1 ]]; then
        printf "  ${CYAN}Record %d:${RESET}\n" "$token_idx"
      fi
      printf "    ${DIM}Name:${RESET}   ${BOLD}%s${RESET}\n" "$txt_name"
      printf "    ${DIM}Type:${RESET}   ${BOLD}TXT${RESET}\n"
      printf "    ${DIM}Value:${RESET}  ${BOLD}%s${RESET}\n" "$tkn"
      printf "\n"
    done

    if [[ ${#tokens[@]} -gt 1 ]]; then
      info "${DIM}Both records use the same name — add them as separate TXT entries.${RESET}"
      echo ""
    fi

    info "${DIM}Tip: Set TTL to the lowest value your provider allows (e.g. 60s or 1 min).${RESET}"
    printf "\n"
    hr
    echo ""

    # Step 3: Wait for user confirmation. This pause is the point of manual
    # DNS-01 — a human has to add the TXT records — so it cannot be skipped.
    if [[ "$ASSUME_YES" == "true" ]]; then
      fatal "Manual DNS-01 validation needs a terminal to pause while you add TXT records — run advanced mode without --yes (over SSH: ssh -t)."
    fi
    require_tty "Press Enter after you've added the TXT record(s)"
    printf "  ${ARROW} ${BOLD}Press Enter after you've added the TXT record(s)${RESET}..."
    read -r < /dev/tty
    echo ""

    # Step 4: Verify DNS propagation
    info "Checking DNS propagation (this may take up to 2 minutes)..."
    echo ""

    local propagated=false
    for i in $(seq 1 24); do
      progress_bar "$i" 24 "Checking DNS..."

      # Query Google DoH for TXT records
      local dns_answer
      dns_answer=$(curl -sf "https://dns.google/resolve?name=${txt_name}&type=TXT" 2>/dev/null || true)

      if [[ -n "$dns_answer" ]]; then
        local all_found=true
        for tkn in "${tokens[@]}"; do
          if ! echo "$dns_answer" | grep -q "$tkn"; then
            all_found=false
            break
          fi
        done
        if [[ "$all_found" == "true" ]]; then
          propagated=true
          break
        fi
      fi
      sleep 5
    done
    progress_bar 24 24 "Checking DNS..."
    echo ""
    echo ""

    if [[ "$propagated" == "true" ]]; then
      success "DNS records verified"
      echo ""
    else
      warn "DNS records not yet visible via Google DNS."
      info "This doesn't necessarily mean they're wrong — propagation can be slow."
      echo ""
      local dns_action=""
      prompt_choice dns_action "What would you like to do?" "" \
        "Continue anyway  — attempt ACME validation now" \
        "Wait & recheck   — give DNS more time to propagate" \
        "Start over       — create a new ACME order with fresh tokens" \
        "Abort            — exit the wizard"

      case "$dns_action" in
        1) info "Proceeding with ACME validation..." ;;
        2)
          echo ""
          info "Waiting an additional 60 seconds..."
          for i in $(seq 1 12); do
            progress_bar "$i" 12 "Waiting..."
            sleep 5
          done
          progress_bar 12 12 "Waiting..."
          echo ""
          echo ""
          info "Proceeding with ACME validation..."
          ;;
        3) continue ;;
        4) fatal "Aborted by user." ;;
        *) fatal "Invalid choice" ;;
      esac
      echo ""
    fi

    # Step 5: Complete the ACME challenge (renew to validate)
    info "Completing ACME validation..."
    echo ""

    local renew_output renew_exit=0
    renew_output=$($HOME_DIR/.acme.sh/acme.sh --renew \
      -d "$DOMAIN" \
      -d "$WILDCARD_DOMAIN" \
      --yes-I-know-dns-manual-mode-enough-go-ahead-please \
      2>&1) || renew_exit=$?

    # Show acme.sh output
    while IFS= read -r line; do
      printf "  ${DIM}  %s${RESET}\n" "$line"
    done <<< "$renew_output"

    # Check if cert was actually issued
    local acme_cert_dir="$HOME_DIR/.acme.sh/${DOMAIN}_ecc"
    if [[ ! -f "$acme_cert_dir/fullchain.cer" ]]; then
      acme_cert_dir="$HOME_DIR/.acme.sh/${DOMAIN}"
    fi

    if [[ -f "$acme_cert_dir/fullchain.cer" ]]; then
      success "Certificate issued by Let's Encrypt"
      echo ""
      break
    fi

    # Validation failed
    echo ""
    error "ACME validation failed."
    info "This usually means the TXT records were not found by Let's Encrypt."
    echo ""
    info "${DIM}Common causes:${RESET}"
    info "  1. DNS propagation hasn't completed yet"
    info "  2. TXT record values were entered incorrectly"
    info "  3. Wrong DNS zone (e.g. adding to a subdomain's zone instead of root)"
    echo ""

    local retry_action=""
    prompt_choice retry_action "What would you like to do?" "" \
      "Retry with new tokens  — create a fresh ACME order (recommended)" \
      "Abort                  — exit the wizard"

    case "$retry_action" in
      1)
        info "Creating a new ACME order..."
        info "${DIM}Please remove the old TXT records before adding new ones.${RESET}"
        echo ""
        require_tty "Press Enter when you've removed the old TXT records"
        printf "  ${ARROW} ${BOLD}Press Enter when you've removed the old TXT records${RESET}..."
        read -r < /dev/tty
        continue
        ;;
      2) fatal "Aborted by user." ;;
      *) fatal "Invalid choice" ;;
    esac
  done
}

# Install the issued certificate into $CERT_DIR and remind the operator about
# DNS A records. Shared tail for both provision_cert_via_dns_api and
# provision_cert_manual_dns.
install_acme_cert() {
  echo ""
  $HOME_DIR/.acme.sh/acme.sh --install-cert \
    -d "$DOMAIN" \
    -d "$WILDCARD_DOMAIN" \
    --ecc \
    --cert-file "$CERT_DIR/cert.pem" \
    --key-file "$CERT_DIR/key.pem" \
    --fullchain-file "$CERT_DIR/fullchain.pem" \
    > /dev/null 2>&1 || {
      # Fallback: copy directly
      local acme_cert_dir="$HOME_DIR/.acme.sh/${DOMAIN}_ecc"
      if [[ ! -d "$acme_cert_dir" ]]; then
        acme_cert_dir="$HOME_DIR/.acme.sh/${DOMAIN}"
      fi
      cp "$acme_cert_dir/fullchain.cer" "$CERT_DIR/fullchain.pem"
      cp "$acme_cert_dir/${DOMAIN}.key" "$CERT_DIR/key.pem" 2>/dev/null || \
        cp "$acme_cert_dir"/*.key "$CERT_DIR/key.pem"
    }

  chmod 600 "$CERT_DIR"/*.pem

  FULLCHAIN_PATH="$CERT_DIR/fullchain.pem"
  KEY_PATH="$CERT_DIR/key.pem"

  success "Certificate installed to ${BOLD}$CERT_DIR${RESET}"
  echo ""

  # Verify cert
  local cert_cn cert_exp
  cert_cn=$(openssl x509 -in "$FULLCHAIN_PATH" -noout -subject 2>/dev/null | sed 's/.*CN = //' || true)
  cert_exp=$(openssl x509 -in "$FULLCHAIN_PATH" -noout -enddate 2>/dev/null | sed 's/.*=//' || true)

  if [[ -n "$cert_cn" ]]; then
    info "Subject:  ${BOLD}$cert_cn${RESET}"
    info "Expires:  ${BOLD}$cert_exp${RESET}"
  fi

  # Detect public IP and remind user about A records
  echo ""
  info "Detecting server public IP..."
  local server_ip=""
  server_ip=$(curl -4 -sf https://ifconfig.me 2>/dev/null || curl -4 -sf https://api.ipify.org 2>/dev/null || true)

  if [[ -n "$server_ip" ]]; then
    success "Public IP: ${BOLD}$server_ip${RESET}"
  fi

  hr
  printf "\n"
  printf "  ${BOLD}${YELLOW}IMPORTANT:${RESET} ${BOLD}Make sure your DNS A records are configured${RESET}\n"
  printf "\n"
  printf "  Your domain must point to this server for Temps to work.\n"
  printf "  Add these A records at your DNS provider (if not already done):\n"
  printf "\n"
  printf "    ${DIM}Name:${RESET}   ${BOLD}%s${RESET}      ${DIM}Type:${RESET} ${BOLD}A${RESET}   ${DIM}Value:${RESET}  ${BOLD}%s${RESET}\n" "$DOMAIN" "${server_ip:-<your-server-ip>}"
  printf "    ${DIM}Name:${RESET}   ${BOLD}*.%s${RESET}    ${DIM}Type:${RESET} ${BOLD}A${RESET}   ${DIM}Value:${RESET}  ${BOLD}%s${RESET}\n" "$DOMAIN" "${server_ip:-<your-server-ip>}"
  printf "\n"
  warn "If using Cloudflare, the wildcard (*.${DOMAIN}) record ${BOLD}must${RESET}${YELLOW} have proxy status OFF${RESET}"
  warn "${YELLOW}(DNS only / grey cloud). Cloudflare does not proxy wildcard records.${RESET}"
  printf "\n"
  info "${DIM}You can remove the _acme-challenge TXT records now — they're no longer needed.${RESET}"
  printf "\n"
  hr
  echo ""
  if [[ "$ASSUME_YES" == "true" ]]; then
    info "${DIM}--yes:${RESET} continuing past the DNS-records reminder."
    return 0
  fi
  require_tty "Press Enter to continue"
  printf "  ${ARROW} ${BOLD}Press Enter to continue${RESET}..."
  read -r < /dev/tty
}

# ---------------------------------------------------------------------------
# Step 4: Temps Setup
# ---------------------------------------------------------------------------

ADMIN_EMAIL=""
ADMIN_PASSWORD=""

# Contact email for Let's Encrypt / ACME certificate issuance. Required in quick
# mode (where the console + apps get on-demand HTTPS) — there is NO fallback in
# the binary, so an empty value means certs can never be issued. Prompted for in
# run_quick_flow and passed to `temps setup --letsencrypt-email`. Also reused as
# the admin login email so the operator has a single real address.
LETSENCRYPT_EMAIL=""

# ---------------------------------------------------------------------------
# Binary installer: download temps from GitHub releases.
# Usage: install_temps_binary [VERSION]
#   VERSION given  -> install that exact tag (ignores $CHANNEL)
#   VERSION empty  -> resolve the newest release on $CHANNEL
# ---------------------------------------------------------------------------
install_temps_binary() {
  local version="${1:-}"
  local platform target bin_dir exe

  platform="$(uname -ms)"
  case "$platform" in
    'Darwin x86_64')            target=darwin-amd64 ;;
    'Darwin arm64')             target=darwin-arm64 ;;
    'Linux aarch64' | 'Linux arm64') target=linux-arm64 ;;
    *)                          target=linux-amd64  ;;
  esac

  # Alpine / musl
  case "$target" in
    linux*) [[ -f /etc/alpine-release ]] && target="$target-musl" ;;
  esac

  # Resolve the newest version on the selected channel if none was pinned.
  if [[ -z "$version" ]]; then
    version=$(resolve_channel_version)
    [[ -z "$version" ]] && fatal "Failed to fetch latest $CHANNEL Temps release from GitHub"
    info "Latest $CHANNEL version: ${BOLD}$version${RESET}"
  else
    info "Pinned version: ${BOLD}$version${RESET}"
  fi

  bin_dir="$HOME_DIR/.temps/bin"
  exe="$bin_dir/temps"
  mkdir -p "$bin_dir"

  local url="https://github.com/gotempsh/temps/releases/download/$version/temps-$target.tar.gz"
  download_with_retry "$url" "$exe.tar.gz" || \
    fatal "Failed to download Temps from $url"
  tar -xzf "$exe.tar.gz" -C "$bin_dir" || fatal "Failed to extract Temps binary"
  chmod +x "$exe"
  rm -f "$exe.tar.gz"

  # $exe lives under $HOME — give it an executable SELinux label now so the
  # systemd service written in step 5 can actually exec it (see
  # ensure_selinux_exec_context). Needs sudo since semanage/restorecon write
  # to root-owned SELinux policy state.
  sudo_notice "to set an executable SELinux context on the Temps binary (Fedora/RHEL enforcing hosts only)"
  ensure_selinux_exec_context "$exe"

  # macOS quarantines binaries downloaded via curl (com.apple.quarantine),
  # which makes Gatekeeper block execution with "cannot be opened". Strip it
  # best-effort so the verification below — and `temps serve` — can run.
  if [[ "$IS_MACOS" == "true" ]] && check_command xattr; then
    xattr -d com.apple.quarantine "$exe" 2>/dev/null || true
  fi

  # Verify the binary actually executes before trusting it. A wrong-arch
  # download (e.g. amd64 on Apple Silicon) extracts fine but fails at exec with
  # "Exec format error"; Gatekeeper can also block it. Catch it here with a
  # clear, actionable message instead of a confusing failure three steps later.
  local installed_version
  if ! installed_version=$("$exe" --version 2>&1); then
    error "The Temps binary was downloaded but does not run on this machine."
    info "Detected platform: ${BOLD}$platform${RESET} (downloaded ${BOLD}temps-$target${RESET})"
    printf "    ${DIM}%s${RESET}\n" "$installed_version"
    if printf '%s' "$installed_version" | grep -qi "exec format error"; then
      info "This is an architecture mismatch — the binary doesn't match your CPU."
      info "Report it at ${UNDERLINE}https://github.com/gotempsh/temps/issues${RESET} with the platform line above."
    fi
    fatal "Cannot continue without a working Temps binary"
  fi

  success "Temps $version installed to ${DIM}$bin_dir${RESET}"
  info "Verified: ${BOLD}${installed_version}${RESET}"
  echo ""
}

# Ensure GeoLite2-City.mmdb is reachable by `temps serve`.
#
# `temps setup` downloads the DB into the data dir ($HOME_DIR/.temps/data), but
# the serve geo plugin opens "GeoLite2-City.mmdb" relative to its working
# directory ($HOME_DIR/.temps). If the file only exists in one place, serve
# crash-loops with "Failed to open MaxMind database". This makes both the
# data-dir copy and the working-dir copy resolve to a real file, downloading
# once if neither exists.
ensure_geolite2() {
  local home_db="$HOME_DIR/.temps/GeoLite2-City.mmdb"
  local data_db="$HOME_DIR/.temps/data/GeoLite2-City.mmdb"
  local geo_url="https://raw.githubusercontent.com/gotempsh/temps/refs/heads/main/crates/temps-cli/GeoLite2-City.mmdb"

  mkdir -p "$HOME_DIR/.temps/data"

  # If neither location has the DB (setup's download was skipped or failed),
  # fetch it into the data dir.
  if [[ ! -e "$data_db" ]] && [[ ! -e "$home_db" ]]; then
    echo ""
    info "Downloading GeoLite2 geolocation database..."
    if curl -sfL "$geo_url" -o "$data_db" 2>/dev/null; then
      success "GeoLite2 database installed"
    else
      warn "Could not download GeoLite2 database automatically."
      info "Temps serve requires it. Install it later with:"
      info "  ${BOLD}curl -sfL $geo_url -o $data_db${RESET}"
      return 0
    fi
  fi

  # Make the working-dir path resolve to the real file. Prefer the data-dir
  # copy as the source of truth; otherwise point data at the home copy.
  if [[ -e "$data_db" ]] && [[ ! -e "$home_db" ]]; then
    ln -sf "$data_db" "$home_db" 2>/dev/null || cp "$data_db" "$home_db" 2>/dev/null || true
  elif [[ -e "$home_db" ]] && [[ ! -e "$data_db" ]]; then
    ln -sf "$home_db" "$data_db" 2>/dev/null || cp "$home_db" "$data_db" 2>/dev/null || true
  fi
}

step_temps_setup() {
  step_header 4 $TOTAL_STEPS "Temps Platform Setup"

  # A previous run may have left a wrong-architecture binary on disk (e.g. it
  # downloaded temps-linux-amd64 on an aarch64 host) — file presence alone does
  # not mean it's usable, so drop it and force a fresh install rather than
  # silently limping forward with a binary that can't execute.
  if [[ -f $HOME_DIR/.temps/bin/temps ]] && ! "$HOME_DIR/.temps/bin/temps" --version &>/dev/null; then
    warn "Existing Temps binary at ${BOLD}$HOME_DIR/.temps/bin/temps${RESET} does not run on this machine — reinstalling."
    rm -f "$HOME_DIR/.temps/bin/temps"
  fi

  # Check if temps binary is installed
  if ! check_command temps && [[ ! -f $HOME_DIR/.temps/bin/temps ]]; then
    info "Installing Temps binary..."
    install_temps_binary "$TEMPS_VERSION"

    # Ensure it's in PATH
    export PATH="$HOME_DIR/.temps/bin:$PATH"
    sudo_notice "to symlink the temps binary into /usr/local/bin (so 'temps' works in your shell)"
    $SUDO ln -sf $HOME_DIR/.temps/bin/temps /usr/local/bin/temps 2>/dev/null || true
  fi

  local temps_bin
  if [[ -f $HOME_DIR/.temps/bin/temps ]]; then
    temps_bin="$HOME_DIR/.temps/bin/temps"
  else
    temps_bin="$(command -v temps)"
  fi

  local temps_version
  if ! temps_version=$("$temps_bin" --version 2>&1); then
    error "The Temps binary at ${BOLD}$temps_bin${RESET} does not run on this machine."
    printf "    ${DIM}%s${RESET}\n" "$temps_version"
    fatal "Cannot continue without a working Temps binary"
  fi
  success "Temps binary: ${DIM}$temps_version${RESET}"
  echo ""

  # Idempotency: check if temps setup has already been completed. "Completed"
  # means the host encryption key exists AND the database actually holds an admin
  # user — the two drift apart across deploy → undeploy → deploy (host data dir
  # kept while the DB volume is reset, or vice-versa). If the DB has no admin we
  # MUST re-seed; skipping would leave `temps serve` to hit the interactive
  # admin-email prompt and die with no TTY.
  local setup_skipped=false
  if [[ -f $HOME_DIR/.temps/data/encryption_key ]]; then
    ADMIN_EMAIL=$(state_get admin_email)
    ADMIN_PASSWORD=$(state_get admin_password)

    if db_has_admin_user; then
      success "Temps platform already configured"
      if [[ -n "$ADMIN_EMAIL" ]]; then
        info "Admin: ${BOLD}$ADMIN_EMAIL${RESET}"
      fi
      echo ""
      if ! prompt_yesno "Re-run temps setup?" "n"; then
        setup_skipped=true
      fi
    else
      warn "Encryption key present but the database has no admin user."
      info "The database volume was likely reset since the last install."
      info "Re-running setup to seed the admin account..."
      echo ""
    fi
  fi

  if [[ "$setup_skipped" != "true" ]]; then
    # Collect admin credentials. --email pre-fills the default so scripted
    # runs (and operators who want one address everywhere) can Enter through.
    prompt_input "Admin email" "$FLAG_EMAIL" ADMIN_EMAIL
    if [[ -z "$ADMIN_EMAIL" ]]; then
      fatal "Admin email is required"
    fi

    echo ""
    local default_password
    default_password=$(generate_admin_password)
    prompt_input "Admin password" "$default_password" ADMIN_PASSWORD
    if [[ ${#ADMIN_PASSWORD} -lt 8 ]]; then
      fatal "Password must be at least 8 characters"
    fi

    # Preview configuration
    echo ""
    hr
    printf "\n  ${BOLD}Configuration Preview${RESET}\n\n"
    summary_row "Domain:" "$DOMAIN"
    summary_row "Wildcard:" "$WILDCARD_DOMAIN"
    summary_row "Admin email:" "$ADMIN_EMAIL"
    summary_row "Admin password:" "$ADMIN_PASSWORD"
    summary_row "Database:" "postgresql://temps:***@127.0.0.1:${DB_PORT}/temps"
    summary_row "Certificate:" "$FULLCHAIN_PATH"
    summary_row "Key:" "$KEY_PATH"
    summary_row "Data directory:" "$HOME_DIR/.temps/data"
    echo ""
    hr
    echo ""

    if ! prompt_yesno "Proceed with this configuration?" "y"; then
      fatal "Setup cancelled by user"
    fi

    echo ""

    mkdir -p $HOME_DIR/.temps/data

    # Postgres only honors POSTGRES_PASSWORD when it initializes an EMPTY data
    # volume. If temps-db-data was reused from a prior install, the container
    # kept its OLD password and the freshly-generated $DB_PASSWORD we're about
    # to hand `temps setup` will fail with "password authentication failed for
    # user temps". Recover the password that actually works (wizard state ->
    # the live value we hold) and, if neither authenticates, reset the role over
    # the container's trusted local socket — exactly what step_timescaledb does,
    # repeated here because setup is also reachable on idempotent re-runs.
    if ! reconcile_db_password; then
      local saved_pw
      saved_pw=$(state_get db_password)
      if [[ -n "$saved_pw" && "$saved_pw" != "$DB_PASSWORD" ]]; then
        DB_PASSWORD="$saved_pw"
        reconcile_db_password || true
      fi
    fi
    state_set db_password "$DB_PASSWORD"

    local db_url="postgresql://temps:${DB_PASSWORD}@127.0.0.1:${DB_PORT}/temps?sslmode=disable"

    local setup_exit=0
    spinner "Configuring Temps platform..." \
      "$temps_bin" setup \
        --database-url "$db_url" \
        --admin-email "$ADMIN_EMAIL" \
        --admin-password "$ADMIN_PASSWORD" \
        --wildcard-domain "$WILDCARD_DOMAIN" \
        --wildcard-domain-cert "$FULLCHAIN_PATH" \
        --wildcard-domain-key "$KEY_PATH" \
        --skip-dns-records \
        --skip-git \
        --data-dir "$HOME_DIR/.temps/data" \
        --non-interactive \
      || setup_exit=$?
    echo ""

    if [[ $setup_exit -ne 0 ]]; then
      echo ""
      warn "Temps setup failed (exit code $setup_exit). Relevant output:"
      # Show non-timestamped lines (filter out Rust structured log noise)
      grep -Ev '^\s*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}' \
        /tmp/temps-wizard-cmd-out.log 2>/dev/null \
        | while IFS= read -r line; do
            [[ -n "$line" ]] && printf "  ${DIM}  %s${RESET}\n" "$line"
          done
      echo ""
      diagnose_setup_failure /tmp/temps-wizard-cmd-out.log
      fatal "Setup cannot continue"
    fi

    # Persist credentials for idempotency
    state_set admin_email "$ADMIN_EMAIL"
    state_set admin_password "$ADMIN_PASSWORD"
  fi

  # --- Post-setup tasks (always run, even on idempotency skip) ---

  # Sync encryption key
  if [[ -f $HOME_DIR/.temps/data/encryption_key ]]; then
    cp $HOME_DIR/.temps/data/encryption_key $HOME_DIR/.temps/encryption_key 2>/dev/null || true
  fi

  # Import base domain certificate (temps setup only imports wildcard;
  # base domain needs its own import for SNI matching)
  local db_url_import="postgresql://temps:${DB_PASSWORD}@127.0.0.1:${DB_PORT}/temps?sslmode=disable"
  if spinner "Importing base domain certificate..." \
    "$temps_bin" domain import \
      --domain "$DOMAIN" \
      --certificate "$FULLCHAIN_PATH" \
      --private-key "$KEY_PATH" \
      --database-url "$db_url_import" \
      --data-dir "$HOME_DIR/.temps/data" \
      --force; then
    echo ""
  else
    echo ""
    warn "Could not import base domain certificate (non-fatal)."
    info "You can run manually: ${BOLD}temps domain import --domain $DOMAIN --certificate $FULLCHAIN_PATH --private-key $KEY_PATH${RESET}"
  fi

  # GeoLite2 is required by `temps serve` (see ensure_geolite2 for the
  # data-dir vs working-dir path gap this resolves).
  ensure_geolite2
}

# ---------------------------------------------------------------------------
# Step 5: Background Service (systemd on Linux, launchd on macOS)
# ---------------------------------------------------------------------------

# Platform-agnostic service helpers
service_is_active() {
  local name="$1"
  if [[ "$IS_LINUX" == "true" ]]; then
    $SUDO systemctl is-active "$name" &>/dev/null
  elif [[ "$IS_MACOS" == "true" ]]; then
    launchctl list "dev.temps.$name" &>/dev/null 2>&1
  fi
}

service_start() {
  local name="$1"
  if [[ "$IS_LINUX" == "true" ]]; then
    $SUDO systemctl start "$name" 2>/dev/null
  elif [[ "$IS_MACOS" == "true" ]]; then
    launchctl bootstrap "gui/$(id -u)" "$HOME_DIR/Library/LaunchAgents/dev.temps.$name.plist" 2>/dev/null || \
      launchctl kickstart "gui/$(id -u)/dev.temps.$name" 2>/dev/null || true
  fi
}

service_stop() {
  local name="$1"
  if [[ "$IS_LINUX" == "true" ]]; then
    $SUDO systemctl stop "$name" 2>/dev/null || true
  elif [[ "$IS_MACOS" == "true" ]]; then
    launchctl bootout "gui/$(id -u)/dev.temps.$name" 2>/dev/null || true
  fi
}

service_restart() {
  local name="$1"
  if [[ "$IS_LINUX" == "true" ]]; then
    $SUDO systemctl restart "$name" 2>/dev/null || true
  elif [[ "$IS_MACOS" == "true" ]]; then
    service_stop "$name"
    sleep 1
    service_start "$name"
  fi
}

service_enable() {
  local name="$1"
  if [[ "$IS_LINUX" == "true" ]]; then
    $SUDO systemctl daemon-reload
    $SUDO systemctl enable "$name" > /dev/null 2>&1
  fi
  # launchd agents in ~/Library/LaunchAgents auto-load on login
}

# Service status/log commands for display
service_status_cmd() {
  local name="$1"
  if [[ "$IS_LINUX" == "true" ]]; then
    echo "${SUDO:+sudo }systemctl status $name"
  else
    echo "launchctl list dev.temps.$name"
  fi
}

service_logs_cmd() {
  local name="$1"
  if [[ "$IS_LINUX" == "true" ]]; then
    echo "${SUDO:+sudo }journalctl -u $name -f"
  else
    echo "tail -f $HOME_DIR/.temps/logs/$name.log"
  fi
}

# dump_service_logs <name> [lines]
# Print the tail of a service's logs inline so a failed start is diagnosable
# without the operator running a second command. Linux reads journald; macOS
# reads the log file launchd writes. De-dupes the repeated "password
# authentication failed" spam down to a single line + a count so the real
# startup error (above the spam) stays visible.
dump_service_logs() {
  local name="$1" lines="${2:-40}" raw
  if [[ "$IS_LINUX" == "true" ]]; then
    raw=$(${SUDO:+sudo }journalctl -u "$name" -n "$lines" --no-pager 2>/dev/null || true)
  else
    raw=$(tail -n "$lines" "$HOME_DIR/.temps/logs/$name.log" 2>/dev/null || true)
  fi
  [[ -z "$raw" ]] && { info "No logs found yet at ${BOLD}$HOME_DIR/.temps/logs/$name.log${RESET}"; return; }
  echo ""
  info "Last ${lines} lines of ${BOLD}$name${RESET} logs:"
  echo "${DIM}────────────────────────────────────────────────────────${RESET}"
  # Collapse runs of identical "password authentication failed" lines.
  printf '%s\n' "$raw" | awk '
    /password authentication failed for user/ { auth++; next }
    { if (auth) { printf "  … (%d× password authentication failed for user \"temps\")\n", auth; auth=0 }
      print "  " $0 }
    END { if (auth) printf "  … (%d× password authentication failed for user \"temps\")\n", auth }'
  echo "${DIM}────────────────────────────────────────────────────────${RESET}"
  echo ""
}

service_restart_cmd() {
  local name="$1"
  if [[ "$IS_LINUX" == "true" ]]; then
    echo "${SUDO:+sudo }systemctl restart $name"
  else
    echo "launchctl kickstart -k gui/\$(id -u)/dev.temps.$name"
  fi
}

step_service() {
  local svc_type="systemd"
  [[ "$IS_MACOS" == "true" ]] && svc_type="launchd"

  step_header 5 $TOTAL_STEPS "Background Service ($svc_type)"

  info "Temps can run as a background service that starts automatically"
  info "on boot and restarts if it crashes."
  echo ""

  # Use the console port chosen on a previous run (if any) for the health probe
  # below; a fresh install resolves it inside write_service_unit. Falls back to
  # the default when no run has happened yet.
  local saved_console
  saved_console="$(state_get console_port)"
  [[ -n "$saved_console" ]] && CONSOLE_PORT="$saved_console"

  # Check if already running and healthy
  if service_is_active temps \
    && curl -sf "http://localhost:${CONSOLE_PORT}/health" > /dev/null 2>&1; then
    success "Temps service is already active and healthy"
    info "Status: ${GREEN}active${RESET}"
    echo ""

    if prompt_yesno "Restart the service with new configuration?" "n"; then
      write_service_unit
      service_restart temps
      sleep 3
      success "Service restarted"
      echo ""
    fi
    return 0
  fi

  local status_cmd logs_cmd
  status_cmd=$(service_status_cmd temps)
  logs_cmd=$(service_logs_cmd temps)

  echo ""
  printf "  ${CYAN}┌─────────────────────────────────────────────────────┐${RESET}\n"
  printf "  ${CYAN}│${RESET}  ${BOLD}Recommended:${RESET} Install as a background service       ${CYAN}│${RESET}\n"
  printf "  ${CYAN}│${RESET}                                                     ${CYAN}│${RESET}\n"
  printf "  ${CYAN}│${RESET}  ${DIM}This ensures Temps runs in the background,${RESET}          ${CYAN}│${RESET}\n"
  printf "  ${CYAN}│${RESET}  ${DIM}starts on boot, and auto-restarts on failure.${RESET}       ${CYAN}│${RESET}\n"
  printf "  ${CYAN}│${RESET}                                                     ${CYAN}│${RESET}\n"
  printf "  ${CYAN}│${RESET}  ${DIM}You can manage it with:${RESET}                             ${CYAN}│${RESET}\n"
  printf "  ${CYAN}│${RESET}    ${GREEN}%-47s${RESET} ${CYAN}│${RESET}\n" "$status_cmd"
  printf "  ${CYAN}│${RESET}    ${GREEN}%-47s${RESET} ${CYAN}│${RESET}\n" "$logs_cmd"
  printf "  ${CYAN}│${RESET}                                                     ${CYAN}│${RESET}\n"
  printf "  ${CYAN}└─────────────────────────────────────────────────────┘${RESET}\n"
  echo ""

  if ! prompt_yesno "Install background service? (recommended)" "y"; then
    echo ""
    warn "Skipping service installation."
    info "You can start Temps manually with:"
    echo ""
    # macOS without root cannot bind :80/:443 — show the high-port fallback
    # so the copy-pasted command actually starts.
    local manual_http=80 manual_tls=443
    if [[ "$IS_MACOS" == "true" ]]; then
      manual_http=8080
      manual_tls=8443
    fi
    printf "  ${GREEN}  temps serve \\\\${RESET}\n"
    printf "  ${GREEN}    --address=\"0.0.0.0:${manual_http}\" \\\\${RESET}\n"
    printf "  ${GREEN}    --tls-address=\"0.0.0.0:${manual_tls}\" \\\\${RESET}\n"
    printf "  ${GREEN}    --database-url=\"postgresql://temps:***@127.0.0.1:${DB_PORT}/temps?sslmode=disable\" \\\\${RESET}\n"
    printf "  ${GREEN}    --data-dir=\"$HOME_DIR/.temps/data\" \\\\${RESET}\n"
    printf "  ${GREEN}    --console-address=\"0.0.0.0:${CONSOLE_PORT}\"${RESET}\n"
    echo ""
    return 0
  fi

  echo ""
  write_service_unit
  service_enable temps

  if ! service_start temps; then
    warn "Service failed to start on first attempt. Retrying in 3 seconds..."
    sleep 3
    service_restart temps
  fi

  echo ""
  # Wait for health
  info "Waiting for Temps to start..."
  local healthy=false
  for i in $(seq 1 20); do
    progress_bar "$i" 20 "checking health"
    if curl -sf "http://localhost:${CONSOLE_PORT}/health" > /dev/null 2>&1; then
      healthy=true
      break
    fi
    sleep 3
  done
  progress_bar 20 20 "checking health"
  echo ""

  if [[ "$healthy" == "true" ]]; then
    success "Temps service is running and healthy"
    echo ""
  else
    warn "Temps did not pass its health check within the timeout."
    dump_service_logs temps 40
    if dump_service_logs temps 60 2>/dev/null | grep -q "password authentication failed"; then
      error "The server cannot authenticate to PostgreSQL."
      info "This usually means the data volume holds an older password."
      info "Re-running the installer will reconcile it; if it persists, reset manually:"
      info "  ${BOLD}docker exec temps-timescaledb psql -U temps -d temps -c \"ALTER USER temps WITH PASSWORD '\$(cat $HOME_DIR/.temps/.wizard-state/db_password)';\"${RESET}"
      info "  ${BOLD}$(service_restart_cmd temps)${RESET}"
    else
      info "It may just need a few more seconds. Watch it with:"
      info "  ${BOLD}$(service_logs_cmd temps)${RESET}"
      info "Check status with: ${BOLD}$(service_status_cmd temps)${RESET}"
    fi
    echo ""
  fi
}

# Optional ClickHouse backend (advanced mode). Offers three choices: keep the
# default (TimescaleDB), point at an existing ClickHouse, or provision a local
# ClickHouse container. On enable, sets the CLICKHOUSE_* globals that
# write_service_unit injects as TEMPS_CLICKHOUSE_* into the service env.
#
# ClickHouse powers the proxy-log, analytics, and trace storage backends, which
# `temps serve` activates purely from those env vars — no settings change. (The
# resource-metrics path additionally gates on the `monitoring.store` setting, so
# it stays on TimescaleDB; the operator can switch it later in the console.)
step_clickhouse_optin() {
  # Already configured on a previous run? Reuse it silently.
  CLICKHOUSE_URL=$(state_get clickhouse_url)
  if [[ -n "$CLICKHOUSE_URL" ]]; then
    CLICKHOUSE_DATABASE=$(state_get clickhouse_database)
    CLICKHOUSE_USER=$(state_get clickhouse_user)
    CLICKHOUSE_PASSWORD=$(state_get clickhouse_password)
    CLICKHOUSE_ENABLED="true"
    success "ClickHouse already configured (${BOLD}${CLICKHOUSE_URL}${RESET})"
    return 0
  fi

  local choice=""
  prompt_choice choice "Use ClickHouse for proxy logs, analytics, and traces?" "1" \
    "No  — keep the default TimescaleDB backend (recommended for most installs)" \
    "Yes — use my existing ClickHouse server (I'll enter the connection details)" \
    "Yes — run a ClickHouse container on this server for me"

  case "$choice" in
    1|"")
      info "Using TimescaleDB for all backends."
      CLICKHOUSE_ENABLED="false"
      return 0
      ;;
    2)
      echo ""
      info "Enter your ClickHouse connection details."
      prompt_input "ClickHouse HTTP URL (e.g. http://ch.example.com:8123)" "" CLICKHOUSE_URL
      if [[ -z "$CLICKHOUSE_URL" ]]; then
        warn "No URL entered — skipping ClickHouse. Using TimescaleDB."
        CLICKHOUSE_ENABLED="false"
        return 0
      fi
      prompt_input "ClickHouse database" "temps" CLICKHOUSE_DATABASE
      prompt_input "ClickHouse user" "default" CLICKHOUSE_USER
      prompt_secret "ClickHouse password" CLICKHOUSE_PASSWORD
      ;;
    3)
      provision_clickhouse_container || {
        warn "ClickHouse container setup failed — continuing with TimescaleDB."
        CLICKHOUSE_ENABLED="false"
        return 0
      }
      ;;
    *)
      warn "Unrecognized choice '$choice' — using TimescaleDB."
      CLICKHOUSE_ENABLED="false"
      return 0
      ;;
  esac

  CLICKHOUSE_ENABLED="true"
  state_set clickhouse_url "$CLICKHOUSE_URL"
  state_set clickhouse_database "$CLICKHOUSE_DATABASE"
  state_set clickhouse_user "$CLICKHOUSE_USER"
  state_set clickhouse_password "$CLICKHOUSE_PASSWORD"
  success "ClickHouse enabled for proxy logs, analytics, and traces"
  info "Endpoint: ${BOLD}${CLICKHOUSE_URL}${RESET}  Database: ${BOLD}${CLICKHOUSE_DATABASE}${RESET}"
  echo ""
}

# Provision a local clickhouse-server container and set the CLICKHOUSE_* globals
# to point at it. Mirrors step_timescaledb: idempotent on the container name,
# binds to a free loopback port, generates a password, waits for readiness.
provision_clickhouse_container() {
  local ch_name="temps-clickhouse"
  local ch_http_port ch_user="temps" ch_db="temps"

  # Reuse a running container from a previous run.
  if $DOCKER_SUDO docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${ch_name}\$"; then
    ch_http_port=$(state_get clickhouse_http_port)
    [[ -z "$ch_http_port" ]] && ch_http_port=8123
    CLICKHOUSE_PASSWORD=$(state_get clickhouse_password)
    [[ -z "$CLICKHOUSE_PASSWORD" ]] && CLICKHOUSE_PASSWORD=$(generate_password)
    CLICKHOUSE_URL="http://127.0.0.1:${ch_http_port}"
    CLICKHOUSE_DATABASE="$ch_db"
    CLICKHOUSE_USER="$ch_user"
    success "ClickHouse container already running"
    info "Container: ${BOLD}${ch_name}${RESET}  Port: ${BOLD}127.0.0.1:${ch_http_port}${RESET}"
    return 0
  fi

  # Restart a stopped container if present.
  if $DOCKER_SUDO docker ps -a --format '{{.Names}}' 2>/dev/null | grep -q "^${ch_name}\$"; then
    info "Starting existing ClickHouse container..."
    $DOCKER_SUDO docker start "$ch_name" &>/dev/null || true
  else
    # Fresh install — pick a free HTTP port (8123 default).
    ch_http_port="$(state_get clickhouse_http_port)"
    [[ -z "$ch_http_port" ]] && ch_http_port=8123
    if port_in_use "$ch_http_port"; then
      local fallback
      if ! fallback="$(next_free_port 8124)"; then
        error "Could not find a free port in the range 8124–8143 for ClickHouse."
        return 1
      fi
      warn "Port ${BOLD}${ch_http_port}${RESET} is in use — using ${BOLD}${fallback}${RESET} for ClickHouse instead."
      ch_http_port="$fallback"
    fi
    state_set clickhouse_http_port "$ch_http_port"

    CLICKHOUSE_PASSWORD=$(generate_password)

    spinner "Pulling ClickHouse image" $DOCKER_SUDO docker pull clickhouse/clickhouse-server:latest || {
      error "Failed to pull the ClickHouse image."
      return 1
    }

    echo ""
    info "Starting ClickHouse container..."
    local run_err
    if ! run_err=$($DOCKER_SUDO docker run -d \
      --name "$ch_name" \
      --restart unless-stopped \
      --ulimit nofile=262144:262144 \
      -e CLICKHOUSE_USER="$ch_user" \
      -e CLICKHOUSE_PASSWORD="$CLICKHOUSE_PASSWORD" \
      -e CLICKHOUSE_DB="$ch_db" \
      -p 127.0.0.1:"$ch_http_port":8123 \
      -v temps-clickhouse-data:/var/lib/clickhouse \
      clickhouse/clickhouse-server:latest 2>&1); then
      echo ""
      error "Failed to start the ClickHouse container."
      printf "    ${DIM}%b${RESET}\n" "$run_err"
      return 1
    fi
  fi

  # Wait for the HTTP interface to answer.
  local ready=false
  for i in $(seq 1 30); do
    progress_bar "$i" 30 "Waiting for ClickHouse..."
    if $DOCKER_SUDO docker exec "$ch_name" \
      clickhouse-client --user "$ch_user" --password "$CLICKHOUSE_PASSWORD" \
      --query "SELECT 1" &>/dev/null; then
      ready=true
      break
    fi
    sleep 1
  done
  progress_bar 30 30 "Waiting for ClickHouse..."
  echo ""

  if [[ "$ready" != "true" ]]; then
    warn "ClickHouse did not become ready within 30 seconds."
    info "Check logs: ${BOLD}docker logs ${ch_name}${RESET}"
    return 1
  fi

  CLICKHOUSE_URL="http://127.0.0.1:${ch_http_port}"
  CLICKHOUSE_DATABASE="$ch_db"
  CLICKHOUSE_USER="$ch_user"
  success "ClickHouse is ready"
  info "Container: ${BOLD}${ch_name}${RESET}  Port: ${BOLD}127.0.0.1:${ch_http_port}${RESET}"
  return 0
}

write_service_unit() {
  local db_url="postgresql://temps:${DB_PASSWORD}@127.0.0.1:${DB_PORT}/temps?sslmode=disable"
  local temps_bin="$HOME_DIR/.temps/bin/temps"

  # Listen ports for the service. Linux systemd grants CAP_NET_BIND_SERVICE
  # (see AmbientCapabilities below) so the binary can bind the privileged
  # :80/:443 even when running as a non-root User=. macOS launchd *user*
  # agents (~/Library/LaunchAgents) run unprivileged and have no equivalent
  # capability, so they cannot bind ports < 1024 — a hardcoded :80/:443 plist
  # just crash-loops under KeepAlive. On macOS we prefer high ports (8080/8443).
  # resolve_service_ports also bumps off any port already taken (e.g. a second
  # Temps install) and persists the choice. Prefer 80/443 on Linux, 8080/8443
  # on macOS; resolve_service_ports maps a taken sub-1024 port to the 8080/8443
  # range automatically.
  local http_pref=80 tls_pref=443
  if [[ "$IS_MACOS" == "true" ]]; then
    http_pref=8080
    tls_pref=8443
  fi
  resolve_service_ports "$http_pref" "$tls_pref"
  local http_port="$LOCAL_PORT"
  local tls_port="$TLS_PORT"

  # Collect the extra service environment from two optional sources, so the
  # systemd `Environment=` lines and the launchd EnvironmentVariables dict are
  # each built once (a single dict — two competing dicts would be invalid plist):
  #   - telemetry opt-out (--no-telemetry) -> TEMPS_TELEMETRY=0
  #   - ClickHouse backend (advanced opt-in) -> the four TEMPS_CLICKHOUSE_* vars,
  #     which `temps serve` reads to activate the ClickHouse storage backends.
  local systemd_extra_env=""        # newline-prefixed `Environment=K=V` lines
  local plist_env_pairs=""          # `    <key>K</key>\n    <string>V</string>` lines

  add_service_env() {
    local key="$1" val="$2"
    systemd_extra_env+=$'\n'"Environment=${key}=${val}"
    plist_env_pairs+="    <key>${key}</key>"$'\n'"    <string>${val}</string>"$'\n'
  }

  if [[ "$TELEMETRY_OPTOUT" == "true" ]]; then
    add_service_env "TEMPS_TELEMETRY" "0"
  fi
  if [[ "$CLICKHOUSE_ENABLED" == "true" && -n "$CLICKHOUSE_URL" ]]; then
    add_service_env "TEMPS_CLICKHOUSE_URL" "$CLICKHOUSE_URL"
    add_service_env "TEMPS_CLICKHOUSE_DATABASE" "$CLICKHOUSE_DATABASE"
    add_service_env "TEMPS_CLICKHOUSE_USER" "$CLICKHOUSE_USER"
    add_service_env "TEMPS_CLICKHOUSE_PASSWORD" "$CLICKHOUSE_PASSWORD"
  fi

  # Wrap the collected pairs in the launchd EnvironmentVariables dict (only when
  # there is at least one pair), injected before WorkingDirectory.
  local plist_env_block=""
  if [[ -n "$plist_env_pairs" ]]; then
    plist_env_block="  <key>EnvironmentVariables</key>"$'\n'"  <dict>"$'\n'"${plist_env_pairs}  </dict>"$'\n'
  fi

  if [[ "$IS_LINUX" == "true" ]]; then
    sudo_notice "to write the systemd service unit to /etc/systemd/system/temps.service"
    $SUDO bash -c "cat > /etc/systemd/system/temps.service" << EOF
[Unit]
Description=Temps Platform Server
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=$RUN_USER
WorkingDirectory=$HOME_DIR/.temps
ExecStart=$temps_bin serve \\
  --address="0.0.0.0:${http_port}" \\
  --tls-address="0.0.0.0:${tls_port}" \\
  --database-url="$db_url" \\
  --data-dir="$HOME_DIR/.temps/data" \\
  --console-address="0.0.0.0:${CONSOLE_PORT}"
Restart=always
RestartSec=5
LimitNOFILE=65535
AmbientCapabilities=CAP_NET_BIND_SERVICE
Environment=HOME=$HOME_DIR$systemd_extra_env

[Install]
WantedBy=multi-user.target
EOF
    success "Systemd unit written to ${BOLD}/etc/systemd/system/temps.service${RESET}"

  elif [[ "$IS_MACOS" == "true" ]]; then
    mkdir -p "$HOME_DIR/Library/LaunchAgents"
    mkdir -p "$HOME_DIR/.temps/logs"
    cat > "$HOME_DIR/Library/LaunchAgents/dev.temps.temps.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>dev.temps.temps</string>
  <key>ProgramArguments</key>
  <array>
    <string>$temps_bin</string>
    <string>serve</string>
    <string>--address=0.0.0.0:${http_port}</string>
    <string>--tls-address=0.0.0.0:${tls_port}</string>
    <string>--database-url=$db_url</string>
    <string>--data-dir=$HOME_DIR/.temps/data</string>
    <string>--console-address=0.0.0.0:${CONSOLE_PORT}</string>
    <string>--disable-https-redirect</string>
  </array>
${plist_env_block}  <key>WorkingDirectory</key>
  <string>$HOME_DIR/.temps</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$HOME_DIR/.temps/logs/temps.log</string>
  <key>StandardErrorPath</key>
  <string>$HOME_DIR/.temps/logs/temps.log</string>
</dict>
</plist>
EOF
    success "LaunchAgent written to ${BOLD}~/Library/LaunchAgents/dev.temps.temps.plist${RESET}"
    warn "macOS launchd user agents cannot bind privileged ports."
    info "Temps will listen on ${BOLD}:${http_port}${RESET} (HTTP) and ${BOLD}:${tls_port}${RESET} (HTTPS) instead of :80/:443."
    info "To serve on :80/:443, put a reverse proxy in front or run as a root LaunchDaemon."
  fi
}

# ---------------------------------------------------------------------------
# Verification: generate API key + verify console URL is reachable
# ---------------------------------------------------------------------------

API_KEY=""

# Generate (or reuse) an admin API key for CLI/automation access, directly
# against the database (works before/without console reachability). Persisted
# in wizard state so re-runs return the same key. Sets the API_KEY global; on
# failure leaves it empty and prints the manual command (non-fatal).
ensure_api_key() {
  [[ -n "$API_KEY" ]] && return 0
  [[ -z "$DB_PASSWORD" ]] && DB_PASSWORD=$(state_get db_password)
  [[ -z "$ADMIN_EMAIL" ]] && ADMIN_EMAIL=$(state_get admin_email)

  local temps_bin="$HOME_DIR/.temps/bin/temps"
  if [[ ! -f "$temps_bin" ]]; then
    temps_bin="$(command -v temps 2>/dev/null || echo "$HOME_DIR/.temps/bin/temps")"
  fi

  local db_url="postgresql://temps:${DB_PASSWORD}@127.0.0.1:${DB_PORT}/temps?sslmode=disable"

  # Check if we already have an API key from a previous run
  API_KEY=$(state_get api_key)
  if [[ -z "$API_KEY" ]]; then
    info "Generating API key..."
    local apikey_output
    apikey_output=$("$temps_bin" api-key \
      --database-url "$db_url" \
      --name "wizard-setup" \
      --role admin \
      --user-email "$ADMIN_EMAIL" \
      --output-format json \
      2>/dev/null) || true

    if [[ -n "$apikey_output" ]]; then
      # Extract the key from JSON output
      API_KEY=$(json_value "$apikey_output" "key")
      # Fallback: try "api_key" field name
      [[ -z "$API_KEY" ]] && API_KEY=$(json_value "$apikey_output" "api_key")
      # Fallback: try "token" field name
      [[ -z "$API_KEY" ]] && API_KEY=$(json_value "$apikey_output" "token")
    fi

    if [[ -n "$API_KEY" ]]; then
      state_set api_key "$API_KEY"
      success "API key generated"
    else
      warn "Could not generate API key automatically."
      info "You can create one manually: ${BOLD}temps api-key --database-url \"$db_url\" --name \"my-key\"${RESET}"
    fi
  else
    success "API key already generated"
  fi
}

step_verify() {
  echo ""
  hr
  echo ""
  printf "  ${BG_BLUE}${BOLD}${WHITE} VERIFYING ${RESET}  ${BOLD}Checking your Temps instance${RESET}\n"
  echo ""

  # Recover globals from state if needed (idempotent re-runs)
  [[ -z "$DOMAIN" ]] && DOMAIN=$(state_get domain)
  [[ -z "$DB_PASSWORD" ]] && DB_PASSWORD=$(state_get db_password)
  [[ -z "$ADMIN_EMAIL" ]] && ADMIN_EMAIL=$(state_get admin_email)

  local console_url="https://$DOMAIN"

  # --- 1. Generate API key ---
  ensure_api_key

  # --- 2. Verify console URL is reachable ---
  echo ""
  info "Verifying ${BOLD}$console_url${RESET} is reachable..."

  local verified=false
  for i in $(seq 1 15); do
    progress_bar "$i" 15 "waiting for response"
    local http_status
    http_status=$(curl -sk -o /dev/null -w "%{http_code}" "$console_url" 2>/dev/null || echo "000")

    # Any real HTTP response (even 302 redirect to login) means it's working
    if [[ "$http_status" =~ ^[2-3][0-9][0-9]$ ]]; then
      verified=true
      break
    fi
    sleep 3
  done
  progress_bar 15 15 "waiting for response"
  echo ""

  if [[ "$verified" == "true" ]]; then
    success "Console is live at ${BOLD}${UNDERLINE}$console_url${RESET}"
    echo ""
  else
    warn "Console did not respond yet at ${BOLD}$console_url${RESET}"
    info "DNS propagation may still be in progress."
    info "Check service logs: ${BOLD}$(service_logs_cmd temps)${RESET}"
    echo ""
  fi
}

# ---------------------------------------------------------------------------
# Test Deployments (optional)
# ---------------------------------------------------------------------------

step_test_deploy() {
  echo ""
  hr
  echo ""
  printf "  ${BG_BLUE}${BOLD}${WHITE} TEST DEPLOY ${RESET}  ${BOLD}Verify your platform with sample apps${RESET}\n"
  echo ""
  info "This will deploy a static page and a Next.js Docker app"
  info "to confirm everything is working end-to-end."
  echo ""

  if ! prompt_yesno "Deploy test applications?" "y"; then
    info "Skipping test deploy."
    return 0
  fi

  # Recover globals from state if needed
  if [[ -z "$DOMAIN" ]]; then
    DOMAIN=$(state_get domain)
  fi
  if [[ -z "$API_KEY" ]]; then
    API_KEY=$(state_get api_key)
  fi

  if [[ -z "$DOMAIN" ]] || [[ -z "$API_KEY" ]]; then
    warn "Domain or API key not available — cannot run test deploy."
    return 0
  fi

  local base_url="https://$DOMAIN"

  # --- Ensure Node.js / npx is available ---
  local npx_cmd=""

  if check_command npx; then
    npx_cmd="npx"
  elif check_command bunx; then
    npx_cmd="bunx"
  else
    info "Installing Node.js for CLI tools..."
    spinner "Installing Node.js 22..." bash -c '
      if command -v apt-get &>/dev/null; then
        curl -fsSL https://deb.nodesource.com/setup_22.x | '"$SUDO"' bash - &>/dev/null
        '"$SUDO"' apt-get install -y nodejs &>/dev/null
      elif command -v dnf &>/dev/null; then
        curl -fsSL https://rpm.nodesource.com/setup_22.x | '"$SUDO"' bash - &>/dev/null
        '"$SUDO"' dnf install -y nodejs &>/dev/null
      elif command -v yum &>/dev/null; then
        curl -fsSL https://rpm.nodesource.com/setup_22.x | '"$SUDO"' bash - &>/dev/null
        '"$SUDO"' yum install -y nodejs &>/dev/null
      elif command -v brew &>/dev/null; then
        brew install node &>/dev/null
      else
        exit 1
      fi
    '
    echo ""
    hash -r 2>/dev/null || true

    if check_command npx; then
      npx_cmd="npx"
      success "Node.js installed"
    else
      warn "Could not install Node.js — skipping test deploy."
      return 0
    fi
  fi

  echo ""
  # Configure Temps CLI
  info "Configuring Temps CLI..."
  local api_url="${base_url}/api"
  $npx_cmd -y @temps-sdk/cli configure set apiUrl "$api_url" --no-color 2>/dev/null
  $npx_cmd -y @temps-sdk/cli login --api-key "$API_KEY" --no-color 2>/dev/null
  success "CLI authenticated"
  echo ""

  local test_work_dir
  test_work_dir=$(mktemp -d)

  # Track results
  local static_ok=false
  local nextjs_ok=false

  # ===========================================================
  # Test A — Static Files
  # ===========================================================

  echo ""
  printf "  ${BOLD}${CYAN}Test A${RESET} ${DIM}─${RESET} ${BOLD}Static Files${RESET}\n"
  echo ""

  local static_slug="hello-world"

  # Check if project exists
  local existing
  existing=$(curl -sk \
    -H "Authorization: Bearer $API_KEY" \
    "${base_url}/api/projects" 2>/dev/null || echo "")

  if echo "$existing" | grep -q "\"slug\":\"$static_slug\""; then
    info "Project ${BOLD}$static_slug${RESET} already exists — redeploying"
  else
    info "Creating project ${BOLD}$static_slug${RESET}..."
    local create_code create_body create_resp
    create_resp=$(curl -sk -w "\n%{http_code}" \
      -H "Authorization: Bearer $API_KEY" \
      -H "Content-Type: application/json" \
      -X POST "${base_url}/api/projects" \
      -d "{\"name\":\"$static_slug\",\"directory\":\"/\",\"main_branch\":\"main\",\"preset\":\"nextjs\",\"storage_service_ids\":[],\"source_type\":\"static_files\"}" 2>/dev/null)
    create_code=$(echo "$create_resp" | tail -1)
    if [[ "$create_code" != "200" ]] && [[ "$create_code" != "201" ]]; then
      create_body=$(echo "$create_resp" | sed '$d')
      error "Failed to create project (HTTP $create_code): $create_body"
      warn "Skipping static test."
    else
      success "Project created"
    fi
  fi

  # Build static site
  local static_dir="$test_work_dir/site"
  mkdir -p "$static_dir"
  cat > "$static_dir/index.html" << 'STATICHTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hello from Temps</title>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:linear-gradient(135deg,#0f172a,#1e293b);color:#e2e8f0;min-height:100vh;display:flex;align-items:center;justify-content:center}
    .c{text-align:center;padding:2rem}
    h1{font-size:3rem;background:linear-gradient(90deg,#38bdf8,#818cf8,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1rem}
    p{font-size:1.25rem;color:#94a3b8;margin-bottom:2rem}
    .b{display:inline-block;background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.3);border-radius:9999px;padding:.5rem 1.5rem;font-size:.875rem;color:#38bdf8}
  </style>
</head>
<body>
  <div class="c">
    <h1>Hello from Temps</h1>
    <p>Your self-hosted deployment platform is working.</p>
    <span class="b">Static Deploy Test</span>
  </div>
</body>
</html>
STATICHTML

  local archive="$test_work_dir/site.tar.gz"
  tar -czf "$archive" -C "$static_dir" .

  info "Deploying static files..."
  local deploy_exit=0
  local deploy_out
  deploy_out=$($npx_cmd -y @temps-sdk/cli deploy:static \
    --path "$archive" \
    --project "$static_slug" \
    --environment "production" \
    --yes \
    --no-color 2>&1) || deploy_exit=$?

  if [[ $deploy_exit -ne 0 ]]; then
    error "Static deploy failed (exit $deploy_exit)"
    echo "    $deploy_out" | head -5
  else
    success "Static files deployed"

    # Verify
    local static_url="https://${static_slug}-production.${DOMAIN}"
    local http_ok=false
    for i in $(seq 1 10); do
      progress_bar "$i" 10 "verifying"
      local code
      code=$(curl -sk -o /dev/null -w "%{http_code}" "$static_url" 2>/dev/null || echo "000")
      if [[ "$code" =~ ^[2-3][0-9][0-9]$ ]]; then
        http_ok=true
        break
      fi
      sleep 2
    done
    progress_bar 10 10 "done"
    echo ""

    if [[ "$http_ok" == "true" ]]; then
      success "Static app live at ${BOLD}${UNDERLINE}$static_url${RESET}"
      static_ok=true
    else
      warn "Static app not responding at $static_url"
    fi
  fi

  # ===========================================================
  # Test B — Next.js Docker
  # ===========================================================

  local has_docker=false
  if $DOCKER_SUDO docker info &>/dev/null 2>&1; then
    has_docker=true
  fi

  if [[ "$has_docker" == "true" ]]; then
    echo ""
    printf "  ${BOLD}${CYAN}Test B${RESET} ${DIM}─${RESET} ${BOLD}Next.js Docker${RESET}\n"
    echo ""

    local nextjs_slug="hello-nextjs"
    local nextjs_image="hello-nextjs-temps-test:latest"

    # Create project
    if echo "$existing" | grep -q "\"slug\":\"$nextjs_slug\""; then
      info "Project ${BOLD}$nextjs_slug${RESET} already exists — redeploying"
    else
      info "Creating project ${BOLD}$nextjs_slug${RESET}..."
      create_resp=$(curl -sk -w "\n%{http_code}" \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -X POST "${base_url}/api/projects" \
        -d "{\"name\":\"$nextjs_slug\",\"directory\":\"/\",\"main_branch\":\"main\",\"preset\":\"nextjs\",\"storage_service_ids\":[],\"source_type\":\"docker_image\"}" 2>/dev/null)
      create_code=$(echo "$create_resp" | tail -1)
      if [[ "$create_code" != "200" ]] && [[ "$create_code" != "201" ]]; then
        create_body=$(echo "$create_resp" | sed '$d')
        error "Failed to create project (HTTP $create_code): $create_body"
      else
        success "Project created"
      fi
    fi

    # Scaffold Next.js app
    local nextjs_dir="$test_work_dir/nextjs-app"
    mkdir -p "$nextjs_dir/app"

    cat > "$nextjs_dir/package.json" << 'PKGJSON'
{
  "name": "hello-nextjs",
  "version": "1.0.0",
  "private": true,
  "scripts": { "dev": "next dev", "build": "next build", "start": "next start" },
  "dependencies": { "next": "15.3.4", "react": "^19.0.0", "react-dom": "^19.0.0" }
}
PKGJSON

    cat > "$nextjs_dir/next.config.js" << 'NEXTCFG'
/** @type {import('next').NextConfig} */
const nextConfig = { output: 'standalone' }
module.exports = nextConfig
NEXTCFG

    cat > "$nextjs_dir/app/layout.js" << 'LAYOUT'
export const metadata = { title: 'Hello from Temps' }
export default function RootLayout({ children }) {
  return <html lang="en"><body>{children}</body></html>
}
LAYOUT

    cat > "$nextjs_dir/app/page.js" << 'PAGEJS'
export default function Home() {
  return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'linear-gradient(135deg,#0f172a,#1e293b)',color:'#e2e8f0',fontFamily:'-apple-system,BlinkMacSystemFont,sans-serif'}}>
      <div style={{textAlign:'center'}}>
        <h1 style={{fontSize:'3rem',marginBottom:'1rem'}}>Hello from Temps</h1>
        <p style={{fontSize:'1.25rem',color:'#94a3b8'}}>Next.js running in Docker on your self-hosted platform.</p>
        <span style={{display:'inline-block',background:'rgba(56,189,248,.1)',border:'1px solid rgba(56,189,248,.3)',borderRadius:'9999px',padding:'.5rem 1.5rem',fontSize:'.875rem',color:'#38bdf8',marginTop:'1rem'}}>Next.js Docker Deploy</span>
      </div>
    </div>
  )
}
PAGEJS

    cat > "$nextjs_dir/Dockerfile" << 'DKRFILE'
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json ./
RUN npm install --production=false

FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
DKRFILE

    info "Building Docker image (30-90 seconds)..."
    local build_exit=0
    spinner "Building Next.js Docker image..." $DOCKER_SUDO docker build -t "$nextjs_image" "$nextjs_dir" || build_exit=$?
    echo ""

    if [[ $build_exit -ne 0 ]]; then
      error "Docker build failed. Check output above."
    else
      local image_size
      image_size=$($DOCKER_SUDO docker images "$nextjs_image" --format "{{.Size}}" 2>/dev/null || echo "unknown")
      success "Docker image built (${image_size})"
      echo ""

      # Get project ID and environment ID
      local proj_data proj_id env_data env_id
      proj_data=$(curl -sk \
        -H "Authorization: Bearer $API_KEY" \
        "${base_url}/api/projects" 2>/dev/null || echo "")

      if check_command python3; then
        proj_id=$(echo "$proj_data" | python3 -c "
import json,sys
for p in json.load(sys.stdin).get('projects',[]):
  if p.get('slug')=='$nextjs_slug': print(p['id']); break
" 2>/dev/null || echo "")
      fi
      if [[ -z "$proj_id" ]]; then
        proj_id=$(json_value "$proj_data" "id")
      fi

      if [[ -n "$proj_id" ]]; then
        env_data=$(curl -sk \
          -H "Authorization: Bearer $API_KEY" \
          "${base_url}/api/projects/$proj_id/environments" 2>/dev/null || echo "")

        if check_command python3; then
          env_id=$(echo "$env_data" | python3 -c "
import json,sys
for e in json.load(sys.stdin):
  if e.get('name')=='production': print(e['id']); break
" 2>/dev/null || echo "")
        fi
        if [[ -z "$env_id" ]]; then
          env_id=$(json_value "$env_data" "id")
        fi
      fi

      if [[ -n "$proj_id" ]] && [[ -n "$env_id" ]]; then
        # Export and upload
        info "Uploading Docker image to Temps..."
        local image_tar="$test_work_dir/nextjs-image.tar"
        spinner "Exporting Docker image..." $DOCKER_SUDO docker save "$nextjs_image" -o "$image_tar"
        echo ""

        local upload_resp upload_code upload_body
        upload_resp=$(curl -sk -w "\n%{http_code}" \
          -H "Authorization: Bearer $API_KEY" \
          -F "file=@${image_tar};type=application/x-tar" \
          "${base_url}/api/projects/${proj_id}/environments/${env_id}/deploy/image-upload" 2>/dev/null)
        upload_code=$(echo "$upload_resp" | tail -1)
        upload_body=$(echo "$upload_resp" | sed '$d')

        rm -f "$image_tar"

        if [[ "$upload_code" != "200" ]] && [[ "$upload_code" != "201" ]] && [[ "$upload_code" != "202" ]]; then
          error "Image upload failed (HTTP $upload_code): $upload_body"
        else
          success "Image uploaded — deployment started"

          # Wait for deployment
          info "Waiting for deployment..."
          local dep_status="pending" dep_ok=false
          for i in $(seq 1 40); do
            progress_bar "$i" 40 "$dep_status"
            local status_resp new_status=""
            status_resp=$(curl -sk \
              -H "Authorization: Bearer $API_KEY" \
              "${base_url}/api/projects/${proj_id}/deployments" 2>/dev/null || echo "")
            if check_command python3; then
              new_status=$(echo "$status_resp" | python3 -c "
import json,sys
d=json.load(sys.stdin).get('deployments',[])
if d: print(d[0].get('status',''))
" 2>/dev/null || echo "")
            fi
            if [[ -z "$new_status" ]]; then
              new_status=$(json_value "$status_resp" "status")
            fi
            if [[ -n "$new_status" ]]; then
              dep_status="$new_status"
            fi
            case "$dep_status" in
              completed|ready|active|succeeded) dep_ok=true; break ;;
              failed|error|cancelled) break ;;
            esac
            sleep 3
          done
          progress_bar 40 40 "$dep_status"
          echo ""

          if [[ "$dep_ok" == "true" ]]; then
            success "Next.js deployment completed"
            echo ""

            # Verify
            local nextjs_url="https://${nextjs_slug}-production.${DOMAIN}"
            for i in $(seq 1 10); do
              progress_bar "$i" 10 "verifying"
              local code
              code=$(curl -sk -o /dev/null -w "%{http_code}" "$nextjs_url" 2>/dev/null || echo "000")
              if [[ "$code" =~ ^[2-3][0-9][0-9]$ ]]; then
                nextjs_ok=true
                break
              fi
              sleep 2
            done
            progress_bar 10 10 "done"
            echo ""

            if [[ "$nextjs_ok" == "true" ]]; then
              success "Next.js app live at ${BOLD}${UNDERLINE}$nextjs_url${RESET}"
            else
              warn "Next.js app not responding at $nextjs_url"
            fi
          else
            error "Next.js deployment failed (status: $dep_status)"
          fi
        fi
      else
        error "Could not determine project/environment IDs"
      fi

      # Clean up image
      $DOCKER_SUDO docker rmi "$nextjs_image" &>/dev/null || true
    fi
  else
    info "Docker not available — skipping Next.js Docker test"
  fi

  # --- Summary ---
  echo ""
  printf "  ${BOLD}Test Results${RESET}\n"
  echo ""

  if [[ "$static_ok" == "true" ]]; then
    printf "  ${CHECK} ${BOLD}Static Files${RESET}    ${GREEN}$static_url${RESET}\n"
  else
    printf "  ${CROSS} ${BOLD}Static Files${RESET}    ${YELLOW}not verified${RESET}\n"
  fi

  if [[ "$has_docker" == "true" ]]; then
    if [[ "$nextjs_ok" == "true" ]]; then
      printf "  ${CHECK} ${BOLD}Next.js Docker${RESET}  ${GREEN}$nextjs_url${RESET}\n"
    else
      printf "  ${CROSS} ${BOLD}Next.js Docker${RESET}  ${YELLOW}not verified${RESET}\n"
    fi
  else
    printf "  ${DIM}  Next.js Docker   skipped (no Docker)${RESET}\n"
  fi
  echo ""

  # Clean up work dir
  rm -rf "$test_work_dir"
}

# ---------------------------------------------------------------------------
# Completion
# ---------------------------------------------------------------------------

# Minimal JSON string escaping (backslash + double quote). The values we emit
# are generated passwords, emails, domains, and URLs — control characters
# don't occur, so this is sufficient without pulling in jq/python.
json_escape() {
  local s="${1//\\/\\\\}"
  s="${s//\"/\\\"}"
  printf '%s' "$s"
}

# Write the machine-readable install result for scripted/headless runs
# (AI agents, CI): ~/.temps/setup-result.json (mode 0600 — it contains the
# admin password) plus a final "::temps:result:: {json}" stdout line so a
# caller can harvest it from the command output without knowing the path.
# Usage: write_setup_result <console_url> <apps_url_pattern> <domain>
write_setup_result() {
  local console_url="$1" apps_url_pattern="$2" domain="$3"
  local result_file="$HOME_DIR/.temps/setup-result.json"
  local api_key_json="null"
  [[ -n "${API_KEY:-}" ]] && api_key_json="\"$(json_escape "$API_KEY")\""
  local json
  json=$(printf '{"status":"ok","mode":"%s","channel":"%s","console_url":"%s","apps_url_pattern":"%s","domain":"%s","admin_email":"%s","admin_password":"%s","api_key":%s}' \
    "$(json_escape "$SETUP_MODE")" "$(json_escape "$CHANNEL")" \
    "$(json_escape "$console_url")" "$(json_escape "$apps_url_pattern")" \
    "$(json_escape "$domain")" "$(json_escape "$ADMIN_EMAIL")" \
    "$(json_escape "$ADMIN_PASSWORD")" "$api_key_json")
  mkdir -p "$HOME_DIR/.temps"
  ( umask 077; printf '%s\n' "$json" > "$result_file" ) \
    || warn "Could not write $result_file (non-fatal)"
  printf '::temps:result:: %s\n' "$json"
}

show_completion() {
  # Recover credentials from state if step was skipped on re-run
  [[ -z "$ADMIN_EMAIL" ]] && ADMIN_EMAIL=$(state_get admin_email)
  [[ -z "$ADMIN_PASSWORD" ]] && ADMIN_PASSWORD=$(state_get admin_password)

  echo ""
  hr
  echo ""
  printf "  ${BG_GREEN}${BOLD}${WHITE} SETUP COMPLETE ${RESET}\n"
  echo ""

  local console_url="https://$DOMAIN"

  printf "  ${BOLD}Your Temps instance is ready!${RESET}\n"
  echo ""
  summary_row "Console:" "$console_url"
  summary_row "Admin email:" "$ADMIN_EMAIL"
  summary_row "Admin password:" "$ADMIN_PASSWORD"
  if [[ -n "$API_KEY" ]]; then
    summary_row "API key:" "$API_KEY"
  fi
  summary_row "Domain:" "$DOMAIN"
  summary_row "Wildcard:" "$WILDCARD_DOMAIN"
  if [[ "$CLICKHOUSE_ENABLED" == "true" ]]; then
    summary_row "ClickHouse:" "${CLICKHOUSE_URL} (logs, analytics, traces)"
  fi
  if [[ "$TELEMETRY_OPTOUT" == "true" ]]; then
    summary_row "Telemetry:" "disabled (opt-out)"
  else
    summary_row "Telemetry:" "on (anonymous, no PII) — disable with --no-telemetry"
  fi
  echo ""

  warn "Save your admin password and API key now — they won't be shown again."
  echo ""

  hr
  echo ""
  printf "  ${BOLD}Next steps${RESET}\n"
  echo ""
  info "1. Open your console at ${GREEN}${UNDERLINE}${console_url}${RESET}"
  info "2. Log in with ${BOLD}$ADMIN_EMAIL${RESET} and your password"
  info "3. Deploy your first app with ${GREEN}temps deploy${RESET}"
  echo ""

  hr
  echo ""
  printf "  ${BOLD}Useful commands${RESET}\n"
  echo ""
  info "${GREEN}$(service_status_cmd temps)${RESET}"
  info "                                  Service status"
  info "${GREEN}$(service_restart_cmd temps)${RESET}"
  info "                                  Restart the server"
  info "${GREEN}$(service_logs_cmd temps)${RESET}"
  info "                                  Live logs"
  info "${GREEN}temps --help${RESET}                     CLI reference"
  echo ""

  hr
  echo ""
  info "Documentation: ${UNDERLINE}https://temps.sh/docs${RESET}"
  info "Support:       ${UNDERLINE}https://github.com/gotempsh/temps/issues${RESET}"
  echo ""

  # Final access box — shown last so credentials are always visible on screen
  hr
  echo ""
  printf "  ${BG_BLUE}${BOLD}${WHITE} YOUR ACCESS DETAILS ${RESET}\n"
  echo ""
  printf "  ${BOLD}%-20s${RESET} ${GREEN}${UNDERLINE}%s${RESET}\n" "Console URL:" "$console_url"
  printf "  ${BOLD}%-20s${RESET} %s\n" "Email:" "$ADMIN_EMAIL"
  printf "  ${BOLD}%-20s${RESET} ${BOLD}%s${RESET}\n" "Password:" "$ADMIN_PASSWORD"
  echo ""
  warn "Save your password now — also stored at ${DIM}$STATE_DIR/admin_password${RESET}"
  echo ""

  write_setup_result "$console_url" "https://<project>.${DOMAIN}" "$DOMAIN"
}

# ---------------------------------------------------------------------------
# QuickStart flow (sslip.io)
# ---------------------------------------------------------------------------
#
# A streamlined path that gets Temps running without a custom domain. The
# console at console.<ip>.sslip.io and every app at <app>.<ip>.sslip.io get a
# real Let's Encrypt certificate via on-demand TLS (ADR-018): the proxy binds
# :443 and issues a per-host HTTP-01 cert lazily the first time each hostname is
# hit (the first handshake fails fast, the retry succeeds). `temps setup` turns
# this on automatically for sslip.io installs. No wildcard cert is needed —
# *.<ip>.sslip.io wildcards cannot be issued by Let's Encrypt, but per-host
# certs can. Local mode stays HTTP (loopback is unreachable from Let's Encrypt).
#
# Reuses step_docker and step_timescaledb (mode-agnostic, idempotent), then
# installs the binary on the chosen channel and runs `temps setup --auto`.

# Detect this server's public IPv4, falling back to a private IP, then 127.0.0.1.
detect_public_ip_quick() {
  local ip=""
  ip=$(curl -4 -sf --max-time 5 https://api.ipify.org 2>/dev/null \
    || curl -4 -sf --max-time 5 https://ifconfig.me 2>/dev/null || true)
  if [[ -z "$ip" ]]; then
    ip=$(detect_local_ip)
  fi
  [[ -z "$ip" ]] && ip="127.0.0.1"
  echo "$ip"
}

# Detect this machine's own outbound interface IPv4 (the address it presents
# on its local network, before any router/NAT translates it). Used to spot
# NAT: if this differs from the internet-facing IP an echo service reports,
# there's a router between us and the internet and inbound traffic to the
# public IP only reaches this box if that router forwards it here.
detect_local_ip() {
  local ip=""
  if [[ "$IS_LINUX" == "true" ]]; then
    ip=$(ip -4 route get 8.8.8.8 2>/dev/null | grep -oE 'src [0-9.]+' | awk '{print $2}' | head -1 || true)
    [[ -z "$ip" ]] && ip=$(hostname -I 2>/dev/null | awk '{print $1}' || true)
  elif [[ "$IS_MACOS" == "true" ]]; then
    local iface=""
    iface=$(route -n get 8.8.8.8 2>/dev/null | awk '/interface: / {print $2}' || true)
    [[ -n "$iface" ]] && ip=$(ipconfig getifaddr "$iface" 2>/dev/null || true)
  fi
  echo "$ip"
}

# Write the systemd unit / launchd plist for quick mode.
# Usage: write_quick_service_unit <tls: true|false>
# HTTP listens on :80 with --disable-https-redirect; when tls=true we also
# listen on :443 (the cert is served from the data dir provisioned via HTTP-01).
write_quick_service_unit() {
  local tls="${1:-false}"
  local db_url="postgresql://temps:${DB_PASSWORD}@127.0.0.1:${DB_PORT}/temps?sslmode=disable"
  local temps_bin="$HOME_DIR/.temps/bin/temps"

  # Build the service environment once for both systemd and launchd, from:
  #   - telemetry opt-out (--no-telemetry) -> TEMPS_TELEMETRY=0
  #   - ClickHouse backend (step_clickhouse_optin) -> the four TEMPS_CLICKHOUSE_*
  #     vars, which `temps serve` reads to activate the ClickHouse backends.
  # Mirrors write_service_unit so quick/local installs get ClickHouse too.
  local systemd_extra_env=""        # newline-prefixed `Environment=K=V` lines
  local plist_env_pairs=""          # `    <key>K</key>\n    <string>V</string>` lines

  add_service_env() {
    local key="$1" val="$2"
    systemd_extra_env+=$'\n'"Environment=${key}=${val}"
    plist_env_pairs+="    <key>${key}</key>"$'\n'"    <string>${val}</string>"$'\n'
  }

  if [[ "$TELEMETRY_OPTOUT" == "true" ]]; then
    add_service_env "TEMPS_TELEMETRY" "0"
  fi
  if [[ "$CLICKHOUSE_ENABLED" == "true" && -n "$CLICKHOUSE_URL" ]]; then
    add_service_env "TEMPS_CLICKHOUSE_URL" "$CLICKHOUSE_URL"
    add_service_env "TEMPS_CLICKHOUSE_DATABASE" "$CLICKHOUSE_DATABASE"
    add_service_env "TEMPS_CLICKHOUSE_USER" "$CLICKHOUSE_USER"
    add_service_env "TEMPS_CLICKHOUSE_PASSWORD" "$CLICKHOUSE_PASSWORD"
  fi

  # Wrap the launchd pairs in a single EnvironmentVariables dict (only if any).
  local plist_env_block=""
  if [[ -n "$plist_env_pairs" ]]; then
    plist_env_block="  <key>EnvironmentVariables</key>"$'\n'"  <dict>"$'\n'"${plist_env_pairs}  </dict>"$'\n'
  fi

  if [[ "$IS_LINUX" == "true" ]]; then
    local tls_line=""
    [[ "$tls" == "true" ]] && tls_line="  --tls-address=\"0.0.0.0:443\" \\"
    $SUDO bash -c "cat > /etc/systemd/system/temps.service" << EOF
[Unit]
Description=Temps Platform Server
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=$RUN_USER
WorkingDirectory=$HOME_DIR/.temps
ExecStart=$temps_bin serve \\
  --address="0.0.0.0:${LOCAL_PORT}" \\
${tls_line:+$tls_line
}  --database-url="$db_url" \\
  --data-dir="$HOME_DIR/.temps/data" \\
  --console-address="0.0.0.0:${CONSOLE_PORT}" \\
  --disable-https-redirect
Restart=always
RestartSec=5
LimitNOFILE=65535
AmbientCapabilities=CAP_NET_BIND_SERVICE
Environment=HOME=$HOME_DIR$systemd_extra_env

[Install]
WantedBy=multi-user.target
EOF
    success "Systemd unit written to ${BOLD}/etc/systemd/system/temps.service${RESET}"

  elif [[ "$IS_MACOS" == "true" ]]; then
    mkdir -p "$HOME_DIR/Library/LaunchAgents"
    mkdir -p "$HOME_DIR/.temps/logs"
    local tls_arg=""
    [[ "$tls" == "true" ]] && tls_arg="    <string>--tls-address=0.0.0.0:443</string>"
    cat > "$HOME_DIR/Library/LaunchAgents/dev.temps.temps.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>dev.temps.temps</string>
  <key>ProgramArguments</key>
  <array>
    <string>$temps_bin</string>
    <string>serve</string>
    <string>--address=0.0.0.0:${LOCAL_PORT}</string>
${tls_arg:+$tls_arg
}    <string>--database-url=$db_url</string>
    <string>--data-dir=$HOME_DIR/.temps/data</string>
    <string>--console-address=0.0.0.0:${CONSOLE_PORT}</string>
    <string>--disable-https-redirect</string>
  </array>
${plist_env_block}  <key>WorkingDirectory</key>
  <string>$HOME_DIR/.temps</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$HOME_DIR/.temps/logs/temps.log</string>
  <key>StandardErrorPath</key>
  <string>$HOME_DIR/.temps/logs/temps.log</string>
</dict>
</plist>
EOF
    success "LaunchAgent written to ${BOLD}~/Library/LaunchAgents/dev.temps.temps.plist${RESET}"
  fi
}

# Ensure on-demand HTTP-01 TLS (ADR-018) is enabled so the proxy can issue
# per-host Let's Encrypt certs for the console and app aliases on a sslip.io
# install.
#
# `temps setup` auto-enables on-demand TLS for sslip.io zones (it writes
# `app_settings.on_demand_tls.enabled = true` directly to the DB) — but ONLY at
# setup time. An instance whose settings were written by an older binary (before
# the feature existed) stays disabled after a binary upgrade, because upgrading
# does not re-run the auto-enable. The symptom: quick mode binds :443, but with
# on-demand TLS off the proxy has no cert to serve and every HTTPS handshake
# fails.
#
# on_demand_tls is NOT exposed by the settings API (GET /api/settings omits it
# and PUT cannot carry it) — it is a setup-time/DB concern by design. So the
# self-heal re-runs `temps setup --auto` with the SAME admin email, the SAME
# stored password, and the SAME wildcard domain. That is idempotent: it resets
# the admin password to the identical value (no-op for the operator), preserves
# projects and the encryption key, and re-applies the sslip.io auto-enable via
# the server's own logic. The caller restarts the service afterward; we then
# confirm success by looking for the proxy's startup log line.
#
# Returns 0 iff the re-run completed (the caller restarts + verifies via logs).
# Returns non-zero if the re-run could not be performed, so the caller can fall
# back to HTTP instead of binding :443 with nothing to serve.
#
# Usage: ensure_on_demand_tls_enabled <temps_bin> <db_url>
ensure_on_demand_tls_enabled() {
  local temps_bin="$1" db_url="$2"

  # Re-running setup needs the same admin credentials so the password reset is a
  # no-op. deploy.sh stores both in state after the first setup.
  local admin_email admin_password
  admin_email=$(state_get admin_email)
  admin_password=$(state_get admin_password)
  [[ -z "$admin_email" ]] && admin_email="$ADMIN_EMAIL"
  [[ -z "$admin_password" ]] && admin_password="$ADMIN_PASSWORD"
  if [[ -z "$admin_email" || -z "$admin_password" ]]; then
    warn "Missing stored admin credentials — cannot safely re-run setup to enable on-demand TLS."
    return 1
  fi

  local external_url="http://${SSLIP_DOMAIN}${port_suffix}"

  # Carry the Let's Encrypt contact email through the re-run so the ACME contact
  # stays set (the binary has no fallback; an empty email means no cert issuance).
  local le_email
  le_email=$(state_get letsencrypt_email)
  [[ -z "$le_email" ]] && le_email="$LETSENCRYPT_EMAIL"
  local le_email_arg=()
  [[ -n "$le_email" ]] && le_email_arg=(--letsencrypt-email "$le_email")

  info "Enabling on-demand TLS for ${BOLD}${SSLIP_DOMAIN}${RESET} (re-applying setup)..."

  # Re-run setup with identical inputs. Idempotent: same admin password (no-op
  # reset), same wildcard domain, and the sslip.io auto-enable flips
  # on_demand_tls on in the DB. --skip-* are implied by --auto.
  local rerun_exit=0
  "$temps_bin" setup \
    --auto \
    --database-url "$db_url" \
    --admin-email "$admin_email" \
    --admin-password "$admin_password" \
    --wildcard-domain "*.${SSLIP_DOMAIN}" \
    --server-ip "$SERVER_IP" \
    --external-url "$external_url" \
    --data-dir "$HOME_DIR/.temps/data" \
    "${le_email_arg[@]+"${le_email_arg[@]}"}" \
    >/dev/null 2>&1 || rerun_exit=$?

  if [[ $rerun_exit -ne 0 ]]; then
    warn "Re-running setup to enable on-demand TLS failed (exit $rerun_exit)."
    return 1
  fi

  return 0
}

# Confirm the proxy actually started its on-demand TLS certificate manager, by
# scanning the service logs for the startup marker. Returns 0 if found.
# Usage: verify_on_demand_tls_active
verify_on_demand_tls_active() {
  local logs=""
  if check_command journalctl; then
    logs=$(journalctl -u temps --no-pager -n 400 2>/dev/null || true)
  elif [[ -f "$HOME_DIR/.temps/logs/temps.log" ]]; then
    logs=$(tail -n 400 "$HOME_DIR/.temps/logs/temps.log" 2>/dev/null || true)
  fi
  [[ -z "$logs" ]] && return 1
  echo "$logs" | grep -q "on-demand TLS enabled: certificate manager started"
}

run_quick_flow() {
  local mode_label="QuickStart"
  [[ "$SETUP_MODE" == "local" ]] && mode_label="Local"

  TOTAL_STEPS=5

  echo ""
  info "Setting up Temps in ${BOLD}$mode_label${RESET} mode."
  case "$SETUP_MODE" in
    local)
      info "Running on ${BOLD}this machine${RESET} via ${BOLD}127.0.0.1.sslip.io${RESET}, HTTP only — nothing exposed publicly."
      ;;
    quick)
      info "Instant ${BOLD}sslip.io${RESET} domain with automatic HTTPS — no domain or DNS configuration needed."
      info "The console and your apps get real Let's Encrypt certs on first request (on-demand TLS)."
      ;;
  esac
  echo ""

  if ! prompt_yesno "Ready to begin?" "y"; then
    echo ""
    info "Cancelled. Run this wizard again when you're ready."
    echo ""
    exit 0
  fi

  # --- Steps 1 & 2: Docker + database (shared with advanced mode) ---
  step_docker
  step_timescaledb

  # --- Step 3: Binary + sslip.io domain ---
  step_header 3 $TOTAL_STEPS "Temps Binary & Domain"

  # A previous run may have left a wrong-architecture binary on disk (e.g. it
  # downloaded temps-linux-amd64 on an aarch64 host) — file presence alone does
  # not mean it's usable, so drop it and force a fresh install rather than
  # silently limping forward with a binary that can't execute.
  if [[ -f $HOME_DIR/.temps/bin/temps ]] && ! "$HOME_DIR/.temps/bin/temps" --version &>/dev/null; then
    warn "Existing Temps binary at ${BOLD}$HOME_DIR/.temps/bin/temps${RESET} does not run on this machine — reinstalling."
    rm -f "$HOME_DIR/.temps/bin/temps"
  fi

  # Install the binary on the chosen channel (idempotent)
  if ! check_command temps && [[ ! -f $HOME_DIR/.temps/bin/temps ]]; then
    info "Installing Temps binary..."
    install_temps_binary "$TEMPS_VERSION"
    export PATH="$HOME_DIR/.temps/bin:$PATH"
    sudo_notice "to symlink the temps binary into /usr/local/bin (so 'temps' works in your shell)"
    $SUDO ln -sf $HOME_DIR/.temps/bin/temps /usr/local/bin/temps 2>/dev/null || true
  else
    success "Temps binary already installed"
  fi

  local temps_bin="$HOME_DIR/.temps/bin/temps"
  [[ ! -f "$temps_bin" ]] && temps_bin="$(command -v temps)"

  if ! "$temps_bin" --version &>/dev/null; then
    error "The Temps binary at ${BOLD}$temps_bin${RESET} does not run on this machine."
    fatal "Cannot continue without a working Temps binary"
  fi

  # Resolve the sslip.io domain. Local mode pins the loopback address so the
  # whole platform stays on this machine; other modes use the public IP.
  local http_pref=80
  if [[ "$SETUP_MODE" == "local" ]]; then
    SERVER_IP="127.0.0.1"
    # Linux systemd grants CAP_NET_BIND_SERVICE so :80 works even unprivileged;
    # macOS launchd user agents cannot bind privileged ports, so prefer :8080.
    [[ "$IS_MACOS" == "true" ]] && http_pref=8080
  else
    info "Detecting server IP..."
    SERVER_IP=$(detect_public_ip_quick)
  fi
  # Pick free HTTP/console ports (a running Temps on 8080/8081 won't block us).
  # Local/quick mode is HTTP-only up front (TLS is on-demand), so prefer a high
  # TLS port that won't collide; it isn't bound as a listener here.
  resolve_service_ports "$http_pref" 8443
  # Dashed IP, not dotted. sslip.io locates the target address by scanning the
  # hostname for four numeric components joined by a *single* separator style
  # (all dots or all dashes) and taking the leftmost match, unanchored to the
  # base domain. With a dotted base, any generated label ending in a number
  # donates it to the front of the IP and the name resolves elsewhere entirely:
  #
  #   observability-starter-1.127.0.0.1.sslip.io -> 1.127.0.0   (not this host)
  #   pr-42.127.0.0.1.sslip.io                   -> 42.127.0.0  (not this host)
  #
  # Temps deployment slugs are {project}-{n} and preview environments are
  # pr-{number}, so on a dotted base that is every generated app hostname.
  # The dashed form makes the separator styles disagree (`1.127-0-0` mixes a
  # dot and dashes, so it is rejected) and the real `127-0-0-1` wins.
  SSLIP_DOMAIN="${SERVER_IP//./-}.sslip.io"

  local port_suffix=""
  [[ "$LOCAL_PORT" != "80" ]] && port_suffix=":${LOCAL_PORT}"

  success "Using domain: ${BOLD}*.${SSLIP_DOMAIN}${RESET}"
  info "Console will be at ${BOLD}console.${SSLIP_DOMAIN}${port_suffix}${RESET}"
  echo ""
  state_set domain "$SSLIP_DOMAIN"
  state_set server_ip "$SERVER_IP"
  state_set local_port "$LOCAL_PORT"

  # --- Step 4: temps setup --auto ---
  step_header 4 $TOTAL_STEPS "Temps Platform Setup"

  local db_url="postgresql://temps:${DB_PASSWORD}@127.0.0.1:${DB_PORT}/temps?sslmode=disable"
  mkdir -p "$HOME_DIR/.temps/data"

  ADMIN_EMAIL=$(state_get admin_email)
  ADMIN_PASSWORD=$(state_get admin_password)
  LETSENCRYPT_EMAIL=$(state_get letsencrypt_email)

  # "Already configured" requires BOTH the host-side encryption key AND an admin
  # user that actually exists in the database. The two can drift apart across a
  # deploy → undeploy → deploy cycle (host data dir kept, DB volume reset, or
  # vice-versa); when they do, fall through to the full seeding setup below so
  # the server never boots into the interactive admin-email prompt and dies.
  if [[ -f $HOME_DIR/.temps/data/encryption_key ]] && [[ -n "$ADMIN_PASSWORD" ]] \
       && db_has_admin_user; then
    success "Temps platform already configured"
    [[ -n "$ADMIN_EMAIL" ]] && info "Admin: ${BOLD}$ADMIN_EMAIL${RESET}"

    # The stored external_url was written on the FIRST run with whatever port was
    # free then. If the resolved HTTP port changed since (e.g. another process
    # took 8080, so we bumped to 8084), the DB still advertises the old port and
    # OAuth callbacks / app links break. Reconcile it on every re-run. `temps
    # setup --auto` only upserts settings here (encryption key already exists),
    # so this is a cheap, idempotent way to refresh external_url + preview domain.
    local external_url="http://${SSLIP_DOMAIN}${port_suffix}"
    local stored_external_url=""
    stored_external_url=$(state_get external_url)
    if [[ "$stored_external_url" != "$external_url" ]]; then
      local le_email_arg=()
      [[ -n "$LETSENCRYPT_EMAIL" ]] && le_email_arg=(--letsencrypt-email "$LETSENCRYPT_EMAIL")
      if spinner "Updating external URL to ${external_url}..." \
        "$temps_bin" setup \
          --auto \
          --database-url "$db_url" \
          --admin-email "${ADMIN_EMAIL:-admin@${SSLIP_DOMAIN}}" \
          --admin-password "$ADMIN_PASSWORD" \
          --wildcard-domain "*.${SSLIP_DOMAIN}" \
          --server-ip "$SERVER_IP" \
          --external-url "$external_url" \
          --data-dir "$HOME_DIR/.temps/data" \
          "${le_email_arg[@]+"${le_email_arg[@]}"}"; then
        state_set external_url "$external_url"
        success "External URL set to ${BOLD}${external_url}${RESET}"
      else
        warn "Could not update external URL (non-fatal). Set it in Settings → External URL."
      fi
      echo ""
    fi
  else
    # Quick mode serves the console + apps over HTTPS via on-demand Let's
    # Encrypt. ACME needs a real contact email and the binary has NO fallback,
    # so require one up front. We reuse it as the admin login email too, so the
    # operator ends up with a single real address. Local mode stays HTTP (Let's
    # Encrypt can't reach a loopback box), so the email is optional there.
    if [[ "$SETUP_MODE" == "quick" ]]; then
      # Require a real, dotted email. Held in a variable because bash =~ treats
      # backslash escapes in inline patterns inconsistently; [.] matches a literal
      # dot. This rejects dotless hosts like system@localhost / admin@localhost.
      local email_re='^[^@[:space:]]+@[^@[:space:]]+[.][^@[:space:]]+$'
      while [[ -z "$LETSENCRYPT_EMAIL" ]]; do
        prompt_input "Email for Let's Encrypt / HTTPS certificates (required)" "" LETSENCRYPT_EMAIL
        if [[ ! "$LETSENCRYPT_EMAIL" =~ $email_re ]]; then
          warn "Please enter a valid email address (e.g. you@example.com)."
          LETSENCRYPT_EMAIL=""
        fi
      done
      ADMIN_EMAIL="$LETSENCRYPT_EMAIL"
    fi

    [[ -z "$ADMIN_EMAIL" ]] && ADMIN_EMAIL="admin@${SSLIP_DOMAIN}"
    ADMIN_PASSWORD=$(generate_admin_password)

    # The external URL carries the proxy port when it isn't 80 (local mode on
    # macOS uses :8080), so generated app/console links are correct.
    local external_url="http://${SSLIP_DOMAIN}${port_suffix}"
    # Only pass --letsencrypt-email when we have one (quick mode). It populates
    # settings.letsencrypt.email, the single source of truth for the ACME
    # contact — without it on-demand HTTPS issuance can never succeed.
    local le_email_arg=()
    [[ -n "$LETSENCRYPT_EMAIL" ]] && le_email_arg=(--letsencrypt-email "$LETSENCRYPT_EMAIL")
    # Pass the domain/IP explicitly so deploy.sh stays the source of truth
    # (it already detected the IP for the reachability probe + completion
    # screen). --auto still forces skip-ssl/skip-dns/skip-git and generates an
    # HTTP-only config; we supply --external-url because providing an explicit
    # --wildcard-domain bypasses --auto's own external-URL defaulting.
    local setup_exit=0
    spinner "Configuring Temps platform..." \
      "$temps_bin" setup \
        --auto \
        --database-url "$db_url" \
        --admin-email "$ADMIN_EMAIL" \
        --admin-password "$ADMIN_PASSWORD" \
        --wildcard-domain "*.${SSLIP_DOMAIN}" \
        --server-ip "$SERVER_IP" \
        --external-url "$external_url" \
        --data-dir "$HOME_DIR/.temps/data" \
        "${le_email_arg[@]+"${le_email_arg[@]}"}" \
      || setup_exit=$?
    echo ""

    if [[ $setup_exit -ne 0 ]]; then
      echo ""
      warn "Temps setup failed (exit code $setup_exit). Relevant output:"
      grep -Ev '^\s*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}' \
        /tmp/temps-wizard-cmd-out.log 2>/dev/null \
        | while IFS= read -r line; do
            [[ -n "$line" ]] && printf "  ${DIM}  %s${RESET}\n" "$line"
          done
      echo ""
      diagnose_setup_failure /tmp/temps-wizard-cmd-out.log
      fatal "Setup cannot continue"
    fi
    state_set admin_email "$ADMIN_EMAIL"
    state_set admin_password "$ADMIN_PASSWORD"
    state_set external_url "$external_url"
    [[ -n "$LETSENCRYPT_EMAIL" ]] && state_set letsencrypt_email "$LETSENCRYPT_EMAIL"
  fi

  # Sync encryption key to where `temps serve` looks for it
  if [[ -f $HOME_DIR/.temps/data/encryption_key ]]; then
    cp $HOME_DIR/.temps/data/encryption_key $HOME_DIR/.temps/encryption_key 2>/dev/null || true
  fi

  # `temps setup` downloads GeoLite2 into the data dir, but `temps serve`'s geo
  # plugin opens GeoLite2-City.mmdb relative to its working directory
  # ($HOME_DIR/.temps). Bridge that gap or serve crash-loops with
  # "Failed to open MaxMind database".
  ensure_geolite2

  # --- Optional: ClickHouse backend (available in every mode) ---
  # Must run BEFORE the service unit is written so the TEMPS_CLICKHOUSE_* env
  # vars are injected into the systemd unit / launchd plist.
  echo ""
  step_clickhouse_optin

  # --- Step 5: Background service ---
  step_header 5 $TOTAL_STEPS "Background Service"

  # Start HTTP-only first. The console API (:8081) is bound regardless of the
  # :443 TLS listener, so we bring the service up without TLS, confirm on-demand
  # TLS is actually enabled in settings, and only THEN rewrite the unit with
  # :443. This avoids the failure mode where :443 is bound but on-demand TLS is
  # off in the DB (e.g. settings written by an older binary) — the proxy would
  # then have no cert to serve and every HTTPS handshake would fail.
  write_quick_service_unit "false"
  service_enable temps
  if ! service_start temps; then
    warn "Service failed to start. Retrying..."
    sleep 3
    service_restart temps
  fi

  echo ""
  info "Waiting for Temps to start..."
  local healthy=false
  for i in $(seq 1 20); do
    progress_bar "$i" 20 "checking health"
    if curl -sf "http://localhost:${CONSOLE_PORT}/health" >/dev/null 2>&1; then
      healthy=true
      break
    fi
    sleep 3
  done
  progress_bar 20 20 "checking health"
  echo ""
  if [[ "$healthy" == "true" ]]; then
    success "Temps service is running and healthy"
  else
    warn "Temps did not pass its health check within the timeout."
    dump_service_logs temps 40
    if dump_service_logs temps 60 2>/dev/null | grep -q "password authentication failed"; then
      error "The server cannot authenticate to PostgreSQL."
      info "The data volume likely holds an older password. Reconcile it with:"
      info "  ${BOLD}docker exec temps-timescaledb psql -U temps -d temps -c \"ALTER USER temps WITH PASSWORD '\$(cat $HOME_DIR/.temps/.wizard-state/db_password)';\"${RESET}"
      info "  ${BOLD}$(service_restart_cmd temps)${RESET}"
    else
      info "It may just need a few more seconds. Watch it with:"
      info "  ${BOLD}$(service_logs_cmd temps)${RESET}"
    fi
  fi
  echo ""

  # Console scheme defaults to HTTP. Quick mode upgrades to HTTPS only after
  # confirming on-demand TLS is enabled (self-healing if `temps setup` left it
  # off on an upgraded install), then rebinds the service with :443. Local mode
  # stays HTTP — Let's Encrypt cannot reach a loopback box for the challenge.
  local console_scheme="http"
  if [[ "$SETUP_MODE" == "quick" ]]; then
    if [[ "$healthy" == "true" ]] && ensure_on_demand_tls_enabled "$temps_bin" "$db_url"; then
      # On-demand TLS is now enabled in the DB. Rewrite the unit with the :443
      # TLS listener and restart so the proxy binds :443 AND boots its on-demand
      # certificate manager. Then confirm the manager actually started (log
      # marker) before committing to the HTTPS console scheme — if it didn't,
      # fall back to HTTP rather than leaving :443 with no cert.
      write_quick_service_unit "true"
      service_enable temps
      service_restart temps

      echo ""
      local tls_active=false
      info "Waiting for the on-demand TLS certificate manager to start..."
      for i in $(seq 1 10); do
        progress_bar "$i" 10 "starting cert manager"
        if verify_on_demand_tls_active; then
          tls_active=true
          break
        fi
        sleep 2
      done
      progress_bar 10 10 "done"
      echo ""

      if [[ "$tls_active" == "true" ]]; then
        console_scheme="https"
        success "On-demand TLS is active — the console and apps will get HTTPS on first request"
        echo ""
      else
        warn "On-demand TLS did not start — serving the console over HTTP."
        info "Check logs: ${BOLD}$(service_logs_cmd temps)${RESET}"
        # Re-bind HTTP-only so we don't leave :443 advertised without a cert.
        write_quick_service_unit "false"
        service_restart temps
        sleep 2
      fi
    else
      warn "Could not enable on-demand TLS — serving the console over HTTP."
      info "Ensure ports 80/443 are reachable, then re-run the installer to retry."
      info "See: ${BOLD}https://temps.sh/docs${RESET}"
      echo ""
    fi
  fi

  local console_url="${console_scheme}://console.${SSLIP_DOMAIN}${port_suffix}"

  # Verify the console responds before declaring success.
  #
  # In quick mode the console cert is issued on demand: the FIRST HTTPS request
  # to console.<zone> triggers HTTP-01 issuance (the proxy presents NO fallback
  # cert, so until the real cert is active the handshake fails fast — `curl -sk`
  # returns 000). A 2xx/3xx over HTTPS therefore PROVES the console cert was
  # actually provisioned (curl -k bypasses validation, not the need for a cert
  # to handshake at all). The loop below keeps requesting to both trigger and
  # confirm issuance.
  echo ""
  info "Verifying the console responds at ${BOLD}${console_url}${RESET}..."
  if [[ "$console_scheme" == "https" ]]; then
    info "${DIM}The first request triggers certificate issuance and may fail — this is expected.${RESET}"
  fi
  local verified=false
  for i in $(seq 1 20); do
    progress_bar "$i" 20 "waiting for response"
    local code
    code=$(curl -sk -o /dev/null -w "%{http_code}" "$console_url" 2>/dev/null || echo "000")
    if [[ "$code" =~ ^[2-3][0-9][0-9]$ ]]; then
      verified=true
      break
    fi
    sleep 3
  done
  progress_bar 20 20 "done"
  echo ""
  if [[ "$verified" == "true" ]]; then
    if [[ "$console_scheme" == "https" ]]; then
      success "Console is live and its HTTPS certificate is provisioned"
    else
      success "Console is live"
    fi
    echo ""
  elif [[ "$console_scheme" == "https" ]]; then
    # HTTPS console never responded → the console certificate did NOT provision.
    # Surface the actual reason from the on-demand issuance logs instead of a
    # vague "try again", since the common causes are operator-fixable (port 80
    # blocked for the HTTP-01 challenge, or a Let's Encrypt rate limit).
    warn "The console HTTPS certificate did not provision within the wait window."
    local issue_log=""
    if check_command journalctl; then
      issue_log=$(journalctl -u temps --no-pager -n 400 2>/dev/null \
        | grep "on-demand TLS: issuance failed" | tail -1 || true)
    elif [[ -f "$HOME_DIR/.temps/logs/temps.log" ]]; then
      issue_log=$(grep "on-demand TLS: issuance failed" "$HOME_DIR/.temps/logs/temps.log" 2>/dev/null | tail -1 || true)
    fi
    if [[ -n "$issue_log" ]]; then
      local category
      category=$(echo "$issue_log" | sed -n 's/.*error_category=\([a-z_]*\).*/\1/p')
      case "$category" in
        rate_limited) warn "Reason: Let's Encrypt rate limit. Wait and reload, or use a custom domain (Advanced mode)." ;;
        dns_failure)  warn "Reason: DNS/validation failure. Confirm ${BOLD}console.${SSLIP_DOMAIN}${RESET} resolves to ${BOLD}${SERVER_IP}${RESET}." ;;
        timeout|challenge_mismatch)
          warn "Reason: HTTP-01 challenge failed (${category:-unknown})."
          info "Let's Encrypt must reach this server on ${BOLD}port 80${RESET} — open it in your firewall / cloud security group, then reload."
          ;;
        *) warn "Reason: ${category:-see logs}. ${DIM}$(service_logs_cmd temps)${RESET}" ;;
      esac
    else
      # No explicit failure logged — most likely the challenge can't reach us.
      info "Most likely ${BOLD}port 80${RESET} (HTTP-01 challenge) or ${BOLD}443${RESET} is not reachable from the internet."
      info "Open ports 80 and 443 in your firewall / cloud security group, then reload ${BOLD}${console_url}${RESET}."
    fi
    info "Inspect issuance logs: ${BOLD}$(service_logs_cmd temps) | grep on-demand${RESET}"
    echo ""
  else
    warn "Console did not respond yet — it may need a few more seconds."
    echo ""
  fi

  # Headless installs (--yes) mint an admin API key up front so the
  # machine-readable result is immediately usable for CLI automation —
  # interactive users can create keys from the console instead.
  [[ "$ASSUME_YES" == "true" ]] && ensure_api_key

  # The full end-to-end test deploy (step_test_deploy) assumes an HTTPS custom
  # domain, so it only runs in advanced mode. Local/quick rely on the health
  # check above plus the next-steps guidance below.
  show_quick_completion "$console_scheme" "$port_suffix"
}

# Mode-aware completion screen for the local/quick flow.
# Usage: show_quick_completion <console_scheme: http|https> [port_suffix e.g. ":8080"]
show_quick_completion() {
  local scheme="${1:-http}"
  local port_suffix="${2:-}"
  local console_url="${scheme}://console.${SSLIP_DOMAIN}${port_suffix}"
  # Apps share the console scheme: quick mode certs every <host>.<ip>.sslip.io
  # on demand, so they are reachable over HTTPS too; local mode stays HTTP.
  local apps_url="${scheme}://<project>.${SSLIP_DOMAIN}${port_suffix}"
  local is_local=false
  [[ "$SETUP_MODE" == "local" ]] && is_local=true

  echo ""
  hr
  echo ""
  printf "  ${BG_GREEN}${BOLD}${WHITE} SETUP COMPLETE ${RESET}\n"
  echo ""
  printf "  ${BOLD}Your Temps instance is ready!${RESET}\n"
  echo ""
  summary_row "Console:" "$console_url"
  summary_row "Apps at:" "$apps_url"
  summary_row "Admin email:" "$ADMIN_EMAIL"
  summary_row "Admin password:" "$ADMIN_PASSWORD"
  summary_row "Domain:" "*.${SSLIP_DOMAIN}"
  if [[ -n "$TEMPS_VERSION" ]]; then
    summary_row "Version:" "$TEMPS_VERSION (pinned)"
  else
    summary_row "Channel:" "$CHANNEL"
  fi
  echo ""
  warn "Save your admin password now — it won't be shown again."
  info "${DIM}It's also stored at $STATE_DIR/admin_password${RESET}"
  echo ""

  hr
  echo ""
  printf "  ${BOLD}About this setup${RESET}\n"
  echo ""
  if [[ "$is_local" == "true" ]]; then
    info "Temps is running on ${BOLD}this machine${RESET} via ${BOLD}127.0.0.1.sslip.io${RESET},"
    info "which resolves the console and every app subdomain to ${BOLD}127.0.0.1${RESET}."
    info "Nothing is exposed to the internet — this is for local dogfooding."
  else
    info "You're using a free ${BOLD}sslip.io${RESET} domain that maps ${BOLD}*.${SSLIP_DOMAIN}${RESET}"
    info "to this server's IP (${BOLD}${SERVER_IP}${RESET}) — no DNS configuration required."
    if [[ "$scheme" == "https" ]]; then
      echo ""
      info "The console and your apps get real Let's Encrypt certificates"
      info "automatically via ${BOLD}on-demand TLS${RESET}: the proxy issues a per-host"
      info "certificate the first time each ${BOLD}<host>.${SSLIP_DOMAIN}${RESET} is opened over"
      info "HTTPS. The very first request to a new host can fail while the cert is"
      info "issued (a few seconds) — just reload."
      echo ""
      info "Heads up: sslip.io shares a Let's Encrypt rate-limit bucket. For"
      info "production, move to your own domain (Advanced mode) and a wildcard cert."
    else
      echo ""
      info "Everything is served over ${BOLD}HTTP${RESET} for now. That's fine for trying"
      info "Temps out, but use a real domain before exposing anything publicly."
    fi
  fi
  echo ""

  if [[ "$is_local" == "true" ]]; then
    hr
    echo ""
    printf "  ${BOLD}Going beyond local${RESET}\n"
    echo ""
    info "When you're ready to host this for real, re-run the installer on a"
    info "server with a public IP:"
    info "     ${GREEN}curl -fsSL https://temps.sh/deploy.sh | bash -s -- --mode quick${RESET}     ${DIM}# instant sslip.io${RESET}"
    info "     ${GREEN}curl -fsSL https://temps.sh/deploy.sh | bash -s -- --mode advanced${RESET}  ${DIM}# your own domain${RESET}"
    echo ""
  else
    hr
    echo ""
    printf "  ${BOLD}Add a real domain when you're ready${RESET}\n"
    echo ""
    info "1. Point your domain's DNS at this server (${BOLD}${SERVER_IP}${RESET}):"
    info "     ${DIM}A     yourdomain.com        → ${SERVER_IP}${RESET}"
    info "     ${DIM}A     *.yourdomain.com      → ${SERVER_IP}${RESET}"
    info "2. Add the domain and provision an HTTPS certificate:"
    info "     ${GREEN}bunx @temps-sdk/cli domains add --domain yourdomain.com${RESET}"
    info "     ${GREEN}bunx @temps-sdk/cli domains verify --domain yourdomain.com${RESET}   ${DIM}# HTTP-01 cert${RESET}"
    info "   ${DIM}or, for a wildcard cert, re-run this installer in Advanced mode:${RESET}"
    info "     ${GREEN}curl -fsSL https://temps.sh/deploy.sh | bash -s -- --mode advanced${RESET}"
    info "3. In the console, point a project at your domain under ${BOLD}Project → Domains${RESET}."
    echo ""
  fi

  hr
  echo ""
  printf "  ${BOLD}Next steps${RESET}\n"
  echo ""
  info "1. Open your console at ${GREEN}${UNDERLINE}${console_url}${RESET}"
  info "2. Log in with ${BOLD}$ADMIN_EMAIL${RESET} and your password"
  info "3. Deploy your first app with ${GREEN}temps deploy${RESET}"
  echo ""

  hr
  echo ""
  printf "  ${BOLD}Useful commands${RESET}\n"
  echo ""
  info "${GREEN}$(service_status_cmd temps)${RESET}   ${DIM}Service status${RESET}"
  info "${GREEN}$(service_logs_cmd temps)${RESET}   ${DIM}Live logs${RESET}"
  info "${GREEN}temps --help${RESET}   ${DIM}CLI reference${RESET}"
  echo ""

  hr
  echo ""
  info "Documentation: ${UNDERLINE}https://temps.sh/docs${RESET}"
  info "Support:       ${UNDERLINE}https://github.com/gotempsh/temps/issues${RESET}"
  echo ""

  # Final access box — shown last so credentials are always visible on screen
  hr
  echo ""
  printf "  ${BG_BLUE}${BOLD}${WHITE} YOUR ACCESS DETAILS ${RESET}\n"
  echo ""
  printf "  ${BOLD}%-20s${RESET} ${GREEN}${UNDERLINE}%s${RESET}\n" "Console URL:" "$console_url"
  printf "  ${BOLD}%-20s${RESET} %s\n" "Email:" "$ADMIN_EMAIL"
  printf "  ${BOLD}%-20s${RESET} ${BOLD}%s${RESET}\n" "Password:" "$ADMIN_PASSWORD"
  echo ""
  warn "Save your password now — also stored at ${DIM}$STATE_DIR/admin_password${RESET}"
  echo ""

  write_setup_result "$console_url" "$apps_url" "$SSLIP_DOMAIN"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

check_prerequisites() {
  local missing=()

  check_command curl    || missing+=("curl")
  check_command openssl || missing+=("openssl")

  if [[ ${#missing[@]} -eq 0 ]]; then
    return 0
  fi

  warn "Missing required tools: ${BOLD}${missing[*]}${RESET}"

  if check_command brew; then
    info "Installing via Homebrew..."
    brew install "${missing[@]}" > /dev/null 2>&1 || true
  elif check_command apt-get; then
    info "Installing via apt..."
    $SUDO apt-get update -qq > /dev/null 2>&1 || true
    $SUDO apt-get install -y -qq "${missing[@]}" > /dev/null 2>&1 || true
  elif check_command yum; then
    info "Installing via yum..."
    $SUDO yum install -y -q "${missing[@]}" > /dev/null 2>&1 || true
  elif check_command apk; then
    info "Installing via apk..."
    $SUDO apk add --quiet "${missing[@]}" > /dev/null 2>&1 || true
  fi

  # Re-check after install attempt
  local still_missing=()
  for cmd in "${missing[@]}"; do
    check_command "$cmd" || still_missing+=("$cmd")
  done

  if [[ ${#still_missing[@]} -gt 0 ]]; then
    fatal "Could not install: ${BOLD}${still_missing[*]}${RESET}. Install them manually and re-run."
  fi

  success "Installed missing dependencies: ${BOLD}${missing[*]}${RESET}"
}

# Parse CLI flags: --mode <local|quick|advanced>, --channel <stable|beta|nightly>,
# and --version <tag>. All also accept the --flag=value form. Unknown flags are
# rejected so typos don't silently fall through to the interactive flow.
parse_flags() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --mode)       SETUP_MODE="${2:-}"; shift 2 || fatal "--mode requires a value (local, quick, or advanced)" ;;
      --mode=*)     SETUP_MODE="${1#*=}"; shift ;;
      --channel)    CHANNEL="${2:-}"; shift 2 || fatal "--channel requires a value (stable, beta, or nightly)" ;;
      --channel=*)  CHANNEL="${1#*=}"; shift ;;
      --version)    TEMPS_VERSION="${2:-}"; shift 2 || fatal "--version requires a release tag (e.g. v0.1.0)" ;;
      --version=*)  TEMPS_VERSION="${1#*=}"; shift ;;
      --no-telemetry) TELEMETRY_OPTOUT="true"; shift ;;
      --domain)     FLAG_DOMAIN="${2:-}"; shift 2 || fatal "--domain requires a value (e.g. example.com)" ;;
      --domain=*)   FLAG_DOMAIN="${1#*=}"; shift ;;
      --email)      FLAG_EMAIL="${2:-}"; shift 2 || fatal "--email requires a value (e.g. you@example.com)" ;;
      --email=*)    FLAG_EMAIL="${1#*=}"; shift ;;
      --dns-provider)  FLAG_DNS_PROVIDER="${2:-}"; shift 2 || fatal "--dns-provider requires a value (cloudflare, route53, or digitalocean)" ;;
      --dns-provider=*) FLAG_DNS_PROVIDER="${1#*=}"; shift ;;
      --cloudflare-token)  FLAG_CLOUDFLARE_TOKEN="${2:-}"; shift 2 || fatal "--cloudflare-token requires a value" ;;
      --cloudflare-token=*) FLAG_CLOUDFLARE_TOKEN="${1#*=}"; shift ;;
      --aws-access-key-id)  FLAG_AWS_ACCESS_KEY_ID="${2:-}"; shift 2 || fatal "--aws-access-key-id requires a value" ;;
      --aws-access-key-id=*) FLAG_AWS_ACCESS_KEY_ID="${1#*=}"; shift ;;
      --aws-secret-access-key)  FLAG_AWS_SECRET_ACCESS_KEY="${2:-}"; shift 2 || fatal "--aws-secret-access-key requires a value" ;;
      --aws-secret-access-key=*) FLAG_AWS_SECRET_ACCESS_KEY="${1#*=}"; shift ;;
      --aws-region)  FLAG_AWS_REGION="${2:-}"; shift 2 || fatal "--aws-region requires a value" ;;
      --aws-region=*) FLAG_AWS_REGION="${1#*=}"; shift ;;
      --digitalocean-token)  FLAG_DIGITALOCEAN_TOKEN="${2:-}"; shift 2 || fatal "--digitalocean-token requires a value" ;;
      --digitalocean-token=*) FLAG_DIGITALOCEAN_TOKEN="${1#*=}"; shift ;;
      --yes|-y|--non-interactive) ASSUME_YES="true"; shift ;;
      -h|--help)
        echo "Usage: deploy.sh [--mode local|quick|advanced] [--channel stable|beta|nightly] [--version <tag>]"
        echo "                 [--email <address>] [--domain <domain>] [--dns-provider cloudflare|route53|digitalocean]"
        echo "                 [--cloudflare-token <token>] [--aws-access-key-id <id>] [--aws-secret-access-key <key>]"
        echo "                 [--aws-region <region>] [--digitalocean-token <token>] [--yes] [--no-telemetry]"
        echo ""
        echo "  --version <tag>  Install a specific Temps release (e.g. v0.1.0-beta.30)"
        echo "                   instead of the newest on the channel. A pinned version"
        echo "                   ignores --channel entirely."
        echo "  --email <address>"
        echo "                   Pre-answer the email prompts: the Let's Encrypt contact"
        echo "                   address and the admin login email."
        echo "  --domain <domain>"
        echo "                   Pre-answer the domain prompt (advanced mode)."
        echo "  --dns-provider cloudflare|route53|digitalocean"
        echo "                   Advanced mode only: provision the wildcard certificate's"
        echo "                   DNS-01 challenge automatically via this provider's API"
        echo "                   instead of pasting a TXT record by hand. Requires the"
        echo "                   matching credential flag below (or its env var fallback)."
        echo "  --cloudflare-token <token>       (env: CLOUDFLARE_API_TOKEN)"
        echo "  --aws-access-key-id <id>         (env: AWS_ACCESS_KEY_ID)"
        echo "  --aws-secret-access-key <key>    (env: AWS_SECRET_ACCESS_KEY)"
        echo "  --aws-region <region>            (env: AWS_REGION, default us-east-1)"
        echo "  --digitalocean-token <token>     (env: DIGITALOCEAN_API_TOKEN)"
        echo "  --yes, -y, --non-interactive"
        echo "                   Accept every confirmation's default answer (headless"
        echo "                   install). Quick mode requires --email with this flag."
        echo "                   Advanced mode without --dns-provider still needs a"
        echo "                   terminal: manual DNS-01 validation pauses while you add"
        echo "                   a TXT record."
        echo "  --no-telemetry   Disable anonymous product telemetry (opt-out)."
        echo "                   Telemetry is anonymous and on by default; this sets"
        echo "                   TEMPS_TELEMETRY=0 in the service."
        echo ""
        echo "Headless QuickStart example (run on the server, e.g. over SSH):"
        echo "  bash deploy.sh --mode quick --email you@example.com --yes"
        echo ""
        echo "Headless Advanced example with automatic DNS-01 (no manual TXT records):"
        echo "  bash deploy.sh --mode advanced --domain example.com --email you@example.com \\"
        echo "    --dns-provider cloudflare --cloudflare-token \$CLOUDFLARE_API_TOKEN --yes"
        exit 0
        ;;
      *) fatal "Unknown argument: $1" ;;
    esac
  done

  if [[ -n "$FLAG_DNS_PROVIDER" ]]; then
    case "$FLAG_DNS_PROVIDER" in
      cloudflare|route53|digitalocean) ;;
      *) fatal "Invalid --dns-provider '$FLAG_DNS_PROVIDER'. Valid providers: cloudflare, route53, digitalocean" ;;
    esac
  fi

  case "$CHANNEL" in
    stable|beta|nightly) ;;
    *) fatal "Invalid --channel '$CHANNEL'. Valid channels: stable, beta, nightly" ;;
  esac

  # A pinned version must look like a release tag (vX.Y.Z, optional -suffix).
  # This catches typos early instead of failing on a 404 download.
  if [[ -n "$TEMPS_VERSION" && ! "$TEMPS_VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+([.-][A-Za-z0-9.]+)?$ ]]; then
    fatal "Invalid --version '$TEMPS_VERSION'. Expected a release tag like v0.1.0 or v0.1.0-beta.30."
  fi

  # Validate --email up front with the same rule as the interactive prompt
  # (a real, dotted address — Let's Encrypt rejects dotless hosts), so a typo
  # fails immediately instead of mid-install. Seed the Let's Encrypt email so
  # quick mode's required prompt is already answered.
  if [[ -n "$FLAG_EMAIL" ]]; then
    local flag_email_re='^[^@[:space:]]+@[^@[:space:]]+[.][^@[:space:]]+$'
    if [[ ! "$FLAG_EMAIL" =~ $flag_email_re ]]; then
      fatal "Invalid --email '$FLAG_EMAIL'. Expected a real address like you@example.com."
    fi
    LETSENCRYPT_EMAIL="$FLAG_EMAIL"
  fi

  if [[ "$ASSUME_YES" == "true" && "${SETUP_MODE:-}" == "quick" && -z "$FLAG_EMAIL" ]]; then
    fatal "Quick mode with --yes requires --email <address> (Let's Encrypt needs a contact address and there is no fallback)."
  fi

  if [[ -n "$SETUP_MODE" ]]; then
    case "$SETUP_MODE" in
      local|quick|advanced) ;;
      # `testing` was folded into `quick` (on-demand TLS now certs the console
      # automatically). Accept it as a deprecated alias so existing scripts and
      # docs keep working instead of hard-failing.
      testing)
        warn "--mode testing is deprecated; it now behaves the same as 'quick' (on-demand TLS certs the console automatically). Using 'quick'."
        SETUP_MODE="quick"
        ;;
      *) fatal "Invalid --mode '$SETUP_MODE'. Valid modes: local, quick, advanced" ;;
    esac
  fi
}

# Interactive mode picker — shown only when --mode was not supplied.
# Detects a public IP and pre-selects QuickStart when the server is
# reachable from the internet.
choose_mode() {
  [[ -n "$SETUP_MODE" ]] && return 0

  # Try to detect a public IPv4 (non-loopback, non-RFC-1918)
  local detected_ip="" default_choice=1 nat_detected=false local_ip=""
  detected_ip=$(curl -4 -sf --max-time 5 https://api.ipify.org 2>/dev/null \
    || curl -4 -sf --max-time 5 https://ifconfig.me 2>/dev/null || true)

  if [[ -n "$detected_ip" ]] && \
     [[ ! "$detected_ip" =~ ^127\. ]] && \
     [[ ! "$detected_ip" =~ ^10\. ]] && \
     [[ ! "$detected_ip" =~ ^172\.(1[6-9]|2[0-9]|3[01])\. ]] && \
     [[ ! "$detected_ip" =~ ^192\.168\. ]]; then
    # An internet echo service reporting a non-private IP only proves that's
    # the address the *router* in front of us is seen as — not that traffic
    # to it reaches this machine. Compare against our own interface IP: if
    # they differ, we're behind a NAT/router and QuickStart's sslip.io domain
    # will only work once that router forwards ports 80/443 here.
    local_ip=$(detect_local_ip)
    if [[ -n "$local_ip" ]] && [[ "$local_ip" != "$detected_ip" ]]; then
      nat_detected=true
    else
      default_choice=2
    fi
  fi

  echo ""
  printf "  ${BOLD}How would you like to set up Temps?${RESET}\n"
  echo ""
  if [[ "$nat_detected" == "true" ]]; then
    warn "Public IP detected: ${BOLD}${detected_ip}${RESET}${YELLOW}, but this machine's local address is ${BOLD}${local_ip}${RESET}${YELLOW} — you're likely behind a router/NAT."
    warn "QuickStart's ${BOLD}${detected_ip}.sslip.io${RESET}${YELLOW} domain only works if ports 80 and 443 are forwarded to this machine on that router."
    echo ""
  elif [[ $default_choice -eq 2 ]]; then
    info "Public IP detected: ${BOLD}${detected_ip}${RESET} — QuickStart is recommended."
    echo ""
  fi
  printf "    ${CYAN}1)${RESET}  Local       — run on this machine via 127.0.0.1.sslip.io, HTTP only (try it out)\n"
  if [[ $default_choice -eq 2 ]]; then
    printf "    ${CYAN}2)${RESET}  ${BOLD}QuickStart${RESET}  — instant ${BOLD}%s${RESET}.sslip.io domain + automatic HTTPS ${GREEN}[recommended]${RESET}\n" "$detected_ip"
  elif [[ "$nat_detected" == "true" ]]; then
    printf "    ${CYAN}2)${RESET}  QuickStart  — instant %s.sslip.io domain + automatic HTTPS ${DIM}(needs port forwarding — NAT detected)${RESET}\n" "$detected_ip"
  else
    printf "    ${CYAN}2)${RESET}  QuickStart  — server with a public IP, instant sslip.io domain + automatic HTTPS\n"
  fi
  printf "    ${CYAN}3)${RESET}  Advanced    — your own domain + wildcard Let's Encrypt cert (manual DNS)\n"
  echo ""

  local _choice
  if [[ "$ASSUME_YES" == "true" ]]; then
    info "${DIM}--yes:${RESET} no --mode given — using the recommended default."
    _choice="$default_choice"
  else
    require_tty "Setup mode"
    printf "  ${ARROW} ${BOLD}Enter choice${RESET} ${DIM}[1-3, default: %d]${RESET}: " "$default_choice"
    read -r _choice < /dev/tty
    _choice="${_choice:-$default_choice}"
  fi

  case "$_choice" in
    1) SETUP_MODE="local" ;;
    2) SETUP_MODE="quick" ;;
    3) SETUP_MODE="advanced" ;;
    *) fatal "Invalid choice: $_choice" ;;
  esac
}

main() {
  parse_flags "$@"

  banner
  require_root
  check_prerequisites

  # Ensure state dir exists
  mkdir -p "$STATE_DIR"

  if [[ -n "$TEMPS_VERSION" ]]; then
    warn "Installing pinned version ${BOLD}$TEMPS_VERSION${RESET}${YELLOW} — ignoring the release channel.${RESET}"
    echo ""
  elif [[ "$CHANNEL" == "nightly" ]]; then
    warn "Installing the ${BOLD}nightly${RESET}${YELLOW} channel — an automated daily build from main, the least stable option. Not recommended for production.${RESET}"
    echo ""
  elif [[ "$CHANNEL" == "beta" ]]; then
    warn "Installing the ${BOLD}beta${RESET}${YELLOW} channel — prereleases may be unstable.${RESET}"
    echo ""
  fi

  choose_mode

  # Local and QuickStart modes share a dedicated sslip.io-based flow.
  if [[ "$SETUP_MODE" == "local" || "$SETUP_MODE" == "quick" ]]; then
    run_quick_flow
    return
  fi

  # --- Advanced mode: your own domain + wildcard Let's Encrypt cert ---------

  info "This wizard will set up a complete Temps deployment platform"
  info "on this server. It takes about 2-5 minutes."
  echo ""

  if ! prompt_yesno "Ready to begin?" "y"; then
    echo ""
    info "Cancelled. Run this wizard again when you're ready."
    echo ""
    exit 0
  fi

  step_docker
  step_timescaledb
  step_domain_ssl
  step_temps_setup
  step_clickhouse_optin
  step_service
  step_verify
  show_completion
  step_test_deploy
}

main "$@"

}
