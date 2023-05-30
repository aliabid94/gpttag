import gradio as gr
import random
import json

# from transformers import pipeline, set_seed
# generator = pipeline('text-generation', model='gpt2')
# def generate_next(dialogue):
#   return [out["generated_text"] for out in generator(dialogue, num_return_sequences=3)]


with open("wordlist.json") as wordlist_json:
    target_words = json.load(wordlist_json)
start_prompts = [
    "Once upon a time,",
    "There was chocolate everywhere.",
    "The government doesn't want you to know this, but",
    "These are the lyrics to my favorite song:",
]


def generate_next(dialogue):
    return [dialogue + " " + random.choice(target_words) for _ in range(3)]


with gr.Blocks() as demo:
    gr.Markdown(
        """
  # GPT Tag

  Let's play GPT Tag! Try to get GPT to say the target word by prompting it up to 10 times.
  Each prompt you get to enter the next three words in the text sequence. 
  Then pick one from a set of 3 generated sequences to add to the text.
  Let's Go!
  """
    )

    start_btn = gr.Button("Start")

    with gr.Column(visible=False) as content:
        target_box = gr.Textbox(label="Target", interactive=False)
        dialogue_box = gr.Textbox(lines=15, label="GPT Dialogue", interactive=False)
        with gr.Column(visible=False) as error_set:
            error_box = gr.Textbox(label="Error")
        with gr.Column() as prompt_set:
            prompt_box = gr.Textbox(
                label="Prompt",
                placeholder="Enter the next three words to the text above...",
            )
            submit_prompts_btn = gr.Button("Go")
        with gr.Column(visible=False) as generated_set:
            gr.Markdown("Pick one of these generated options:")
            choices = gr.Radio([], label="Path")
        with gr.Column(visible=False) as win_set:
            win_text = gr.Markdown("## You won!", visible=False)

    def start():
        return {
            content: gr.update(visible=True),
            target_box: random.choice(target_words),
            dialogue_box: random.choice(start_prompts),
        }
    start_btn.click(start, [], [content, target_box, dialogue_box])


    def submit_prompts(target, dialogue, prompt):
        error = None
        if target in prompt:
            error = "You can't use the target word in the prompt!"
        if len(prompt.split(" ")) != 3:
            error = "Exactly three words please"
        if error:
            return {
                error_box: error
            }        
        next_choices = generate_next(dialogue + " " + prompt)
        {
            prompt_set: gr.update(visible=False),
            generated_set: gr.update(visible=True),
            error_set: gr.update(visible=False),
            choices: gr.update(choices=next_choices, value=None),
            dialogue_box: dialogue + " " + prompt,
        }
    submit_prompts_btn.click(
        submit_prompts,
        [target_box, dialogue_box, prompt_box],
        [prompt_set, generated_set, error_set, error_box, choices,  dialogue_box],
    )


    def select_prompt(extension, dialogue, target):
        return {
            dialogue_box: extension,
            generated_set: gr.update(False),
            prompt_set: gr.update(visible=(target not in extension)),
            win_set: gr.update(visible=(target in extension))           
        }

    choices.change(
        select_prompt,
        [choices, dialogue_box, target_box],
        [dialogue_box, generated_set, prompt_set, win_set],
    )

demo.launch()
