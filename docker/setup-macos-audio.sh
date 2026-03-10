#!/bin/bash
#
# Sets up PulseAudio on macOS to receive audio streamed from the Docker container.
# After running this script, start the container with:
#
#   PULSE_SERVER=tcp:host.docker.internal:4713 docker compose up cogengine
#
# or export it for the session:
#
#   export PULSE_SERVER=tcp:host.docker.internal:4713
#   docker compose up cogengine

set -e

if ! command -v brew &>/dev/null; then
    echo "Homebrew not found. Install it from https://brew.sh first."
    exit 1
fi

echo "Installing PulseAudio..."
brew install pulseaudio

PA_CONFIG="$(brew --prefix)/etc/pulse/default.pa"

if ! grep -qE "^load-module module-native-protocol-tcp" "$PA_CONFIG"; then
    echo "" >> "$PA_CONFIG"
    echo "# Allow Docker containers to stream audio over TCP (no auth for local dev)" >> "$PA_CONFIG"
    echo "load-module module-native-protocol-tcp auth-anonymous=1 port=4713" >> "$PA_CONFIG"
    echo "Added TCP module to $PA_CONFIG"
else
    echo "TCP module already present in $PA_CONFIG"
fi

# Restart PulseAudio to pick up the new config
pulseaudio --kill 2>/dev/null || true
sleep 1
pulseaudio --daemon

echo ""
echo "PulseAudio is running on port 4713."
echo ""
echo "To enable audio when running the container:"
echo "  export PULSE_SERVER=tcp:host.docker.internal:4713"
echo "  docker compose up cogengine"
