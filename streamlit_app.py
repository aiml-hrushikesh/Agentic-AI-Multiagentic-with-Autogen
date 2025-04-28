import streamlit as st
import os
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
load_dotenv()
# Azure OpenAI config (set in backend via .env or hardcoded)
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
model_name = os.getenv("AZURE_OPENAI_MODEL")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

config_list = [
    {
        "model": model_name,
        "api_key": api_key,
        "base_url": endpoint,
        "api_type": "azure",
        "api_version": api_version,
    }
]

llm_config = {"config_list": config_list}
gpt4o_config = {"cache_seed": 42, "temperature": 0, "config_list": config_list, "timeout": 120}

# Prompts
task_template = '''
**Task**: As an architect, design a solution for the following business requirements:
{}
Break down the problem using a Chain-of-Thought approach. Ensure that your
solution architecture follows best practices.
'''

cloud_prompt_template = '''
**Role**: You are a cloud architect. Design architecture using Azure, AWS, and GCP.
Include a comparison table and state why cloud is better than on-prem.
''' + task_template

oss_prompt_template = '''
**Role**: You are an open-source software architect. Avoid cloud, use only popular OSS.
Include a summary table and benefits of open-source.
''' + task_template

lead_prompt_template = '''
**Role**: You are a lead architect reviewing solutions from cloud and OSS architects.
Critically evaluate, highlight disadvantages, and choose the best solution using tables.
''' + task_template

# Streamlit UI
st.title("AI-Generated Architecture Design")

user_prompt = st.text_area("Enter your business problem or requirement:", height=200)

if st.button("Generate Architecture Solution"):
    if user_prompt.strip():
        # Dynamic prompts
        task = user_prompt.strip()
        cloud_prompt = cloud_prompt_template.format(task)
        oss_prompt = oss_prompt_template.format(task)
        lead_prompt = lead_prompt_template.format(task)

        # Agents
        user_proxy = UserProxyAgent(
            name="supervisor",
            system_message="A Human Head of Architecture",
            code_execution_config={
                "last_n_messages": 2,
                "work_dir": "groupchat",
                "use_docker": False,
            },
            human_input_mode="NEVER"
        )

        cloud_agent = AssistantAgent(name="cloud", system_message=cloud_prompt, llm_config=llm_config)
        oss_agent = AssistantAgent(name="oss", system_message=oss_prompt, llm_config=llm_config)
        lead_agent = AssistantAgent(name="lead", system_message=lead_prompt, llm_config=llm_config)

        def state_transition(last_speaker, groupchat):
            if last_speaker is None or last_speaker is user_proxy:
                return cloud_agent
            elif last_speaker is cloud_agent:
                return oss_agent
            elif last_speaker is oss_agent:
                return lead_agent
            else:
                return None

        groupchat = GroupChat(
            agents=[user_proxy, cloud_agent, oss_agent, lead_agent],
            messages=[],
            max_round=2,
            speaker_selection_method=state_transition,
        )

        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

        user_proxy.initiate_chat(manager, message=task)

        # Display results
        st.subheader("AI Architecture Output")
        for msg in groupchat.messages:
            st.markdown(f"**{msg['name'].capitalize()}**: {msg['content']}")
    else:
        st.warning("Please enter a business problem to continue.")
