// main.js — logic for index.html

const ParamVideoId = 'v';
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const videoId = urlParams.get(ParamVideoId);

var RedirectByVideoId = function (videoId) {
    const parser = new URL(window.location);
    parser.searchParams.set(ParamVideoId, videoId);
    window.location = parser.href;
}

let inputVideoId = document.getElementById('video-id');
let buttonGoto = document.getElementById('button-goto');
inputVideoId.value = videoId;

function extractVideoId(input) {
    // Regular expression to match YouTube URL patterns
    const regex = /^(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:youtu\.be\/|youtube\.com\/(?:(?:watch)?\?(?:.*&)?v(?:i)?=|(?:embed|v|vi|user)\/))([^\?&\"'>]+)/;

    // Check if input matches the YouTube URL pattern
    const match = input.match(regex);

    // If input matches the URL pattern, return the matched video ID, otherwise return input as is
    return match ? match[1] : input;
}

buttonGoto.addEventListener('click', function () {
    RedirectByVideoId(extractVideoId(inputVideoId.value));
});

let elementVideo = document.getElementById('video');
let youtubeEmbed = document.createElement('iframe');
elementVideo.appendChild(youtubeEmbed);
youtubeEmbed.id = 'embedded_video';
youtubeEmbed.src = `https://www.youtube.com/embed/${videoId}`;
youtubeEmbed.frameBorder = 0;
youtubeEmbed.allowFullscreen = true;
youtubeEmbed.style.height = "100%";
youtubeEmbed.style.width = "100%";
youtubeEmbed.style.minHeight = "360px";
youtubeEmbed.style.minWidth = "640px";

var LoadSRT = function (url, callback) {
    const httpRequest = new XMLHttpRequest();

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                let subtitles = parser.fromSrt(httpRequest.responseText, true);

                for (let i in subtitles) {
                    subtitles[i] = {
                        start: subtitles[i].startTime / 1000,
                        end: subtitles[i].endTime / 1000,
                        text: subtitles[i].text
                    };
                }
                elementVideo.style.display = 'inherit';
                document.getElementById('video-fullscreen').style.display = 'inherit';
                document.getElementById('video-size').style.display = 'inherit';
                callback(subtitles);
            } else {
                console.log("Response status: " + httpRequest.status);
            }
        }
    };

    httpRequest.open('GET', url, true);
    httpRequest.send(null);
};

var LanguageName = {}
fetch(`./static/src/translation/language.json`)
    .then(response => response.json())
    .then(data => {
        console.log("Loaded language.json");
        LanguageName = data;
    })

var GetLanguageName = function (langcode) {
    if (LanguageName[langcode]) {
        return LanguageName[langcode];
    }
    return langcode;
}

var TitleDict = {};
var CreateVideoDropdown = function () {
    // Get a reference to the parent element where the dropdown will be inserted
    const selectElement = document.getElementById('video-list-dropdown-select');

    selectElement.addEventListener('change', () => {
        const selectedOption = selectElement.value;
        if (selectedOption !== "Select...") {
            inputVideoId.value = selectedOption
        }
        console.log(selectedOption)
    });
    // Loop through the options array and create an option element for each one
    for (const [key, value] of Object.entries(TitleDict)) {
        console.log(`${key}: ${value}`);
        const optionElement = document.createElement('option');
        optionElement.value = key;
        optionElement.text = value;
        selectElement.appendChild(optionElement);
    }
}

var SetReviewSubtitleLink = function (url) {
    for (element of document.getElementsByClassName('review-subtitle-link')) {
        element.href = url;
    }
}

var LanguageOptions = {};
var CreateLanguageDropdown = function () {
    const selectContainerElement = document.getElementById('language-choice');
    selectContainerElement.style.display = 'inherit';

    const selectElement = document.getElementById('language-choice-select');

    for (const [key, value] of Object.entries(LanguageOptions)) {
        console.log(`${key}: ${value}`);
        const optionElement = document.createElement('option');
        optionElement.value = key;
        optionElement.text = GetLanguageName(key);
        selectElement.appendChild(optionElement);
    }
}

var LoadVideoTitleDict = function (callback) {
    fetch(`./json/titles.json`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            callback(data);
        })
        .catch(error => {
            console.error('Error fetching title dictionary:', error);
        });
}

var LoadSubtitleList = function (callback) {
    fetch(`./json/subtitles.json`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            callback(data);
        })
        .catch(error => {
            console.error('Error fetching subtitle list:', error);
        });
}

var LoadVideoMetadata = function (videoId, callback) {
    fetch(`./json/${videoId}.json`)
        .then(response => response.json())
        .then(data => {
            // Do something with the JSON data
            console.log(data);
            document.getElementById('permission-github').href = "https://github.com/dklassic/GDC-transcript/issues/new?assignees=&labels=feedback&template=speaker-feedback.md&title=%5Bfeat%5D+" + videoId + "+speaker+feedback";
            document.getElementById('permission-google').href = "https://docs.google.com/forms/d/e/1FAIpQLScLEsZcoPCQNm3mm8CTg-vrH7V3UK3MaB3ggBUpUGYKBdmsuw/viewform?usp=pp_url&entry.1807811719=" + videoId;
            callback(data);
        })
        .catch(error => {
            console.error('Error fetching video metadata:', error);
            document.getElementById('not-exists').style.display = 'inherit';
            document.getElementById('create-new-issue').href = "https://github.com/dklassic/GDC-transcript/issues/new?assignees=&labels=missing+transcript&template=transcript-request.md&title=%5Bfeat%5D+" + videoId + "+missing+transcript";
        });
}

