#!/bin/sh
# Tell your terminal where pixi is, whichever shell it opens and however that
# shell was started.
#
# This is the same program as .pin_shell_path.py beside it, written in shell so
# that it needs nothing installed to run. That matters on the one day it matters
# most: a machine where pixi has just been installed and cannot yet be found has
# no pixi environment to run the Python from, and a Mac without Xcode's command
# line tools answers `python3` with a dialog box rather than a program. A shell
# is the one interpreter that is certainly already there.
#
#     sh .pin_shell_path.sh
#
# The long account of why any of this is needed -- two shells that do not read
# each other's files, and the difference between a login shell and an
# interactive one -- is at the top of .pin_shell_path.py, and is not repeated
# here. The short version is that the pixi installer writes its PATH line into
# one file belonging to one shell, and the window that later cannot find pixi is
# usually a different shell, or the same shell started a different way. So the
# line goes into every file each shell reads on every kind of start: ~/.zshenv
# for zsh, the login file and ~/.bashrc for bash, and config.fish for fish.
#
# The two versions must stay in step. They write the same line under the same
# marker and both look for the folder rather than for their own handiwork, so
# whichever runs first does the work and the other finds nothing left to do. If
# you change what gets written here, change it there in the same commit.
#
# Windows keeps its PATH in the registry rather than in a startup file, so there
# is nothing here for it to do.

set -u

# Where the pixi installer puts pixi, written the way a startup file writes it.
INSTALLER_BIN=".pixi/bin"

# Written above the line so that whoever finds it later knows where it came from
# and that deleting it is allowed. It names `pixi run check` in both versions
# even when this one was run by hand, because that is the command a student is
# told about and the one they will search for when they meet it again.
MARKER='# Added for the Instructing Machines course by `pixi run check`.'


# A shell's name out of a path or a process name, however it was written. A
# login shell lists itself as -zsh and $SHELL is usually a whole path, so
# neither arrives as the bare word this needs to look anything up by.
shell_named() {
    _name=$(printf '%s' "${1:-}" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//; s/^-*//')
    _name=${_name##*/}
    printf '%s' "$_name" | tr '[:upper:]' '[:lower:]'
}


# The shell a new terminal window will start. $SHELL is the right question here,
# and it is a different one from "what am I running inside": this script may
# well be run by a shell a student typed on purpose, while what matters is the
# shell they will meet tomorrow when they open Terminal.
login_shell() {
    _first=$(shell_named "${SHELL:-}")
    case "$_first" in
        zsh|bash|fish) printf '%s' "$_first" ;;
        *)
            if [ "$(uname -s 2>/dev/null)" = Darwin ]; then
                printf 'zsh'
            else
                printf 'bash'
            fi
            ;;
    esac
}


# Every shell to set up: both of the two this is about, plus the default one if
# it is neither. A student whose default shell is fish still gets zsh and bash
# configured; it costs a few lines in files they do not read, and it means that
# the day something opens a bash for them, and something will, pixi is there.
shells_to_cover() {
    _default=$(login_shell)
    case "$_default" in
        zsh|bash) printf 'zsh bash' ;;
        *) printf 'zsh bash %s' "$_default" ;;
    esac
}


# Where that shell keeps its startup files, which is not always the home folder.
# zsh reads $ZDOTDIR instead when it is set, and a student who has set it has
# done so on purpose.
shell_home() {
    if [ "$1" = zsh ] && [ -n "${ZDOTDIR:-}" ]; then
        case "$ZDOTDIR" in
            '~') printf '%s' "$HOME" ;;
            '~/'*) printf '%s%s' "$HOME" "${ZDOTDIR#\~}" ;;
            *) printf '%s' "$ZDOTDIR" ;;
        esac
    else
        printf '%s' "$HOME"
    fi
}


# The file bash opens when it starts as a login shell. bash reads the first of
# these that exists and then stops, so the one to write to is the first that is
# already there rather than always .bash_profile: writing to .bash_profile while
# a .profile is the file being read today would both put the line where bash
# never looks and, by creating .bash_profile, silence that .profile from then on.
bash_login_file() {
    for _name in .bash_profile .bash_login .profile; do
        if [ -e "$1/$_name" ]; then
            printf '%s' "$1/$_name"
            return
        fi
    done
    printf '%s' "$1/.bash_profile"
}


