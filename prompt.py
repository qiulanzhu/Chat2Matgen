INSTRUCTIONS = """
---
我的问题：
{{question}}
---
请根据KEY_INFORMATION回答我的问题。KEY_INFORMATION可能有用，也可能没用，你需要从我给出KEY_INFORMATION中选出与我的问题最相关的那些，来为你的回答提供依据。回答一定要忠于原文，回答流程但不失专业，不要胡乱编造，也不需要解释。请用中文回答。
让回复的格式更清晰美观。你的回复："""

PROMPT_TEMPLATE = f"""
<INSTRUCTIONS>
{INSTRUCTIONS}
</INSTRUCTIONS>

<KEY_INFORMATION>
{{key_information}}
</KEY_INFORMATION>
"""