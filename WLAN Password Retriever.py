# Import the subprocess library
import subprocess

# Define a function to extract network name from a line
def extract_network_name(line):
    return line.split(":")[1].strip()

# Define a function to extract key content from a line
def extract_key_content(line):
    return line.split(":")[1].strip()

# Define the main function
def main():
    try:
        # Execute the command to get WLAN profiles and store the output
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split("\n")
        # Extract profile names from the output
        profile_names = [extract_network_name(line) for line in output if "All User Profile" in line]

        # Loop through profile names
        for profile_name in profile_names:
            try:
                # Execute the command to get profile details and store the output
                key_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile_name, 'key=clear']).decode('utf-8', errors="backslashreplace").split("\n")
                # Find the line with the "Key Content" information
                key_content_line = next((line for line in key_output if "Key Content" in line), None)

                # If the line exists, extract the password
                if key_content_line:
                    password = extract_key_content(key_content_line)
                else:
                    password = ""

            except subprocess.CalledProcessError:
                # Handle any errors in the process
                password = "ENCODING ERROR"

            # Print the profile name and password
            print(f"{profile_name:<30}|  {password}")

    except subprocess.CalledProcessError:
        # Handle any errors in the main command execution
        print("Error occurred during command execution.")
        
    # Prompt the user to press Enter to close the script
    input("Press Enter to close the script...")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