# Every file that shell has to be told, one per line, so that it is told in all
# its moods. zsh needs one and bash needs two; fish reads its one config file
# whether or not it is interactive, so it needs only that.
path_files() {
    case "$1" in
        zsh)
            printf '%s\n' "$2/.zshenv"
            ;;
        bash)
            printf '%s\n' "$(bash_login_file "$2")"
            printf '%s\n' "$2/.bashrc"
            ;;
        fish)
            printf '%s\n' "$2/.config/fish/config.fish"
            ;;
    esac
}


# The login file to make read the rc file, or nothing where there is no safe
# one. For bash this is deliberately not whatever bash_login_file returns. That
# can be ~/.profile, which sh reads too, and `source` is bash's spelling of `.`:
# an sh reading it would print an error on every login. So the bridge only goes
# in a file belonging to bash alone, and is only created where there is no
# ~/.profile for a new ~/.bash_profile to shadow.
bridge_file() {
    case "$1" in
        zsh)
            printf '%s' "$2/.zprofile"
            return
            ;;
        bash) ;;
        *) return ;;
    esac
    for _name in .bash_profile .bash_login; do
        if [ -e "$2/$_name" ]; then
            printf '%s' "$2/$_name"
            return
        fi
    done
    if [ ! -e "$2/.profile" ]; then
        printf '%s' "$2/.bash_profile"
    fi
}


# The rc file the bridge makes the login file read, and the line that does it,
# each written the way that shell's own manual writes it. Both are guarded on
# the rc file existing, so neither breaks a home folder that has not got one.
bridge_rc_name() {
    if [ "$1" = bash ]; then printf '.bashrc'; else printf '.zshrc'; fi
}

bridge_line() {
    if [ "$1" = bash ]; then
        printf '%s' 'if [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi'
    else
        printf '%s' '[[ -f ~/.zshrc ]] && source ~/.zshrc'
    fi
}


# The line that puts pixi on PATH, written the way that shell writes it. It is
# guarded on the folder not being on PATH already, because the line goes in more
# than one file per shell and a login shell reads more than one of them:
# unguarded, PATH would collect a copy of the folder from each, and another copy
# for every shell opened inside another. The guard is POSIX shell rather than
# [[ ]], because for bash the file it lands in can be ~/.profile, and on a Linux
# machine sh reads that one as well, where [[ is a syntax error rather than a test.
path_line() {
    if [ "$1" = fish ]; then
        printf '%s' 'fish_add_path "$HOME/.pixi/bin"'
        return
    fi
    printf '%s' 'case ":$PATH:" in
    *":$HOME/.pixi/bin:"*) ;;
    *) export PATH="$HOME/.pixi/bin:$PATH" ;;
esac'
}


# Whether that file already says that, a missing file counting as a no. Looked
# for by the folder, or by the rc file's name, rather than by the whole line, so
# that what the pixi installer wrote, or what a student typed themselves in one
# of the several forms people write these in, counts as done and does not get a
# second copy underneath it. Backslashes are read as slashes so that a line
# written by a Windows-flavored tool still counts.
mentions() {
    [ -f "$1" ] || return 1
    tr '\\' '/' < "$1" 2>/dev/null | LC_ALL=C grep -q -F "$2"
}


