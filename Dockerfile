FROM ubuntu:16.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python2.7 \
    python-gtk2 \
    python-glade2 \
    python-pygame \
    festival \
    xvfb \
    x11-utils \
    x11vnc \
    novnc \
    websockify \
    pulseaudio \
    && rm -rf /var/lib/apt/lists/*

COPY cogengine/ /app/cogengine/
COPY cogdevapp/ /app/cogdevapp/

# Both cogengine and cogdevapp directories on path so CogDevApp can import CogEngine modules
ENV PYTHONPATH=/app/cogengine:/app/cogdevapp
ENV DISPLAY=:1

EXPOSE 6080

COPY docker/cogengine.html /usr/share/novnc/cogengine.html
COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/festival_server /usr/local/bin/festival_server
RUN chmod +x /entrypoint.sh /usr/local/bin/festival_server

ENTRYPOINT ["/entrypoint.sh"]
CMD ["engine"]
