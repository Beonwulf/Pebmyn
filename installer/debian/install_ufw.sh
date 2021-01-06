#!/bin/bash
has_sudo() {
    local prompt

    prompt=$(sudo -nv 2>&1)
    if [ $? -eq 0 ]; then
    echo "has_sudo__pass_set"
    elif echo $prompt | grep -q '^sudo:'; then
    echo "has_sudo__needs_pass"
    else
    echo "no_sudo"
    fi
}

HAS_SUDO=$(has_sudo)

if [ "$HAS_SUDO" == 'no_sudo' ]
	then
		echo "you should have sudo priveledge to run this script"
		exit 1
elif [ "$HAS_SUDO" == 'has_sudo__needs_pass' ]
	then
		echo "you should have sudo priveledge to run this script"
		exit 1
elif [ "$HAS_SUDO" == 'has_sudo__pass_set' ]
	then 
		sudo apt update
		sudo apt install ufw
fi
