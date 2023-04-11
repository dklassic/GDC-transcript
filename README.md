# GDC-transcript

> An attempt to transcript all GDC YouTube public videos

GDC-transcript is a pet project of [PeDev](https://twitter.com/PeDev_) and [DK Liao](https://twitter.com/RandomDevDK) in an attempt to transcribe public videos in [Game Developers Conference's YouTube channel](https://www.youtube.com/@Gdconf).

## Why

In hopes to help those who need of assistance to better enjoy the content from GDC. Not only for non English speakers, but also for when the audio quality is really bad and will destroy our eardrums when listening to.

For example [Integrating Narrative into Game Design: A Portal Post-Mortem](https://www.youtube.com/watch?v=c2YRVWZupwo) is a really great talk but the audio quality really suffers.

Also with full transcript, it would be a lot easier to find whatever you need with text search.

## How

We recently discovered there's this nice project by OpenAI called [Whisper](https://github.com/openai/whisper) which turned out to be a pretty good multilingual transcripter.

Some extensive tests show it is far capable of handling accent, bad audio quality, and both.

## Contributing

As far as Whisper goes, it is a decent transcription tool which often rivals human translators in terms of context recognition. However, it will often go haywire and make things up which surely exhibits generative AI's trait.

Please create Pull Request following [Contributing Guide](./.github/CONTRIBUTING.md) to help us make these awesome contents available to everyone! Also feel free to create Issue when a video you need isn't transcribed yet.

Before you start working on something, it's best to check if there is an existing issue first. It's also a good idea to stop by the Discord server and confirm with the team if it makes sense or if someone else is already working on it.

Thank you to everyone contributing to GDC-transcript!

## Dependency

- [subtitles-parser](https://github.com/bazh/subtitles-parser) to parse SRT
- [youtube.external.subtitle](https://github.com/siloor/youtube.external.subtitle) to display external subtitle

## Futurework

- [ ] Allow the resize of video through other means
- [ ] Regenerate transcription for reviewed subtitles
- [ ] Auto-generate translations for reviewed subtitles
