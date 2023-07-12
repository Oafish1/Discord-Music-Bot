### 2023-07-12
- Add `.config` file for configuring bot parameters
- Add join logic for `/play`
- Add `MAX_QUEUE` and `MAX_QUEUE_HISTORY` parameters
- Add user name display in verbose song output commands (`/current`, `/next`, etc.)
- Added `/history` command
- Change `client.queues` default hierarchy to add `'history'`
- Disable `/join` command if the bot would rejoin the same channel
- Renamed to `Magic Music Bot`
- Replace queue tuple with dictionary for expandability

### 2023-07-10 (3)
- Await commands which modify rather than add to loop, avoid race conditions
- Bugfix in `play` for weird behavior with multiple songs rapidly queued and paused songs
- Change `RawReader` to not require `discord.PCMAudio`
- Change `sync_local` permissions
- Fixed bug with spamming `play` on channel join not playing anything
- Make playing functions async in preparation for background downloading
- Modify command status return behavior
- Modify initialization
- Mute regular console output for ffmpeg
- Small hierarchy changes

### 2023-07-10 (2)
- Added `sync_local` command
- Fix `tree.sync(...)` implementations to properly function
- New guild configurations
- Now works on multiple servers at once
- Revise sync behavior

### 2023-07-10 (1)
- Add rate-limiting warning message
- Change `url` argument for `play` to be required
- Fix popping noise at beginning/end of voice chat playback
- More guidance in `README.md`
- Slash command sync bugfix

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
