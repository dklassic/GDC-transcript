// transcript.js — logic for transcript.html

const ParamVideoId = 'v';
const ParamLanguage = 'l';
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const videoId = urlParams.get(ParamVideoId);
const language = urlParams.get(ParamLanguage);

let elementScript = document.getElementById('transcript');

function wrapLinesWithParagraphTag(text) {
    if (typeof text !== 'string') {
        throw new Error('Input must be a string');
    }

    const lines = text.split('\n');
    return lines.map(line => `<p>${line}</p>`).join('');
}

var LoadTranscript = function (url) {
    const httpRequest = new XMLHttpRequest();

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                elementScript.style.display = 'inherit';
                document.getElementById("transcript-exists").style.display = 'inherit';
                document.getElementById("video-link").href = "/GDC-transcript/?v=" + videoId;
                if (language == "en")
                    document.getElementById("transcript-link").href = "https://github.com/dklassic/gdc-transcript/blob/main/static/src/transcript/" + videoId + ".txt";
                else
                    document.getElementById("transcript-link").href = "https://github.com/dklassic/gdc-transcript/blob/main/static/src/translation/" + language + "/transcript/" + videoId + ".txt";
                elementScript.innerHTML = wrapLinesWithParagraphTag(httpRequest.responseText);
            } else {
                console.log("Response status: " + httpRequest.status);
                document.getElementById("transcript-not-exists").style.display = 'inherit';
            }
        }
    };

    httpRequest.open('GET', url, true);
    httpRequest.send(null);
};

if (videoId != null && videoId != "" && language != null && language != "") {
    let transcriptPath = "";
    if (language == "en")
        transcriptPath = "static/src/transcript/" + videoId + ".txt";
    else
        transcriptPath = "static/src/translation/" + language + "/transcript/" + videoId + ".txt";
    LoadTranscript(transcriptPath);
}