var CheckTranscript = function (videoId, languageId) {
    const httpRequest = new XMLHttpRequest();
    let transcriptPath = "";
    if (languageId == "en")
        transcriptPath = "static/src/transcript/" + videoId + ".txt";
    else
        transcriptPath = "static/src/translation/" + languageId + "/transcript/" + videoId + ".txt";
    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {
            if (httpRequest.status === 200) {
                document.getElementById("not-reviewed-transcript-exists").style.display = 'inherit';
                document.getElementById("not-reviewed-transcript-exists").href = "/GDC-transcript/transcript.html?v=" + videoId + "&l=" + languageId;
                document.getElementById("reviewed-transcript-exists").style.display = 'inherit';
                document.getElementById("reviewed-transcript-exists").href = "/GDC-transcript/transcript.html?v=" + videoId + "&l=" + languageId;
            } else {
                document.getElementById("not-reviewed-transcript-exists").style.display = 'none';
                document.getElementById("reviewed-transcript-exists").style.display = 'none';
            }
        }
    };

    httpRequest.open('GET', transcriptPath, true);
    httpRequest.send(null);
}

// LoadVideoTitleDict is available but unused until the video list dropdown is re-enabled.

if (videoId != null && videoId != "") {
    LoadVideoMetadata(videoId, data => {
        const explicitPermission = data["explicit_permission"]
        const explicitDisallowance = data["explicit_disallowance"]
        const additionalDescription = data["additional_description"]
        if (explicitDisallowance) {
            document.getElementById('explicit-disallowed').style.display = 'inherit';
            document.getElementById('not-reviewed-yet').style.display = "none";
            document.getElementById('reviewed').style.display = "none";
            return;
        } else if (explicitPermission) {
            document.getElementById('info-available').style.display = 'inherit';
            document.getElementById('info-available-content').textContent = additionalDescription;
        } else {
            document.getElementById('info-unavailable').style.display = 'inherit';
        }

        const reviewer = data["reviewer"]
        if (!reviewer || !reviewer["en"]) {
            document.getElementById('not-reviewed-yet').style.display = 'inherit';
        }
        else {
            document.getElementById('reviewed').style.display = 'inherit';
            document.getElementById('reviewed-by').textContent = `This subtitle was reviewed by \"${reviewer["en"]}\".`
        }

        const translation = data["translation"]
        LanguageOptions = { "en": data["subtitle"] }
        for (const [key, value] of Object.entries(translation)) {
            LanguageOptions[key] = value;
        }
        SetReviewSubtitleLink("https://github.com/dklassic/GDC-transcript/tree/main/static/src/subtitle/" + videoId + ".srt");
        if (Object.keys(LanguageOptions).length > 1)
            CreateLanguageDropdown();

        let video_subtitles = {};
        var youtubeExternalSubtitle;
        for (const [langcode, srtFilePath] of Object.entries(LanguageOptions)) {
            LoadSRT(srtFilePath, function (subtitles) {
                video_subtitles[langcode] = subtitles;
                CheckTranscript(videoId, langcode);

                // Only at the first time you load a subtitle.
                if (!youtubeExternalSubtitle) {
                    youtubeExternalSubtitle = new YoutubeExternalSubtitle.Subtitle(document.getElementById('embedded_video'), subtitles);
                    document.getElementById('language-choice-select').addEventListener('change', function (e) {
                        if (video_subtitles[this.value]) {
                            youtubeExternalSubtitle.load(video_subtitles[this.value]);
                        }
                        CheckTranscript(videoId, this.value);
                        if (this.value == "en")
                            SetReviewSubtitleLink("https://github.com/dklassic/GDC-transcript/tree/main/static/src/subtitle/" + videoId + ".srt");
                        else
                            SetReviewSubtitleLink("https://github.com/dklassic/GDC-transcript/tree/main/static/src/translation/" + this.value + "/subtitle/" + videoId + ".srt");
                        if (!reviewer || !reviewer[this.value]) {
                            document.getElementById('not-reviewed-yet').style.display = 'inherit';
                            document.getElementById('reviewed').style.display = 'none';
                        }
                        else {
                            document.getElementById('reviewed').style.display = 'inherit';
                            document.getElementById('not-reviewed-yet').style.display = 'none';
                            document.getElementById('reviewed-by').textContent = `This subtitle was reviewed by \"${reviewer[this.value]}\".`
                        }
                    });

                    document.getElementById('fullscreen-btn').addEventListener('click', function (e) {
                        var elem = document.getElementById('video');

                        var openFullscreen = function () {
                            if (elem.requestFullscreen) {
                                elem.requestFullscreen();
                            } else if (elem.mozRequestFullScreen) { /* Firefox */
                                elem.mozRequestFullScreen();
                            } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
                                elem.webkitRequestFullscreen();
                            } else if (elem.msRequestFullscreen) { /* IE/Edge */
                                elem.msRequestFullscreen();
                            }
                        };

                        openFullscreen();
                    });

                    document.getElementById('video-size-select').addEventListener('change', function (e) {
                        var size = this.value;
                        youtubeEmbed.style.minHeight = size + "px";
                        youtubeEmbed.style.minWidth = (size * 16 / 9) + "px";
                    });
                }
            });
        }

    });
}
