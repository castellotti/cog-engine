#!/bin/bash
set -e

# Remove stale X lock files left by a previous container run
rm -f /tmp/.X1-lock /tmp/.X11-unix/X1

# Start virtual framebuffer display sized to match CogEngine's game window (640x595)
Xvfb :1 -screen 0 640x595x24 &

# Wait until Xvfb is actually accepting connections, not just that the socket exists.
# xdpyinfo makes a real connection attempt — only succeeds once the server is ready.
until DISPLAY=:1 xdpyinfo >/dev/null 2>&1; do sleep 0.1; done

# Audio setup: if PULSE_SERVER points to a host PulseAudio (e.g. macOS via TCP),
# use it directly. Otherwise start an internal null sink so the app doesn't crash.
if [ -z "$PULSE_SERVER" ]; then
    pulseaudio --system --disallow-exit \
        --load="module-null-sink sink_name=virtual_out sink_properties=device.description=VirtualSink" \
        2>/dev/null &
    # Wait for the PulseAudio socket to appear
    until [ -S /var/run/pulse/native ]; do sleep 0.1; done
    export PULSE_SERVER=unix:/var/run/pulse/native
    export PULSE_SINK=virtual_out
fi
export SDL_AUDIODRIVER=pulse

# Start VNC server. -afteraccept creates a flag file the moment a browser
# connects, which is used below to delay the game until the user clicks Start.
rm -f /tmp/cogengine_ready
x11vnc -display :1 -forever -nopw -quiet -localhost \
    -afteraccept "touch /tmp/cogengine_ready" &

# Start NoVNC websocket proxy so the display is accessible via browser
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

echo ""
echo "================================================"
echo "  Open your browser to: http://localhost:6080/cogengine.html"
echo "  The game will start once you click START."
echo "================================================"
echo ""

# Pre-create TTS temp files so os.access() checks succeed on first Speak() call
touch /tmp/cogengine_outputtext.txt /tmp/cogengine_outputtext.wav

# Set up the web audio directory served by websockify alongside NoVNC
mkdir -p /usr/share/novnc/audio
echo "0" > /usr/share/novnc/audio/counter.txt

APP="${1:-engine}"
GAMEFILE="${2:-}"

# Wait for the browser to connect to VNC (triggered by the user clicking START).
# This ensures TTS does not begin before the browser audio context is ready.
echo "Waiting for browser connection..."
until [ -f /tmp/cogengine_ready ]; do sleep 0.1; done
echo "Browser connected — starting game."

case "$APP" in
    engine)
        cd /app/cogengine
        exec python2.7 CogEngine_Application_GtkSDL.py $GAMEFILE
        ;;
    devapp)
        cd /app/cogdevapp
        exec python2.7 CogDevApp.py $GAMEFILE
        ;;
    bash)
        exec /bin/bash
        ;;
    *)
        echo "Unknown mode: $APP"
        echo "Usage: docker run ... [engine|devapp|bash] [gamefile.cog]"
        exit 1
        ;;
esac
