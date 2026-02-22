from typing import Dict, List


def generate_notes(confusion_events: List[Dict], transcript_segments: List[Dict]) -> List[Dict]:
    notes = []
    for event in confusion_events:
        timestamp = event["start"]
        matching = None
        for segment in transcript_segments:
            if segment["start"] <= timestamp <= segment["end"]:
                matching = segment
                break
        if matching:
            notes.append(
                {
                    "timestamp": timestamp,
                    "text": matching["text"],
                    "source_segment": matching["text"],
                    "score": event["score"],
                }
            )
        else:
            notes.append(
                {
                    "timestamp": timestamp,
                    "text": "Confusion detected without matching transcript segment.",
                    "source_segment": None,
                    "score": event["score"],
                }
            )
    return notes
