meeting_notes = '''
Here are the results for the tickets mentioned in the meeting:

jira_ticket_number: JIRA-123 
ticket_description: Enhance user profile UI and add recent activity section
user: shubhampareek4000
action_item: Nothing to do
previous_release_version: 4.34
suggested_release_version: 4.34  
previous_story_points: 5
suggested_story_points: 5
reasoning: On track for release

jira_ticket_number: JIRA-124
ticket_description: Implement image uploads for user profiles
user: dmitriybaikov  
action_item: Monitor external API integration
previous_release_version: 4.34
suggested_release_version: 4.34
previous_story_points: 5 
suggested_story_points: 7
reasoning: Facing delays due to Imgur API downtime which is critical for image uploads. Increasing story points to account for external dependency.

jira_ticket_number: JIRA-125
ticket_description: Integrate machine learning capabilities using TensorFlow  
user: dmitriybaikov
action_item: Break into subtasks focusing on data preprocessing first
previous_release_version: 4.34
suggested_release_version: 4.35 
previous_story_points: 5
suggested_story_points: 8
reasoning: More complex than expected due to model training and compatibility issues with TensorFlow. Breaking into subtasks and pushing to next release.

jira_ticket_number: JIRA-126
ticket_description: Not provided
user: dmitriybaikov  
action_item: Blocked due to third-party API outage
previous_release_version: 4.34
suggested_release_version: 4.35
previous_story_points: 5
suggested_story_points: 5 
reasoning: Dependent on external API so pushing to next release

jira_ticket_number: JIRA-127
ticket_description: Not provided
user: shubhampareek4000
action_item: Nothing to do  
previous_release_version: 4.34
suggested_release_version: 4.34
previous_story_points: 5
suggested_story_points: 5
reasoning: Back on track after resolving requirements 

jira_ticket_number: JIRA-128
ticket_description: Improve user profile page UI 
user: shubhampareek4000
action_item: Nothing to do
previous_release_version: 4.34 
suggested_release_version: 4.34
previous_story_points: 5 
suggested_story_points: 5
reasoning: On track for release

jira_ticket_number: JIRA-129 
ticket_description: Implement profile image uploads  
user: shubhampareek4000
action_item: Nothing to do
previous_release_version: 4.34
suggested_release_version: 4.34
previous_story_points: 5
suggested_story_points: 3
reasoning: Straightforward feature, reducing story points.

jira_ticket_number: JIRA-130
ticket_description: Optimize database queries using Hibernate
user: shubhampareek4000
action_item: Nothing to do
previous_release_version: 4.34
suggested_release_version: 4.34
previous_story_points: 5
suggested_story_points: 8 
reasoning: Critical for performance, complex due to optimizing queries with Hibernate

jira_ticket_number: JIRA-131  
ticket_description: Implement client-side caching using Redis
user: shubhampareek4000
action_item: Nothing to do 
previous_release_version: 4.34
suggested_release_version: 4.34
previous_story_points: 5
suggested_story_points: 8
reasoning: Critical for performance, complex due to caching implementation with Redis 

jira_ticket_number: JIRA-132
ticket_description: Address critical bugs reported by QA
user: shubhampareek4000
action_item: Nothing to do
previous_release_version: 4.34
suggested_release_version: 4.34
previous_story_points: 5
suggested_story_points: 5  
reasoning: Critical bugs but uncertainty around root causes. 

jira_ticket_number: JIRA-133
ticket_description: Fix usability issue in login flow
user: dmitriybaikov 
action_item: Nothing to do
previous_release_version: 4.34  
suggested_release_version: 4.34
previous_story_points: 5 
suggested_story_points: 3
reasoning: Less complex compared to other bugs

jira_ticket_number: JIRA-134
ticket_description: Integrate new payment gateway using Stripe  
user: dmitriybaikov
action_item: Set up contingency plan for delays
previous_release_version: 4.34
suggested_release_version: 4.34
previous_story_points: 5
suggested_story_points: 10
reasoning: Complex integration due to multiple payment scenarios with Stripe.

In summary, the key highlights from this meeting are:

- Most tickets are on track for 4.34 release. JIRA-125 and JIRA-126 pushed to 4.35 due to dependencies. 

- Critical performance optimization tasks JIRA-130 and JIRA-131 identified and estimated at 8 points each.

- JIRA-124 and JIRA-134 require monitoring of external API integrations. Contingency plans set up.

- JIRA-125 broken into subtasks to simplify machine learning integration.

- Story points adjusted based on task complexity like JIRA-129 reduced to 3 points.

Overall, the team provided estimates for new tasks, identified risks and dependencies to streamline the sprint execution.
'''
from slack_sdk import WebClient
import re
import json

# Slack API configuration
SLACK_TOKEN = 'xoxb-86937043857-5570860957041-pp8iRPv8F6itkjhjgcbP6gr8'  # Replace with your Slack bot token
SLACK_CHANNEL = '#slack-bot-test-channel'  # Replace with the channel name or ID where you want to send the message

client = WebClient(token=SLACK_TOKEN)

result = client.users_list()
members = result.data['members']
# # print(members[0])

# for m in members:
#     if m['name'] == 'gbaringer':
#         print(m)

split_notes = meeting_notes.split("\n\n")

# Initialize an empty list to store the dictionaries
ticket_dicts = []

# Define the keys to extract from each section
keys_to_extract = [
    'user',
    'jira_ticket_number',
    'ticket_description',
    'action_item',
    'previous_release_version',
    'suggested_release_version',
    'previous_story_points',
    'suggested_story_points',
    'reasoning'
]

# Loop through each ticket section and extract the values
for section in split_notes:
    ticket_dict = {}
    for key in keys_to_extract:
        # Use regular expressions to extract the values
        match = re.search(fr'{key}: (.+)', section)
        if match:
            ticket_dict[key] = match.group(1)
    # Add the extracted dictionary to the list
    ticket_dicts.append(ticket_dict)

for ticket in ticket_dicts:
    if 'suggested_story_points' in ticket and ticket['action_item'] != 'Nothing to do':
        username = ticket['user']
        str_representation = json.dumps(ticket)

        for m in members:
            if m['name'] == username:
                user_id = m['id']
                client.chat_postMessage(channel=user_id, text=str_representation)
