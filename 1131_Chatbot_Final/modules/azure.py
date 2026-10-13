from modules.config import config


# Azure Translation
from azure.ai.translation.text import TextTranslationClient
# from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError


# Translator Setup
text_translator = TextTranslationClient(
    credential=AzureKeyCredential(config["AzureTranslator"]["Key"]),
    endpoint=config["AzureTranslator"]["EndPoint"],
    region=config["AzureTranslator"]["Region"],
)


def azure_translate(user_input):

    try:
        target_languages = ["en"]
        # input_text_elements = [InputTextItem(text=user_input)]
        input_text_elements = [user_input]

        response = text_translator.translate(
            body=input_text_elements, to_language=target_languages
        )
        print(response)
        translation = response[0] if response else None

        if translation:
            return translation.translations[0].text

    except HttpResponseError as exception:
        print(f"Error Code: {exception.error}")
        print(f"Message: {exception.error.message}")