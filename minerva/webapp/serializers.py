from rest_framework import serializers


class DiscussionMessageRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    discussion_id = serializers.IntegerField(required=True)
    page_num = serializers.IntegerField(required=True)


class DiscussionIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    hashtag = serializers.CharField()


class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    app_message_id = serializers.IntegerField()
    sent_date = serializers.DateTimeField()
    last_updated = serializers.DateTimeField()
    content = serializers.CharField()
    sender_id = serializers.IntegerField()
    sender_name = serializers.CharField()
    discussions = DiscussionIdSerializer(many=True)
    reply_to_id = serializers.IntegerField()

    # hashtags = serializers.ListField(child=serializers.CharField())

    @classmethod
    def from_message(cls, message):
        discussions = []
        reply_to_id = None
        for discussion in message.discussions.all():
            hashtag = None
            if discussion.hashtag:
                hashtag = discussion.hashtag.content
            discussions.append({'id': discussion.id,
                                'hashtag': hashtag})

        if message.reply_to:
            reply_to_id = message.reply_to.id

        hashtags = [hashtag.content for hashtag in message.hashtags.all()]

        return cls({
            'id': message.id,
            'app_message_id': message.app_message_id,
            'sent_date': message.sent_date,
            'last_updated': message.last_updated,
            'content': message.content,
            'sender_id': message.sent_by.id,
            'sender_name': message.sent_by.username,
            'discussions': discussions,
            'reply_to_id': reply_to_id,
            'hashtags': hashtags
        })

    # @property
    # def data(self):
    #     return {
    #         'id': self.id,
    #         'app_message_id': self.app_message_id,
    #         'sent_date': self.sent_date,
    #         'last_updated': self.last_updated,
    #         'content': self.content,
    #         'sender_id': self.sent_by.id,
    #         'sender_name': self.sent_by.name,
    #         'discussion_ids': self.discussion_ids,
    #         'discussion_hashtags': self.discussion_hashtags,
    #         'reply_to_id': self.reply_to_id,
    #         # 'hashtags': self.hashtags
    #
    #     }


class DiscussionSummaryFilterSerializer(serializers.Serializer):
    group_ids = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True,
                                      allow_empty=True)
    app_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    discussion_ids = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True,
                                           allow_empty=True)
    sender_ids = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True,
                                       allow_empty=True)
    hashtags = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True, allow_empty=True)
    min_date = serializers.DateTimeField(required=False, allow_null=True)
    max_date = serializers.DateTimeField(required=False, allow_null=True)
    freetext_search = serializers.CharField(required=False, allow_null=True, allow_blank=True)


def is_valid_discussion_summary_order_by(order_list):
    list_of_errors = []
    for value in order_list:
        if value not in DiscussionSummaryRequestSerializer.VALID_ORDER_BY_NAMES:
            list_of_errors.append(value)
    if list_of_errors:
        raise serializers.ValidationError('Invalid values to order by: {} '.format(list_of_errors))

    return order_list


class DiscussionSummaryRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    filters = DiscussionSummaryFilterSerializer(required=False)
    order_by = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True,
                                     validators=[is_valid_discussion_summary_order_by])
    page_num = serializers.IntegerField(required=True)
    page_size = serializers.IntegerField(required=True)

    VALID_ORDER_BY_NAMES = (
        'last_updated',
        'app_id',
        'group_id',
        'first_message_id',
    )


class DiscussionSummarySerializer(serializers.Serializer):
    discussion_id = serializers.IntegerField(required=True)
    discussion_name = serializers.CharField(required=True)
    group_id = serializers.IntegerField(required=True)
    message_count = serializers.IntegerField(required=True)
    last_updated = serializers.DateTimeField(required=True)
    first_message = MessageSerializer()
    latest_messages = MessageSerializer(many=True)


class DiscussionStatsRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    group_ids = serializers.ListField(child=serializers.IntegerField(), required=False, allow_empty=True)


class DiscussionStatsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    hashtag = serializers.CharField()
    group_id = serializers.IntegerField()
    group_name = serializers.CharField()
    message_count = serializers.IntegerField()
    last_updated = serializers.DateTimeField()


class GroupStatsRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)


class GroupStatsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    last_updated = serializers.DateTimeField()


class AppGroupsSerializer(serializers.Serializer):
    app_id = serializers.IntegerField()
    app_name = serializers.CharField()
    groups = GroupStatsSerializer(many=True)


class UserHashtagsRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)


class UserHashtagsSerializer(serializers.Serializer):
    hashtags = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
