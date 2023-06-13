from core.rpc.dingding_adapter import DingTalkAdapter

ding_talk_adapter = DingTalkAdapter()


class DingTalkUtil:

    @staticmethod
    def send_text(txt: str):
        ding_talk_adapter.send_text(txt)

    @staticmethod
    def send_markdown_msg(title, txt):
        ding_talk_adapter.send_markdown_msg(title, txt)



