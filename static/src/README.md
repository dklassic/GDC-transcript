

Here is a suggested revision:

# About `.metadata` Files

The `.metadata` file is a JSON file that contains additional information about a subtitle or transcript file. It is located in the same directory as the subtitle or transcript file and has the same name as the file, except with the `.meta` extension.

## Example

Here is an example of a `.metadata` file:

```json
{
    "reviewed": true,
    "reviewer" : "DK Liao",
    "explicit_permission": false,
    "explicit_disallowance": false,
    "additional_description": ""
}
```

The `.metadata` file includes the following fields:

- `reviewed`: a boolean indicating whether the subtitle or transcript file has been reviewed.
- `reviewer`: a string indicating the name of the reviewer who reviewed the subtitle or transcript file.
- `explicit_permission`: a boolean indicating whether explicit permission from the speaker was given to use the content.
- `explicit_disallowance`: a boolean indicating whether explicit disallowance from the speaker was given to use the content.
- `additional_description`: a string for any additional information provided by the speaker about the content.

To see an example of a `.metadata` file in use, please refer to the file located at [`./subtitle/ZW8gWgpptI8.srt.meta`](./subtitle/ZW8gWgpptI8.srt.meta).