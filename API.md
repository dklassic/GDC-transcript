# API Documentation
The front-end can access JSON APIs, which are generated using [`tools/build_metadata_json.py`](tools/build_metadata_json.py) during the deployment workflow.

## Retrieve all subtitles

```
GET /json/subtitles.json
```

### Responses
The array of video IDs.
```javascript
[<video_id>, ...]
```

## Retrieve all reviewed subtitles
```
GET /json/reviewed.json
```

### Responses
The array of video IDs.
```javascript
[<video_id>, ...]
```

## Get video data by ID
```
GET /json/<video_id>.json
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `video_id` | `string` | **Required**. Youtube video id |

### Responses
```
{
    "id": string <Youtube video id>,
    "title": string <Youtube video title>,
    "length": number <The length of video in minutes>,
    "subtitle": string <The file path of video subtitle>,
    "reviewed": boolean <The subtitle is reviewed or not>,
    "translation": {
        "<language>": string,
        ...
    },
}
```

## Get a dictionary of IDs to titles
```
GET /json/titles.json
```
### Responses
```
{
    "<video_id>" : <video_title>,
    ...
}
```
