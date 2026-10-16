def make_message(sender, target_agent, content, is_untrusted_data=False):
    return {
        "sender": sender,
        "target_agent": target_agent,
        "content": content,
        "is_untrusted_data": is_untrusted_data
    }