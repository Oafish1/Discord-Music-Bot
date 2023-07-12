## TODO
### HIGH PRIORITY
- Change name to magic music bot
- Add song history
- Store user with URL
- Cut playlist tag from YouTube URL
- Spotify links
- Itunes/Apple music links
- Replace previews with embeds for hyperlink functionality and more
- Add macro for printing song (i.e. '{get_name(...)} ({user.name})')
- Maybe restrict `/queue`, etc. command to users in channel?
- Refine join calling (don't erase queue if joining same channel), issue is resuming play

### MEDIUM PRIORITY
- Random bug which causes current song to not play, not sure how occurs
- Maybe remove `'current'` from queue and just use the top position in `'queue'`
- Add ban functionality (file with banned ids (per guild?))
- Persist queue in file (use locks)
- Preload video on request using async ffmpeg
- Pass oauth message to end-user, rather than to server.  Make async so heartbeat doesn't die
- Add time left in song/queue
- Playlist compatibility (with restricted creds to owners/admins?)
- Mouse over bot to see song/queue progress
- Autoplay

### LOW PRIORITY
- Add user command log (X skipped Y, etc.)
- Add video streaming
- Add previous song command

### NOTES
- What should the publicity of the `sync_local` command be?
- Add timeout to messages
- Add auto-leave on program exit
- Detect channel change
- Implement whitelist
- Handle edge case where play is called between songs?  Add lock?
- Maybe allow /play when user not in voice?
- Add auto disconnect after no activity period
- Add logic in `join` for user not in voice
- Add song swap functionality
- Store creds for each guild?
- Add message for skipping song/reject if bad link instead of adding to queue
- Maybe skip to song in queue option?  Maybe reorder?
- Replace song function?
- Add crossfade between songs with pydub
- Add search feature for !play
- Add functionality for stream?
- Check which device works with InnerTube
- sort based on quality (already done?)
- Maybe call `after` after rather than recurse
- Refine `is_youtube_link`
- Store queueing user
- Stream music rather than download all at once
