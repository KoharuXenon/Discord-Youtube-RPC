// ==UserScript==
// @name     Koru YouTube to Discord RPC
// @version  1
// @grant    none
// @match        https://www.youtube.com/*
// @match        https://www.youtube.com/
// ==/UserScript==

if (document.location.toString().includes("list=RDMM")) {
    let prevURL = "";
    let element = null;
    let song_name = null;
    let artistElement = null;
    let artist_name = null;
    let targetURL = null;
    let audioPlaying = null;
    let songLoop = null;

    function isAudioPlaying() {
        if ('navigator' in window && 'mediaSession' in navigator) {
            const isPlaying = navigator.mediaSession.playbackState === 'playing';
            return isPlaying;
        } else {
            console.log('Media Session API not supported');
            return false;
        }
    }

    function updateSong() {
        element = document.querySelector('h1.ytd-watch-metadata > yt-formatted-string:nth-child(3)');
        if (!element || (element && element.textContent == "")) {
            console.log("Cant find song name, using alternative.");
            element = document.querySelector('span.cbCustomTitle:nth-child(2)');
        }

        song_name = element ? element.textContent : 'Default Song Name';

        artistElement = document.querySelector('ytd-channel-name.ytd-video-owner-renderer > div:nth-child(1) > div:nth-child(1) > yt-formatted-string:nth-child(1) > a:nth-child(1)');
        artist_name = artistElement ? artistElement.textContent : 'Default Artist Name';

        targetURL = `http://127.0.0.1:5000/update_presence?name=${encodeURIComponent(song_name)}&artist=${encodeURIComponent(artist_name)}`
        audioPlaying = isAudioPlaying()
        if (!audioPlaying) {
            targetURL = "http://127.0.0.1:5000/update_presence?clearit=yes"
        }

        if (targetURL != prevURL) {
            console.log(`Song name: ${song_name}\nArtist: ${artist_name}\nAudio Playing: ${audioPlaying}`);
            fetch(targetURL)
        }

        prevURL = targetURL
    }

    songLoop = setInterval(updateSong, 1000)

    window.addEventListener('unload', function(event) {
        navigator.sendBeacon('http://127.0.0.1:5000/update_presence?clearit=yes');
    });
}
