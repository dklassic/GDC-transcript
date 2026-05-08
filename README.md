# GDC-transcript

> An attempt to transcribe all GDC YouTube public videos

GDC-transcript is a pet project of [PeDev](https://twitter.com/PeDev_) and [DK Liao](https://twitter.com/RandomDevDK) in an attempt to transcribe publicly available videos in [Game Developers Conference's YouTube channel](https://www.youtube.com/@Gdconf).

The live tool is hosted at **https://dklassic.github.io/GDC-transcript**.

## Table of Contents

- [How to Use](#how-to-use)
- [Why](#why)
- [How It Works](#how-it-works)
- [Why Not Just YouTube Transcription?](#why-not-just-youtube-transcription)
- [Project Structure](#project-structure)
- [Tools & Automation](#tools--automation)
- [API](#api)
- [Contributing](#contributing)
- [Limitations](#limitations)
- [Dependencies](#dependencies)
- [Future Work](#future-work)

---

## How to Use

The tool can be accessed at [GDC-transcript](https://dklassic.github.io/GDC-transcript). Enter a YouTube video ID to load the embedded video with synchronized subtitles from this repository.

You can also link directly to a specific video using a GET parameter:

```
https://dklassic.github.io/GDC-transcript/?v=<video_id>
```

For example: https://dklassic.github.io/GDC-transcript/?v=c2YRVWZupwo

For speakers who want to provide explicit permission or disallowance, or to add additional information about transcription of their talk, please submit an [Issue](https://github.com/dklassic/GDC-transcript/issues/new?assignees=&labels=feedback&template=speaker-feedback.md&title=%5Bfeat%5D+%5BInsert_Video_ID%5D+speaker+feedback) or contact us via [Google Form](https://forms.gle/D68jU5FmAKoXMwhc6).

---

## Why

The goal is to help those who need assistance enjoying GDC content — not only non-English speakers, but also anyone dealing with poor audio quality, or anyone who wants to skim or search talk content without watching the full video.

For example, [Integrating Narrative into Game Design: A Portal Post-Mortem](https://www.youtube.com/watch?v=c2YRVWZupwo) is a great talk but the audio quality really suffers. A full transcript makes this content accessible to a much wider audience.

With full transcripts, text search becomes a powerful way to find relevant talks or quickly gauge whether a video is relevant. Since YouTube has removed community translation support, this project also aims to provide a foundation for community-driven subtitle translations.

---

## How It Works

Transcription is performed using [OpenAI Whisper](https://github.com/openai/whisper), a capable multilingual transcription model that handles accents and poor audio quality well. For more precise subtitle timing, we use the [WhisperX](https://github.com/m-bain/whisperX) fork by m-bain.

The pipeline:
1. Audio is downloaded from YouTube using `yt-dlp` or `pytube`.
2. Large audio files (>24 MB) are resampled to a lower bitrate using `ffmpeg`.
3. Audio is sent to the Whisper API or processed locally via WhisperX.
4. The resulting `.srt` subtitle file is saved to `static/src/subtitle/<video_id>.srt`.
5. Plain-text transcripts are generated from the `.srt` files and saved to `static/src/transcript/`.
6. During deployment, `build_metadata_json.py` builds JSON data files consumed by the frontend.

The frontend is a static site with no build step — it embeds the YouTube player and overlays subtitles using `youtube.external.subtitle`.

---

## Why Not Just YouTube Transcription?

- **Better accuracy:** Whisper outperformed YouTube auto-captions in our testing, especially with accents and poor audio.
- **Better sentence structure:** Whisper produces more readable, well-segmented transcripts.
- **Plain-text access:** Transcripts allow previewing or searching talk content without watching the full video.
- **Translation support:** Since YouTube removed community subtitles, this project provides an alternative path for community translations.

---

## Project Structure

```
GDC-transcript/
├── index.html                    # Main web app (embedded player + subtitle viewer)
├── transcript.html               # Transcript-only reader page
├── package.json                  # Node.js dependencies
├── API.md                        # JSON API documentation
│
├── static/
│   └── src/
│       ├── subtitle/             # .srt subtitle files (named by YouTube video ID)
│       ├── metadata/             # .meta JSON sidecar files (speaker permissions)
│       ├── transcript/           # Plain-text transcripts generated from SRTs
│       └── translation/          # Translated subtitles (subdirectories by language code)
│
├── tools/                        # Python scripts and Jupyter notebooks
│   ├── auto_whisper.py           # Main transcription pipeline
│   ├── build_metadata_json.py    # Builds JSON API files for the frontend
│   ├── subtitle_to_transcript.py # Converts SRT to plain text
│   ├── download_audio.py         # Batch audio downloader
│   ├── metadata_setup.py         # Manages per-video .meta sidecar files
│   ├── update_srt_index.py       # Re-numbers SRT index lines
│   ├── WhisperX_Youtube.ipynb    # Jupyter notebook for local WhisperX transcription
│   ├── YouTube_Fetch.ipynb       # Jupyter notebook for YouTube data fetching
│   └── gdc_video_list.txt        # Master list of tracked GDC video IDs
│
└── .github/
    ├── CONTRIBUTING.md
    ├── workflows/                # GitHub Actions automation
    └── ISSUE_TEMPLATE/           # Issue templates for requests and feedback
```

**Current scale:** ~1,759 subtitle files covering ~1,736 tracked GDC videos.

---

## Tools & Automation

### Python Scripts (`tools/`)

| Script | Purpose |
|---|---|
| `auto_whisper.py` | Downloads audio from YouTube and sends it to the Whisper API to produce an `.srt` file. Handles files >24 MB by reducing bitrate with ffmpeg. |
| `build_metadata_json.py` | Builds per-video JSON files consumed by the frontend. Reads `.srt` files, fetches YouTube metadata, reads `.meta` sidecars, and outputs `json/` data files. |
| `subtitle_to_transcript.py` | Converts a single `.srt` file to a plain `.txt` transcript. Supports `en`, `zh_tw`, and `ja`. |
| `subtitle_to_transcript_all.py` | Batch version of the above for all subtitles. |
| `metadata_setup.py` | Creates or updates `.meta` JSON sidecar files, recording reviewer info and explicit speaker permissions. |
| `update_srt_index.py` | Re-numbers sequential indices in an SRT file after manual edits. |
| `download_audio.py` | Batch-downloads audio from a list of video IDs using concurrent threads. |
| `fetch_id_and_name_from_playlist.py` | Fetches video IDs and titles from a YouTube playlist. |
| `fetch_id_and_view_from_list.py` | Fetches view counts for a list of video IDs. |

### GitHub Actions Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `deploy.yml` | Push to `gh-pages` | Builds JSON data files and deploys the site to GitHub Pages. |
| `auto_whisper.yml` | Manual | Transcribes a video by ID and opens a PR with the new `.srt` file. |
| `transcript.yml` | Manual | Converts a subtitle to plain-text transcript and opens a PR. |
| `reviewed_metadata.yml` | Manual | Marks a video as reviewed in its `.meta` file and opens a PR. |
| `allowance_metadata.yml` | Manual | Records explicit speaker permission for a video. |
| `disallowance_metadata.yml` | Manual | Records explicit speaker disallowance for a video. |
| `update_srt_index.yml` | Manual | Re-numbers SRT indices and opens a PR. |
| `all_transcript.yml` | Manual/Scheduled | Batch-generates transcripts for all subtitles. |
| `issue_check.yml` | Issue opened/edited | Warns if a transcript-request issue has unchecked checkboxes. |

### Running the Tools Locally

Install Python dependencies:

```bash
pip install pytube yt-dlp openai requests
# ffmpeg must also be installed on your system
```

Transcribe a single video:

```bash
python tools/auto_whisper.py <video_id>
```

Convert a subtitle to a plain-text transcript:

```bash
python tools/subtitle_to_transcript.py <video_id>
```

---

## API

The frontend consumes a set of JSON files generated at deploy time. See [API.md](./API.md) for full documentation.

| Endpoint | Description |
|---|---|
| `GET /json/subtitles.json` | Array of all transcribed video IDs |
| `GET /json/reviewed.json` | Array of all reviewed video IDs |
| `GET /json/titles.json` | Dictionary mapping video IDs to titles |
| `GET /json/<video_id>.json` | Full metadata for a specific video |

---

## Contributing

Please create a Pull Request following the [Contributing Guide](./.github/CONTRIBUTING.md). Feel free to open an Issue if a video you need has not been transcribed yet.

Key guidelines:
- **Review subtitles, not transcripts.** Transcripts are generated from subtitles, not the other way around.
- Before working on a new feature, open an issue first to discuss whether it's desirable.
- PR titles should follow the format: `review: <YouTube_Video_ID>` or `review: <Talk Title> (<video_id>)`.

GDC-transcript uses Whisper's large model for best accuracy, which costs money to run. If you'd like to support the project financially, you can do so via [Ko-Fi](https://ko-fi.com/dkliao).

Thank you to everyone contributing to GDC-transcript!

---

## Limitations

- **Hallucinations:** Whisper occasionally makes things up. A filler phrase like "This initial prompt states that this is a game development transcript" may appear during music-only segments.
- **Fast speakers:** When a speaker talks very quickly, subtitle alignment can become unreliable.
- **Forced English:** Language detection is forced to English to ensure English segments are correctly transcribed. This can cause Whisper to mistranslate or misalign non-English segments. A future improvement would process these segments in their original language.

---

## Dependencies

- [subtitles-parser](https://github.com/bazh/subtitles-parser) — SRT parsing ([Neos3452's fork](https://github.com/Neos3452/subtitles-parser) for dot-separator support)
- [youtube.external.subtitle](https://github.com/siloor/youtube.external.subtitle) — External subtitle overlay for YouTube embeds
- [OpenAI Whisper](https://github.com/openai/whisper) — AI transcription model
- [WhisperX](https://github.com/m-bain/whisperX) — Whisper fork with improved subtitle timing
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) / [pytube](https://github.com/pytube/pytube) — YouTube audio download

---

## Future Work

- [x] Allow video resize
- [x] Show reviewer information
- [x] Action to generate transcript for reviewed subtitles
- [ ] Action to generate summary for reviewed subtitles
- [ ] Action to generate translations for reviewed subtitles
- [ ] Action to generate summary for reviewed translations
