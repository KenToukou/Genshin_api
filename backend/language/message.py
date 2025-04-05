from core.config import config
from core.context_vars import get_request_lang


class BASE_MESSAGE:
    text_en: str = ""
    text_ja: str = ""
    lang: str = ""

    def __init__(self, lang: str = ""):
        if not lang:
            lang = get_request_lang() or config.default_language

    def __str__(self) -> str:
        text = ""
        if self.lang == "en":
            text = self.text_en
        elif self.lang == "ja":
            text = self.text_ja
        else:
            text = self.text_en
        return text


class INTERNAL_SERVER_ERROR(BASE_MESSAGE):
    def __init__(self, lang: str = "") -> None:
        super().__init__(lang=lang)
        self.text_en = "Internal server error"
        self.text_ja = "システム内部でエラー発生"


class NOT_FOUND(BASE_MESSAGE):
    def __init__(self, name: str, lang: str = "") -> None:
        super().__init__(lang=lang)
        self.text_en = f"{name} is not found."
        self.text_ja = f"{name}が見つかりません。"
