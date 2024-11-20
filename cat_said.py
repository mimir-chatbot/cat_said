from cat.mad_hatter.decorators import hook
from cat.log import log

@hook  # default priority = 1
def before_cat_reads_message(user_message_json, cat):

    if "prompt_settings" not in user_message_json:
        return user_message_json

    prompt_settings = user_message_json["prompt_settings"]

    if "cat_said" not in prompt_settings:
        return user_message_json

    cat_said = prompt_settings["cat_said"]

    for cat_said_item in cat_said:
        cat.working_memory.update_conversation_history('AI', cat_said_item)

    return user_message_json