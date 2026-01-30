from openai import OpenAI

try:
    from utils.prompt_templates import PIXAR_PROMPT
except ImportError:
    from prompt_templates import PIXAR_PROMPT


class SoraDirector:
    def __init__(self):
        self.openai = OpenAI()

    def generate_sora_prompt(
        self, idea: str, prompt_template: str = PIXAR_PROMPT
    ) -> str:
        print("Generating Sora prompt...")
        response = self.openai.responses.create(
            model="gpt-5",
            input=idea,
            instructions=prompt_template,
        )
        return response.output_text


if __name__ == "__main__":
    director = SoraDirector()
    prompt = director.generate_sora_prompt(
        "An intro for a YouTube video about OpenAI's Sora 2 API."
    )
    print(prompt)
