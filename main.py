from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

def generate_prompt(prompt_dict) -> str:
    generated_prompt = "Here is a conversation between a human and you, go through it and analyze it, and then based on the context, response to the human question"
    index = 0

    while index in prompt_dict.keys():
        convo = prompt_dict[index]

        question = convo['prompt']
        question = "human : " + question
        generated_prompt = generated_prompt + "\n" + question


        response = convo['reply']
        if response != "":
           response = "ai : " + response
           generated_prompt = generated_prompt + "\n" + question

        index+=1
    
    return generated_prompt, index-1


anthropic = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    
)

ai_behavior_prompt = '''
    I will be sending you a transcript from a meeting. Based on this transcript I want you to do the following:

    List all the tickets mentioned in this meeting, and for each ticket, give me the following output:

        jira_ticket_number : ticket_number,
        ticket_description : what is the original ticket about
        user : the name of the user this ticket belongs to,
        action_item : action item (eg. increase in story points, delayed release, new subtasks, etc)
        previous_release_version: release version of the task (4.34 by default)
        suggested_release_version: release version you suggest
        previous_story_points: story point of the ticket (default value is 5)
        suggested_story_points: story points you suggest
        reasoning: reasoning for the change
        

        For story points, if a task is taking longer than expected suggest an increase in the story points. Assume each task has a story point of 5, then based on how difficult it is proving
        update the story point by 1,3,5, or 7

        Assume each task is due for 4.34 release. If it seems like it will get delayed, push the release back to 4.35.

        Each ticket can only belong to one user, and not multiple user, identify that user. It is usually the person who first gives updates on the task.

        If a ticket has no action item, just put action item as "nothing to do"

        If you suggest change for any story, provide your reasoning as well, in the reasoning section. Elaborate on this reasoning and don't be vague. If a person has mentioned a reason
        about something being complex, figure out what in particular is complex and put that in reasoning.

    Once you have done this for each ticket, give me a high level summary of this meeting.

    Just reply ok to this message, I will send the transcript in the next message.
    '''

meeting_transcript_file= open("/Users/shubham/Code/personal/DigitalGarageHackathon/sample_meeting_transcript.txt", "r")
meeting_transcript = meeting_transcript_file.read()
meeting_transcript_file.close()

previousPrompts = {
    0 : {
        "prompt" : ai_behavior_prompt,
        "reply" : "ok"
    }, 
    1 : {
        "prompt" : f"Here's the transcript from the meeting. Please do the tasks I mention : \n {meeting_transcript}",
        "reply" : ""
    },
}

prompt, last_index = generate_prompt(previousPrompts)

completion = anthropic.completions.create(
     model="claude-2",
     max_tokens_to_sample=1000000,
     prompt=f"{HUMAN_PROMPT} {prompt} {AI_PROMPT}",
 )

previousPrompts[last_index]['reply'] = completion.completion

print(completion.completion)
