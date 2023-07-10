### 2023-07-09 (6)
- Add command to remove specific song from queue
- Change to slash commands rather than message reading

### 2023-07-09 (5)
- Added bot status
- Download audio directly as `pcm` rather than `wav`.
- Optimize await behavior.
- Send `...now typing...` indicator while processing
- Switch normalization method to use `pydub` rather than manual

### 2023-07-09 (4)
- Add responses
- Add volume normalization
- Better link handling and compatibility (e.g. works with `music.youtube.com` now)
- Fix bug causing retries on first join
- Fix clap sound before playback by removing `wav` file metadata
- Move `after` logic outside `play_url`
- Show YouTube video names in queue previews
- Update command parsing (e.g. no longer case-sensitive)

### 2023-07-09 (3)
- Update `README.md`

### 2023-07-09 (2)
- Add changelog
- Async `find_voice_client` fix for retries
- Fix `!current` command
- Trim `get_queue`

### 2023-07-09 (1)
- Initial commit
