// transcript.js — logic for transcript.html

const ParamVideoId = 'v';
const ParamLanguage = 'l';
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const videoId = urlParams.get(ParamVideoId);
const language = urlParams.get(ParamLanguage);

let elementTranscript = document.getElementById('transcript');

/**
 * Format milliseconds as MM:SS (or H:MM:SS if >= 1 hour).
 */
function formatTimecode(ms) {
    const totalSeconds = Math.floor(ms / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    const mm = String(minutes).padStart(2, '0');
    const ss = String(seconds).padStart(2, '0');

    if (hours > 0) {
        return `${hours}:${mm}:${ss}`;
    }
    return `${mm}:${ss}`;
}

/**
 * Build the video player URL with a seek timestamp.
 */
function videoUrlAtTime(seconds) {
    return `/GDC-transcript/?v=${videoId}&t=${seconds}`;
}

/**
 * Parse SRT text into cue objects using the vendored subtitles-parser library.
 * Returns an array of { startTime (ms), text } objects.
 */
function parseSRT(srtText) {
    // parser is provided by subtitles.parser.min.js (loaded before this script)
    return parser.fromSrt(srtText, true);
}

/**
 * Render an array of SRT cues into the transcript container.
 * Groups cues into paragraph-style blocks the same way subtitle_to_transcript.py does
 * (start a new paragraph after a cue whose text ends with . ! ?).
 * Each cue gets a [MM:SS] timecode badge that links to the video at that time.
 */
function renderCuesWithTimecodes(cues) {
    const container = elementTranscript;
    container.innerHTML = '';

    let currentParagraph = document.createElement('p');
    container.appendChild(currentParagraph);

    cues.forEach((cue, index) => {
        const startSeconds = Math.floor(cue.startTime / 1000);
        const timecodeText = formatTimecode(cue.startTime);

        // Timecode anchor
        const timecodeLink = document.createElement('a');
        timecodeLink.href = videoUrlAtTime(startSeconds);
        timecodeLink.target = '_blank';
        timecodeLink.className = 'timecode-link';
        timecodeLink.textContent = `[${timecodeText}]`;
        timecodeLink.title = 'Watch this moment in the video';

        // Cue text node (strip any HTML tags that whisper sometimes adds)
        const cueText = cue.text.replace(/<[^>]*>/g, '').replace(/\n/g, ' ').trim();

        currentParagraph.appendChild(timecodeLink);
        currentParagraph.appendChild(document.createTextNode(' ' + cueText + ' '));

        // Start a new paragraph after a cue that ends a sentence (. ! ?)
        // matching the same logic as subtitle_to_transcript.py
        if (/[.!?]$/.test(cueText) && index < cues.length - 1) {
            currentParagraph = document.createElement('p');
            container.appendChild(currentParagraph);
        }
    });

    // Remove any trailing empty paragraphs
    container.querySelectorAll('p:empty').forEach(el => el.remove());
}

/**
 * Load and display an SRT file with timecoded transcript.
 */
var LoadSRTAsTranscript = function (srtUrl, txtUrl) {
    const httpRequest = new XMLHttpRequest();

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                elementTranscript.style.display = 'inherit';
                document.getElementById("transcript-exists").style.display = 'inherit';
                document.getElementById("video-link").href = "/GDC-transcript/?v=" + videoId;
                document.getElementById("transcript-link").href = txtUrl;

                const cues = parseSRT(httpRequest.responseText);
                renderCuesWithTimecodes(cues);
            } else {
                console.log("Response status: " + httpRequest.status);
                document.getElementById("transcript-not-exists").style.display = 'inherit';
            }
        }
    };

    httpRequest.open('GET', srtUrl, true);
    httpRequest.send(null);
};

if (videoId != null && videoId != "" && language != null && language != "") {
    let srtPath = "";
    let txtUrl = "";

    if (language == "en") {
        srtPath = "static/src/subtitle/" + videoId + ".srt";
        txtUrl = "https://github.com/dklassic/gdc-transcript/blob/main/static/src/transcript/" + videoId + ".txt";
    } else {
        srtPath = "static/src/translation/" + language + "/subtitle/" + videoId + ".srt";
        txtUrl = "https://github.com/dklassic/gdc-transcript/blob/main/static/src/translation/" + language + "/transcript/" + videoId + ".txt";
    }

    LoadSRTAsTranscript(srtPath, txtUrl);
}
