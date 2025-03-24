#!/bin/bash

# Check if the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "You need to run this script as root or use sudo."
    exit 1
fi

# Check operating system type (CentOS or Ubuntu)
echo "Checking operating system type..."
if [ -f /etc/redhat-release ]; then
    OS="CentOS"
    # Check if dnf is available, else use yum
    if command -v dnf &>/dev/null; then
        PKG_MANAGER="dnf"
    elif command -v yum &>/dev/null; then
        PKG_MANAGER="yum"
    else
        echo "Neither dnf nor yum found. Exiting."
        exit 1
    fi
    USE_SUDO=false  # No sudo required for CentOS
elif [ -f /etc/lsb-release ]; then
    OS="Ubuntu"
    PKG_MANAGER="apt"
    USE_SUDO=true  # Sudo required for Ubuntu
else
    echo "Unsupported operating system!"
    exit 1
fi


echo "Detected operating system: $OS"

# Install ACL
echo "Do you want to install ACL? (default: yes)"
read -p "Enter [y/n]: " install_acl
install_acl=${install_acl:-y}

if [[ "$install_acl" == "y" || "$install_acl" == "Y" ]]; then
    echo "Installing ACL..."
    if [ "$OS" == "CentOS" ]; then
        $PKG_MANAGER install acl -y  # No sudo for CentOS
    elif [ "$OS" == "Ubuntu" ]; then
        sudo $PKG_MANAGER install acl -y  # Use sudo for Ubuntu
    fi
fi

# Let the user choose a developer group, default is developers
read -p "Enter developer group name (default: developers): " GROUP_NAME
GROUP_NAME=${GROUP_NAME:-developers}

# Check if the developer group exists
if getent group "$GROUP_NAME" > /dev/null; then
    echo "Group '$GROUP_NAME' already exists."
else
    echo "Creating group '$GROUP_NAME'..."
    if [ "$OS" == "CentOS" ]; then
        groupadd "$GROUP_NAME"  # No sudo for CentOS
    elif [ "$OS" == "Ubuntu" ]; then
        sudo groupadd "$GROUP_NAME"  # Use sudo for Ubuntu
    fi
fi

# User enters multiple usernames
echo "Enter developer usernames (separate with spaces, leave blank to skip):"
read -p "Usernames: " users

# Track if users were created
user_created=false

# Create developer users and set passwords
for user in $users; do
    if ! id "$user" &>/dev/null; then
        echo "Creating user: $user"
        if [ "$OS" == "CentOS" ]; then
            useradd -m -s /bin/bash -G "$GROUP_NAME" "$user"  # No sudo for CentOS
        elif [ "$OS" == "Ubuntu" ]; then
            sudo useradd -m -s /bin/bash -G "$GROUP_NAME" "$user"  # Use sudo for Ubuntu
        fi
        echo "Please set a password for user $user (password will not be shown):"
        if [ "$OS" == "CentOS" ]; then
            passwd "$user"  # No sudo for CentOS
        elif [ "$OS" == "Ubuntu" ]; then
            sudo passwd "$user"  # Use sudo for Ubuntu
        fi
        user_created=true

        # Create dedicated directory
        user_dir="/opt/$user"
        echo "Creating directory: $user_dir"
        if [ "$OS" == "CentOS" ]; then
            mkdir -p "$user_dir"  # No sudo for CentOS
            chown "$user:$GROUP_NAME" "$user_dir"  # No sudo for CentOS
            chmod 770 "$user_dir"  # No sudo for CentOS
        elif [ "$OS" == "Ubuntu" ]; then
            sudo mkdir -p "$user_dir"  # Use sudo for Ubuntu
            sudo chown "$user:$GROUP_NAME" "$user_dir"  # Use sudo for Ubuntu
            sudo chmod 770 "$user_dir"  # Use sudo for Ubuntu
        fi

        # Set ACL permissions
        echo "Setting ACL permissions for $user_dir..."
        if [ "$OS" == "CentOS" ]; then
            setfacl -R -m u:$user:rwx "$user_dir"  # No sudo for CentOS
            setfacl -R -d -m u:$user:rwx "$user_dir"  # No sudo for CentOS
            setfacl -R -m g:$GROUP_NAME:rwx "$user_dir"  # No sudo for CentOS
            setfacl -R -d -m g:$GROUP_NAME:rwx "$user_dir"  # No sudo for CentOS
        elif [ "$OS" == "Ubuntu" ]; then
            sudo setfacl -R -m u:$user:rwx "$user_dir"  # Use sudo for Ubuntu
            sudo setfacl -R -d -m u:$user:rwx "$user_dir"  # Use sudo for Ubuntu
            sudo setfacl -R -m g:$GROUP_NAME:rwx "$user_dir"  # Use sudo for Ubuntu
            sudo setfacl -R -d -m g:$GROUP_NAME:rwx "$user_dir"  # Use sudo for Ubuntu
        fi
    else
        echo "User $user already exists, skipping creation."
    fi
done