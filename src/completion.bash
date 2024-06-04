# bash completion for maps

_maps_completions()
{
    local cur prev words cword
    _init_completion || return
    
    # if completing the first word
    if [ $cword -eq 1 ]; then
        COMPREPLY=($(compgen -W "runtime remote package --help -h --command -d --deploy -l --list --list-local --repo --reset -r --run -u --uninstall --verbose" -- $cur))
        return
    fi

    # if completing the second word (for runtime unspecified case)
    if [ $cword -eq 2 ]; then
        if [ $prev == "-r" -o $prev == "--run" -o $prev == "--reset" -o $prev == "-u " -o $prev == "--uninstall" ]; then
            COMPREPLY=($(compgen -W "$($words --list-local)" -- $cur))
            return
        fi
        if [ $prev == "-d" -o $prev == "--deploy" ]; then
            COMPREPLY=($(compgen -W "$($words --list | grep '-' | grep -v 'Official' | sed 's/^\s*- //')" -- $cur))
            return
        fi
    fi

    # if completing the third word
    if [ $cword -eq 3 ]; then
        # for "runtime" specified case
        if [ "${COMP_WORDS[1]}" == "runtime" ]; then
            if [ $prev == "-r" -o $prev == "--run" -o $prev == "--reset" -o $prev == "-u" -o $prev == "--uninstall" ]; then
                COMPREPLY=($(compgen -W "$($words --list-local)" -- $cur))
                return
            fi
            if [ $prev == "-d" -o $prev == "--deploy" ]; then
                COMPREPLY=($(compgen -W "$($words --list | grep '-' | grep -v 'Official' | sed 's/^\s*- //')" -- $cur))
                return
            fi
        fi
        # for "remote" specified case
        if [ "${COMP_WORDS[1]}" == "remote" ]; then
            if [ $prev == "--del-remote" ]; then
                COMPREPLY=($(compgen -W "$($words remote --list)" -- $cur))
                return
            fi
        fi
        # for "package" specified case
        if [ "${COMP_WORDS[1]}" == "package" ]; then
            if [ $prev == "-c" -o $prev == "--commit" -o $prev == "-i" -o $prev == "--initialize" -o $prev == "-s" -o $prev == "--sandbox" ]; then
                COMPREPLY=($(compgen -o dirnames -- "$cur"))
                return
            fi
        fi
    fi

    if [ $prev == "runtime" ]; then
        COMPREPLY=($(compgen -W "-h --help --command -d --deploy -l --list --list-local --repo --reset -r --run -u --uninstall --verbose" -- $cur))
        return
    fi

    if [ $prev == "remote" ]; then
        if [ $cword -eq 2 ]; then
            COMPREPLY=($(compgen -W "-h --help --add-remote --del-remote -v --verbose" -- $cur))
            return
        fi
    fi

    if [ $prev == "package" ]; then
        if [ $cword -eq 2 ]; then
            COMPREPLY=($(compgen -W "-h --help -c --commit -i --initialize -s --sandbox -v --verbose" -- $cur))
            return
        fi
    fi


}

complete -F _maps_completions maps
