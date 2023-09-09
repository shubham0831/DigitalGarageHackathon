from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

anthropic = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    
)

previousPrompts = {
    1 : {
        "prompt" : "I will be asking you some questions, always respond as a 5 year old",
    }, 
    2 : {
        "prompt" : "what is a court case?",
        "reply" : ""
    }
}
completion = anthropic.completions.create(
    model="claude-2",
    max_tokens_to_sample=300,
    prompt=f"{HUMAN_PROMPT} how does a court case get to the Supreme Court?{AI_PROMPT}",
)
print(completion.completion)