from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

import re

def extract_transcript(url):
    video_id = None
    match = re.search(r'(?:v=|youtu\.be/|embed/)([\w-]+)', url)
    if match:
        video_id = match.group(1)
    if not video_id:
        raise ValueError("Invalid YouTube URL.")

    # Try Hindi, then English (en, en-US), then anything
    language_tries = [
        ['hi'],              # Hindi
        ['en', 'en-US'],     # English variants
        []                   # Any/auto
    ]
    last_exception = None
    for langs in language_tries:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
            # Make a fake pages dict: page num => [timestamped text]
            pages = {}
            for i, entry in enumerate(transcript):
                ts = f"[{int(entry['start']//60):02d}:{int(entry['start']%60):02d}]"
                pages[i+1] = f"{ts} {entry['text']}"
            return pages, transcript
        except (NoTranscriptFound, TranscriptsDisabled) as e:
            last_exception = e
            continue
    # If nothing found in any language
    raise NoTranscriptFound(f"No transcripts found for video {url} in tried languages. Last error: {last_exception}")
