def ReadIP(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the content of the file
            content = file.readline().strip()
            
            # Extract the IP address from the content
            if content.startswith("IP:"):
                ip_address = content.split(" ")[1]
                return ip_address
            else:
                raise ValueError("Invalid file format. Expected 'IP: <url>'.")
    except FileNotFoundError:
        return "The file does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def ChangeIP(file_path, new_ip):
    try:
        # Ensure the new IP ends with /video
        if not new_ip.endswith("/video"):
            new_ip += "/video"
            
        # Read the current content of the file
        with open(file_path, 'r') as file:
            content = file.readline().strip()
        
        # Modify the content with the new IP address
        if content.startswith("IP:"):
            prefix = content.split(" ")[0]
            new_content = f"{prefix} {new_ip}"
            
            # Write the updated content back to the file
            with open(file_path, 'w') as file:
                file.write(new_content)
        else:
            raise ValueError("Invalid file format. Expected 'IP: <url>'.")
    except FileNotFoundError:
        return "The file does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"