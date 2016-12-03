"""Serialize the models"""
from rest_framework import serializers

from server.entries.models import(
    Entry
)

class EntrySerializer(serializers.ModelSerializer):
    """
    Serializes an entry with embeded information including
    list of tags, categories and links associated with that entry
    as simple strings. It also includes a list of hyperlinks to events
    that are associated with this entry as well as hyperlinks to users
    that are involved with the entry
    """
    title = serializers.CharField()
    description = serializers.CharField()
    content_url = serializers.URLField()
    thumbnail_url = serializers.URLField()
    tags = serializers.CharField()

    # not found in the model, but used in form post validaton
    nonce = serializers.SerializerMethodField('get_current_nonce')

    def get_current_nonce(self, entry):
        """
        Get the current nonce bound to the user session
        """
        return self.context.get('nonce', False)

    class Meta:
        """
        Meta class. Because
        """
        model = Entry
        fields = ("title", "description", "content_url", "thumbnail_url", "tags", "nonce")
