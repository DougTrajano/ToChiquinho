# Data Sources

We want to collect comments from different sources, such as:

- Instagram
- Facebook
- WhatsApp
- Twitter
- Twitch

For each source, we defined a set of public profiles that we want to collect comments from. To maintain privacy, we won't share the profile names.

## Filtering

We want to filter out comments that are not relevant to the toxicity detection using the following criteria:

- Comments must be in Portuguese
- Comments that have one or more related keywords[^1].
- Comments that have more than 50% of confidence score in Perspective API.

## Privacy

We will apply some privacy policies to the comments collected from each source directly in the ingestion pipeline.

- Remove usernames, user ids, and other information that can be used to identify the user.

[^1]: Pending
