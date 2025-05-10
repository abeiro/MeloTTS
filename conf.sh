#!/bin/bash
clear
cat << EOF
Melo-TTS

This will install Melo-TTS. This is a fast TTS that can be run on a potato using either GPU or CPU.

Melo-TTS will use a custom model with predefined Skyrim-like voices.

Options: 
* Choose CPU if you have an AMD GPU.
* Choose GPU if you have a Nvidia GPU that is powerful enough to handle both Skyrim and Melo-TTS

If you are not sure use CPU.

EOF

if [ ! -d /home/dwemer/python-melotts ]; then
	exit "Melo-TTS not installed"
fi

mapfile -t files < <(find /home/dwemer/MeloTTS/ -name "start-*.sh")
# Check if any files were found

if [ ${#files[@]} -eq 0 ]; then
    echo "No files found matching the pattern."
    exit 1
fi

# Display the files in a numbered list
echo -e "Select a an option from the list:\n\n"
for i in "${!files[@]}"; do
    echo "$((i+1)). ${files[$i]}"
done

echo "0. Disable Service";
echo

# Prompt the user to make a selection
read -p "Select an option by picking the matching number: " selection

# Validate the input

if [ "$selection" -eq "0" ]; then
    echo "Disabling service. Run this script again to enable"
    rm /home/dwemer/MeloTTS/start.sh &>/dev/null
    exit 0
fi

if ! [[ "$selection" =~ ^[0-9]+$ ]] || [ "$selection" -lt 1 ] || [ "$selection" -gt ${#files[@]} ]; then
    echo "Invalid selection."
    exit 1
fi

# Get the selected file
selected_file="${files[$((selection-1))]}"

echo "You selected: $selected_file"

ln -sf $selected_file /home/dwemer/MeloTTS/start.sh




