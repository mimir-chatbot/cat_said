from cat.mad_hatter.decorators import hook
from cat.log import log
from cat.memory.vector_memory_collection import VectorMemoryCollectionTypes, DocumentRecall, VectorMemoryCollection

@hook  # default priority = 1
def before_cat_reads_message(user_message_json, cat):

    if "prompt_settings" not in user_message_json:
        return user_message_json

    prompt_settings = user_message_json["prompt_settings"]
    if "cat_said_metadata" in prompt_settings:
        cat.working_memory['cat_said_metadata'] = prompt_settings['cat_said_metadata']

    if "cat_said" not in prompt_settings:
        return user_message_json

    cat_said = prompt_settings["cat_said"]
    for cat_said_item in cat_said:
        cat.working_memory.update_conversation_history('AI', cat_said_item)

    return user_message_json



@hook  # default priority = 1
def after_cat_recalls_memories(cat):

    if 'cat_said_metadata' not in cat.working_memory:
        pass

    recall_query_embedding = cat.cheshire_cat.embedder.embed_query(cat.working_memory.recall_query)
    vector_memory: VectorMemoryCollection = cat.memory.vectors.collections['declarative']

    memories = vector_memory.recall_memories_from_embedding(
            recall_query_embedding, cat.working_memory['cat_said_metadata'], 10, 0.2
    )

    for memory in memories:
        cat.working_memory["declarative_memories"].append(memory)

