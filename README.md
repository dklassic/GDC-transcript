# GDC-transcript

> An attempt to transcribe all GDC YouTube public videos

GDC-transcript is a pet project of [PeDev](https://twitter.com/PeDev_) and [DK Liao](https://twitter.com/RandomDevDK) in an attempt to transcribe publicly available videos in [Game Developers Conference's YouTube channel](https://www.youtube.com/@Gdconf).

## How to use

The tool can be accessed at [GDC-transcript](https://dklassic.github.io/GDC-transcript), enter video ID to attempt loading the embedded video with transcript from this repository.

You can also simply use GET method to link to the video. For example with https://dklassic.github.io/GDC-transcript/?v=c2YRVWZupwo or https://blog.chosenconcept.dev/GDC-transcript/?v=c2YRVWZupwo

For speakers who wanted to provide explicit permission/disallowance and/or additional information on transcription, you can submit an [Issue](https://github.com/dklassic/GDC-transcript/issues/new?assignees=&labels=feedback&template=speaker-feedback.md&title=%5Bfeat%5D+%5BInsert_Video_ID%5D+speaker+feedback) or contact us via [Google Form](https://forms.gle/D68jU5FmAKoXMwhc6).

## Why

In hope of helping those who need of assistance to better enjoy the content from GDC. Not only for non English speakers, but also for when the audio quality is really bad and will destroy our eardrums when listening to. For example [Integrating Narrative into Game Design: A Portal Post-Mortem](https://www.youtube.com/watch?v=c2YRVWZupwo) is a really great talk but the audio quality really suffers.

With full transcript, it would be a lot easier to find whatever you need with text search or just being able to have a quick glance if the content is for you or not. Plus since YouTube has stopped allowing community translation, a possibility to setup community translation would be nice.

## How

We recently discovered there's this nice project by OpenAI called [Whisper](https://github.com/openai/whisper) which turned out to be a pretty good multilingual transcripter. Some extensive tests show it is far capable of handling accent, bad audio quality, and both.

Though in this case, we opted for a version by m-bain called [whipserX](https://github.com/m-bain/whisperX) which is much better at producing precise subtitle timing.

## Why not just YouTube transcription?

Firstly, Whisper showed better results in accuracy than YouTube in our testing.

Secondly, Whisper produces transcripts with better sentence structure that's much easier to read.

And again, being able to just view/preview the content in text format is just easier than sitting through whole video then find out the talk isn't for you.

## Limitation

As far as Whisper goes, it is a decent transcription tool which often rivals human translators in terms of context recognition. However, it will sometimes go haywire and make things up which surely exhibits generative AI's trait. You might see filler script "This initial prompt states that this is a game development transcript" showing up from time to time during music only segments due to this behaviour.

The transcription also tends to mess up when the speaker goes 88 mph and you'll see the structure of subtitle gets messier.

Lastly in order to make sure all English speaking part is properly transcribed, we forcedfully set the langauge detected as "English," which will potentially cause whipser to transribe and translate the non-English part or just having a hard time aligning the subtitle to the right timing. We might go through these case one by one and produce a much robust version of subtitle including orignal language, so that if anyone choose to translate subtitles to non-English versions can have much more context to work on.

## Contributing

Please create Pull Request following [Contributing Guide](./.github/CONTRIBUTING.md) to help us make these awesome contents available to everyone without a hassle! Also feel free to create Issue when a video you need isn't transcribed yet.

Before you start working on some new feature, it's best to check if there is an existing issue first. By opening an issue to express what you have in mind with the feature so we can have a discussion on whether the feature is desirable or not or using the best implementation.

Thank you to everyone contributing to GDC-transcript!

## Dependency

- [subtitles-parser](https://github.com/bazh/subtitles-parser) to parse SRT ([Neos3452's fork](https://github.com/Neos3452/subtitles-parser) to parse dot seperator)
- [youtube.external.subtitle](https://github.com/siloor/youtube.external.subtitle) to display external subtitle

## Futurework

- [x] Allow the resize of video through other mean
- [x] Show reviewer information
- [x] Action to generate transcript for reviewed subtitles
- [ ] Action to generate summary for reviewed subtitles
- [ ] Action to generate translations for reviewed subtitles
- [ ] Action to generate summary for reviewed translations
