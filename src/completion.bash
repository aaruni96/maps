#/usr/bin/env bash
_maps_completions()
{
    cur_=${words_[cword_]}

    # if completing the first word
    if [ "${#COMP_WORDS[@]}" -eq 2 ]; then
        COMPREPLY=($(compgen -W "runtime remote package --help -h --command -d --deploy -l --list --repo --reset -r --run -u --uninstall --verbose" -- "${COMP_WORDS[1]}"))
        return
    fi

    # if completing the second word (for runtime unspecified case)
    if [ "${#COMP_WORDS[@]}" -eq 3 ]; then
        if [ "${COMP_WORDS[1]}" == "-r" -o "${COMP_WORDS[1]}" == "--run" -o "${COMP_WORDS[1]}" == "--reset" -o "${COMP_WORDS[1]}" == "-u " -o "${COMP_WORDS[1]}" == "--uninstall" ]; then
            COMPREPLY=($(compgen -W "$(./src/maps.py --list-local)" -- "${COMP_WORDS[2]}"))
            return
        fi
        if [ "${COMP_WORDS[1]}" == "-d" -o "${COMP_WORDS[1]}" == "--deploy" ]; then
            COMPREPLY=($(compgen -W "$(./src/maps.py --list | grep '-' | grep -v 'Official' | sed 's/^\s*- //')" -- "${COMP_WORDS[2]}"))
            return
        fi
    fi

    # if completing the third word
    if [ "${#COMP_WORDS[@]}" -eq 4 ]; then
        # for "runtime" specified case
        if [ "${COMP_WORDS[1]}" == "runtime" ]; then
            if [ "${COMP_WORDS[2]}" == "-r" -o "${COMP_WORDS[2]}" == "--run" -o "${COMP_WORDS[2]}" == "--reset" -o "${COMP_WORDS[2]}" == "-u " -o "${COMP_WORDS[2]}" == "--uninstall" ]; then
                COMPREPLY=($(compgen -W "$(./src/maps.py --list-local)" -- "${COMP_WORDS[3]}"))
                return
            fi
            if [ "${COMP_WORDS[2]}" == "-d" -o "${COMP_WORDS[2]}" == "--deploy" ]; then
                COMPREPLY=($(compgen -W "$(./src/maps.py --list | grep '-' | grep -v 'Official' | sed 's/^\s*- //')" -- "${COMP_WORDS[3]}"))
                return
            fi
        fi

        # for "remote" specified case
        if [ "${COMP_WORDS[1]}" == "remote" ]; then
            if [ "${COMP_WORDS[2]}" == "--del-remote" ]; then
                COMPREPLY=($(compgen -W "$(./src/maps.py remote --list)" -- "${COMP_WORDS[3]}"))
                return
            fi
        fi
    fi

    if [ "${COMP_WORDS[1]}" == "runtime" ]; then
        COMPREPLY=($(compgen -W "-h --help --command -d --deploy -l --list --repo --reset -r --run -u --uninstall --verbose" -- "${COMP_WORDS[2]}"))
        return
    fi

    if [ "${COMP_WORDS[1]}" == "remote" ]; then
        if [ "${#COMP_WORDS[@]}" -eq 3 ]; then
            COMPREPLY=($(compgen -W "-h --help --add-remote --del-remote -v --verbose" -- "${COMP_WORDS[2]}"))
            return
        fi
    fi


}

complete -F _maps_completions maps.py