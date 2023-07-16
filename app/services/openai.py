import os
from loguru import logger
import openai


class OpenAIClient:
    def __init__(
        self,
        temperature=0.5,
        max_tokens=100,
        system_prompt="You are a helpful assistant.",
    ):
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt
        self.prompts = {}

    def setup(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")

        # read all prompts from files in prompts/ folder in app root. add them to a dictionary with the filename as the key.
        for filename in os.listdir("prompts"):
            with open(os.path.join("prompts", filename), "r") as f:
                self.prompts[filename.rstrip(".txt")] = f.read()

        # use the first prompt as the default system prompt
        chosen_prompts = list(self.prompts.values())[-1]
        logger.opt(colors=True).info(
            f"~~ <i><y>{repr(chosen_prompts)}</y></i>"
        )  # i = italic, y = yellow

        self.system_prompt = chosen_prompts

    async def generate_message(self, prompt):
        logger.info(f"<< {repr(prompt)}")
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        logger.info(f">> {repr(response.choices[0].message['content'])}")
        return response.choices[0].message["content"]

    async def generate_message_with_history(self, prompt, history):
        logger.info(f"<# {repr(prompt)}")
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                *history,
                {"role": "user", "content": prompt},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        logger.info(f"#> {repr(response.choices[0].message['content'])}")
        return response.choices[0].message["content"]


openai_client = OpenAIClient()
