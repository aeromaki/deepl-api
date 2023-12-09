from collections import OrderedDict
from typing import (
    Iterable,
    List,
    Optional,
    Union
)
import dotenv
import deepl

class DeepLTranslator(deepl.Translator):
    def __init__(
        self,
        dotenv_path: str = ".env",
        dotenv_values: Optional[OrderedDict] = None,
        dotenv_key_name: str = "DEEPL_API_KEY",
        auth_key: Optional[str] = None,
        **kwargs
    ):
        if auth_key is None:
            if dotenv_values is None:
                dotenv_values = dotenv.dotenv_values(dotenv_path)
            if dotenv_key_name not in dotenv_values:
                raise Exception("DeepL API key not found in dotenv file")
            auth_key = dotenv_values[dotenv_key_name]

        super().__init__(auth_key, **kwargs)

    def translate(
        self,
        source: Union[str, Iterable[str]],
        target_lang: str,
        return_list: bool = True,
        **kwargs
    ) -> Union[str, Iterable[str], List[str]]:
        if isinstance(source, str):
            return self.translate_str(source, target_lang, **kwargs)
        else:
            if return_list:
                return self.translate_list(source, target_lang, **kwargs)
            else:
                return self.translate_iterable(source, target_lang, **kwargs)

    def translate_to_EN(
        self,
        source: Union[str, Iterable[str]],
        return_list: bool = True,
        **kwargs
    ) -> Union[str, Iterable[str], List[str]]:
        return self.translate(source, "EN-US", return_list, **kwargs)

    def translate_to_KO(
        self,
        source: Union[str, Iterable[str]],
        return_list: bool = True,
        **kwargs
    ) -> Union[str, Iterable[str], List[str]]:
        return self.translate(source, "KO", return_list, **kwargs)

    def translate_str(
        self,
        source_text: str,
        target_lang: str,
        **kwargs
    ) -> str:
        return self.translate_text(source_text, target_lang=target_lang, **kwargs).text

    def translate_iterable(
        self,
        source_iterable: Iterable[str],
        target_lang: str,
        **kwargs
    ) -> Iterable[str]:
        return map(lambda x: x.text, self.translate_text(source_iterable, target_lang=target_lang, **kwargs))

    def translate_list(
        self,
        source_iterable: Iterable[str],
        target_lang: str,
        **kwargs
    ) -> List[str]:
        return list(self.translate_iterable(source_iterable, target_lang, **kwargs))