# A path in the home folder as a student would type it.
tilde() {
    case "$1" in
        "$HOME"/*) printf '~/%s' "${1#"$HOME"/}" ;;
        *) printf '%s' "$1" ;;
    esac
}


# Add the block to the end of that file, making it if it is not there. Appended
# rather than read and rewritten, so that nothing already in the file can be
# lost by this even if it is being written to at the time. The newline goes on
# first because a file whose last line has no newline of its own would otherwise
# have this one welded onto the end of it.
append() {
    _path=$1
    _block=$2

    _dir=${_path%/*}
    if [ "$_dir" != "$_path" ] && [ ! -d "$_dir" ]; then
        if ! mkdir -p "$_dir" 2>/dev/null; then
            printf 'could not write to %s\n' "$_path"
            return 1
        fi
    fi

    _last=''
    if [ -s "$_path" ]; then
        _last=$(tail -c 1 "$_path" 2>/dev/null)
    fi

    if ! {
        if [ -n "$_last" ]; then printf '\n'; fi
        printf '\n%s\n%s\n' "$MARKER" "$_block"
    } 2>/dev/null >>"$_path"; then
        printf 'could not write to %s\n' "$_path"
        return 1
    fi
    return 0
}


# Whether the pixi in play is the one its own installer put in the home folder.
# PIXI_EXE is set by pixi itself, so under `pixi run` this is not a guess.
#
# Where neither that nor PATH finds anything, the folder is asked directly. The
# moment this script is most needed is the one in which nothing can find pixi
# yet: run by hand straight after the installer, from the shell the installer
# has just written a line for and which has not read it, there is no PIXI_EXE
# and no pixi on PATH, and the only evidence that the install happened is the
# file sitting there in the home folder. Asking PATH alone would make the script
# do nothing, and say nothing, in exactly that case. A pixi from somewhere else
# still fails this test, since it leaves no ~/.pixi/bin behind, and pointing a
# startup file at a folder that does not exist would not be the fix for it.
pixi_is_the_installers() {
    _found=${PIXI_EXE:-}
    if [ -z "$_found" ]; then
        _found=$(command -v pixi 2>/dev/null)
    fi

    if [ -z "$_found" ]; then
        [ -e "$HOME/$INSTALLER_BIN/pixi" ]
        return
    fi

    # Follow a symlink to what it points at, so that a pixi linked into some
    # other folder is still recognized as the installer's. Bounded, because a
    # link that points at itself would otherwise never come back.
    _hops=0
    while [ -L "$_found" ] && [ "$_hops" -lt 8 ]; do
        _target=$(readlink "$_found" 2>/dev/null) || break
        [ -n "$_target" ] || break
        case "$_target" in
            /*) _found=$_target ;;
            *) _found=${_found%/*}/$_target ;;
        esac
        _hops=$((_hops + 1))
    done

    _where=$(cd "${_found%/*}" 2>/dev/null && pwd -P) || _where=${_found%/*}
    _wanted=$(cd "$HOME/$INSTALLER_BIN" 2>/dev/null && pwd -P) || _wanted="$HOME/$INSTALLER_BIN"
    [ "$_where" = "$_wanted" ]
}


main() {
    case "$(uname -s 2>/dev/null)" in
        MINGW*|MSYS*|CYGWIN*|Windows_NT) return 0 ;;   # PATH lives in the registry here
    esac

    [ -n "${HOME:-}" ] || return 0

    # Either pixi came from somewhere else and is on PATH by some other means,
    # or it is not here at all -- and neither is fixed by pointing a startup
    # file at ~/.pixi/bin.
    pixi_is_the_installers || return 0

    written=''
    bridged=''

    for shell in $(shells_to_cover); do
        base=$(shell_home "$shell")

        # The file names come back one per line and a home folder may have a
        # space in it, so the loop splits on newlines only, with globbing off in
        # case a name contains a character a glob would try to match.
        _ifs=$IFS
        IFS='
'
        set -f
        # The PATH line goes in first, so that in a home folder with no startup
        # files at all the rc file exists by the time the bridge below asks
        # whether there is anything there worth reading.
        for file in $(path_files "$shell" "$base"); do
            if ! mentions "$file" "$INSTALLER_BIN"; then
                if append "$file" "$(path_line "$shell")"; then
                    written="$written    $shell: added the line to $(tilde "$file")
"
                fi
            fi
        done
        set +f
        IFS=$_ifs

        case "$shell" in
            zsh|bash) ;;
            *) continue ;;
        esac

        rc_name=$(bridge_rc_name "$shell")
        profile=$(bridge_file "$shell" "$base")
        if [ -n "$profile" ] && ! mentions "$profile" "$rc_name"; then
            if append "$profile" "$(bridge_line "$shell")"; then
                bridged="$bridged    $shell: $(tilde "$profile") now reads ~/$rc_name
"
            fi
        fi
    done

    if [ -z "$written" ] && [ -z "$bridged" ]; then
        printf 'Your terminal already knows where pixi is.\n'
        return 0
    fi

    if [ -n "$written" ]; then
        printf 'Told your terminal where pixi is:\n'
        printf '%s' "$written"
    fi
    if [ -n "$bridged" ]; then
        printf 'Made your login shell read the file that line is in:\n'
        printf '%s' "$bridged"
    fi
    printf '\n'
    printf 'A shell only reads those files when it starts, so this terminal is\n'
    printf 'unchanged. Open a new one and pixi will be there in that, and in every\n'
    printf 'terminal after it.\n'
    return 0
}

main "$@"
