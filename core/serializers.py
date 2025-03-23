from django.core.serializers import serialize
import json
from .models import Content


def serialize_contents(contents):
    serialized_data = []
    for content in contents:
        serialized_content = {
            "id": content.id,
            "content_type": content.content_type,
            "duration": content.duration,
            "mediafile": content.mediafile.file.url if content.mediafile else None,
            "custom_page": (
                content.custom_page.view_name if content.custom_page else None
            ),
        }
        serialized_data.append(serialized_content)
    return json.dumps(serialized_data)
