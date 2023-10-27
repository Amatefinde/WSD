from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, Text2TextGenerationPipeline
import time
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = Text2TextGenerationPipeline(
    model=AutoModelForSeq2SeqLM.from_pretrained("jpelhaw/t5-word-sense-disambiguation"),
    tokenizer=AutoTokenizer.from_pretrained("jpelhaw/t5-word-sense-disambiguation", legacy=True),
    device=device,
    max_new_tokens=1024
)


def get_current_word_meaning(word: str, context: str, meanings: list[str]):
    start_time = time.time()
    context = context.lower()
    word = word.lower()
    context = context.split(word)
    word = " " + word + " "

    expressions = ' " , " '.join(meanings[:-1])
    expressions = expressions + ' ", or " ' + meanings[-1]
    model_input = (
        f"""question: which description describes the word " {word} " best in the following context? \descriptions: [ " {expressions} " ] context: {word.join(context)} . """
    )
    output = pipe(model_input)[0]['generated_text']

    response = {
        "idx": meanings.index(output),
        "meaning": output,
        "spentTime":  round(time.time() - start_time, 2)
    }

    return response
