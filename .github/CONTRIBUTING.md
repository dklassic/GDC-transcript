# GDC-transcript Contributing Guide

Hi! We are really excited that you are interested in contributing to GDC-transcipt. Before submitting your contribution though, please make sure to take a moment and read through the appropriate section for the contribution you intend to make:

- [Issue Reporting Guidelines](#issue-reporting-guidelines)
- [Pull Request Guidelines](#pull-request-guidelines)

## Issue Reporting Guidelines

- The issue list of this repo is **exclusively** for feature requests (i.e. requesting for new transcription or tool function). Non-conforming issues will be closed immediately.

- Transcription and translation error definitely exists so please don't open an issue for that, help us fix it instead!

- Try to search for your issue, it may have already been asked for.

- If your issue is resolved but still open, don’t hesitate to close it.

- Most importantly, we beg your patience: this is a side project that takes time and money to process. The issue list is not paid support and we cannot make guarantees about how fast your issue can be resolved.

## Pull Request Guidelines

- It's OK to have multiple small commits as you work on the PR - we will let GitHub automatically squash it before merging.

- If fixing a bug:
  - If you are resolving an issue, add `(fix: #xxxx[,#xxx])` (#xxxx is the issue id) in your PR title for clarity, e.g. `fix: added transcription for [YouTube_Video_ID] (fix #3899)`.
  - If you reviewed a transcript, add `review: [YouTube_Video_ID]` or `review: [YouTube_Video_Name] ([YouTube_Video_ID])` in your PR title for clarity, e.g. `review: c2YRVWZupwo` or `review: Integrating Narrative into Game Design: A Portal Post-Mortem (c2YRVWZupwo)`.

## Financial Contribution

GDC-transcript uses [Whipser](https://github.com/openai/whisper)'s large model to transcript for best accuracy which costs money. Its ongoing development can be supported via [KoFi](https://ko-fi.com/dkliao).
