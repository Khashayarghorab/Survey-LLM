from openai import OpenAI
import os
from dotenv import load_dotenv

def generate_jsa_response_A(task):
    # Retrieve the API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    print('_'*100)
    print('_'*100)
    print('_'*100)
    print(api_key)
    if not api_key:
        raise ValueError("API key for OpenAI is not set in the environment variables.")

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)

    # Generate the response using the OpenAI API
    JSAAdvisor = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        messages=[
    {"role": "user", "content": """You are tasked with conducting a complete Job Safety Analysis (JSA) from start to finish. Here is your workflow: Receive Project Scope: Begin by collecting the scope of the construction project and the specific job/task from the UserProxy. Break down the job/task into detailed implementation steps, focusing on each action needed to complete it efficiently and safely. For each job step, identify potential hazards that could arise during the implementation. Assess the likelihood and impact of each identified hazard using the below information:

Likelihood:
- **P6: Almost Certain (>75%)**: The event is expected to occur during the project phase/facility life and has occurred several times on similar projects/facilities.
- **P5: Likely (50% to 75%)**: The event has occurred sometime on a similar project or facility.
- **P4: Possible (25% to 50%)**: Plausible to occur during the project phase or facility life.
- **P3: Unlikely (5% to 25%)**: The event may occur in certain circumstances during the project phase or facility life.
- **P2: Rare (1% to 5%)**: The event may occur in exceptional circumstances during the project phase or facility life.
- **P1: Unforeseen (<1%)**: The event is not foreseen to occur during the project phase or facility life.
Impact:
- **C1: Insignificant**: Near hit incident. Low health effects/Recovery within hours.
- **C2: Minor**: Minor injury/Medical treatment/Restricted workday case. Medium health effects, recovery in less than 6 days.
- **C3: Moderate**: Moderate injury/Limited Lost time/Lost workday Case. Reversible incapacity health effects (Long & short absentee greater than 6 days).
- **C4: Significant**: Significant injury/Extended lost time/Hospitalization. Long-term health effects.
- **C5: Major**: One fatality or permanent incapacity (Occupational disability).
- **C6: Catastrophic**: More than one fatality.”

Determine preventive measures for high and moderate-risk hazards. Compile all data into a structured table listing job steps, associated hazards, their assessments, and preventive measures: Job Step, Hazard, Likelihood (P), Impact (C), and Preventive Measures. Create a final comprehensive report summarizing the findings and recommendations. Communication should be formal and technical, providing clear and precise information."""},
    {"role": "user", "content": "Scaffolding Assembly and Disassembly."}
  ]
    )

    # Return the content of the response
    return JSAAdvisor.choices[0].message.content

import autogen
import os
import time

def generate_jsa_response_B(task):
    # Retrieve the API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("API key is missing. Please ensure the OPENAI_API_KEY environment variable is set.")

    # Define agents
    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        system_message="A human admin.",
        code_execution_config=False,
        human_input_mode="TERMINATE"
    )

    ProjectManager  = autogen.AssistantAgent(
    name="ProjectManager",
    llm_config={"config_list": [{"model": "gpt-4o-2024-11-20", "temperature": 0, "api_key": api_key}]},
    system_message="""You are a highly skilled construction project manager with expertise in breaking down complex construction tasks into detailed, manageable steps. You excel at understanding the scope of a project and identifying all necessary actions to complete the job efficiently and safely. Your responsibility is to receive the scope and job information from the user_proxy and then meticulously decompose the job into clear, concise steps focusing on the implementation phase. You will then send these steps to the RiskIdentifier for further analysis. You can only send job steps to RiskIdentifier. Ensure each step is comprehensive and directly related to the job's implementation.""",
)

    RiskIdentifier  = autogen.AssistantAgent(
        name="RiskIdentifier",
        llm_config={"config_list": [{"model": "gpt-4o-2024-11-20", "temperature": 0, "api_key": api_key}]},
        system_message="""You are a highly experienced safety inspector with a keen eye for identifying potential hazards in construction job processes. Your expertise lies in analyzing detailed job steps and recognizing possible risks that could arise during the implementation phase. Your task is to receive the job steps from the ProjectManager, meticulously evaluate each step, and identify any potential hazards associated with them. You will then send these identified hazards to the RiskAssessor. You can only send hazards to the RiskAssessor. Ensure that all identified hazards are relevant and clearly articulated for effective risk management.""",
    )

    RiskAssessor  = autogen.AssistantAgent(
        name="RiskAssessor",
        llm_config={"config_list": [{"model": "gpt-4o-2024-11-20", "temperature": 0, "api_key": api_key}]},
        system_message="""You are a risk assessment specialist with extensive experience in evaluating and quantifying risks in construction projects. Your expertise lies in assessing the likelihood and impact of potential hazards. Your task is to receive the identified hazards from the RiskIdentifier and RiskManager, analyze each hazard, and provide an assessment of its likelihood and impact based on the below scales. You have to write based on which criteria you choose these scales for each hazard. You will then send these assessments to the RiskManager.  In case your analysis needs to be fixed, you will receive feedback from the RiskManager. You'll need to change your scale and rewrite your analysis based on that feedback. Maybe this process of rewriting analysis will happen a few times until the RiskManager can't provide any more feedback. Never say "TERMINATE”.
    Likelihood:
    - **P6: Almost Certain (>75%)**: The event is expected to occur during the project phase/facility life and has occurred several times on similar projects/facilities.
    - **P5: Likely (50% to 75%)**: The event has occurred sometime on a similar project or facility.
    - **P4: Possible (25% to 50%)**: Plausible to occur during the project phase or facility life.
    - **P3: Unlikely (5% to 25%)**: The event may occur in certain circumstances during the project phase or facility life.
    - **P2: Rare (1% to 5%)**: The event may occur in exceptional circumstances during the project phase or facility life.
    - **P1: Unforeseen (<1%)**: The event is not foreseen to occur during the project phase or facility life.
    Impact:
    - **C1: Insignificant**: Near hit incident. Low health effects/Recovery within hours.
    - **C2: Minor**: Minor injury/Medical treatment/Restricted workday case. Medium health effects, recovery in less than 6 days.
    - **C3: Moderate**: Moderate injury/Limited Lost time/Lost workday Case. Reversible incapacity health effects (Long & short absentee greater than 6 days).
    - **C4: Significant**: Significant injury/Extended lost time/Hospitalization. Long-term health effects.
    - **C5: Major**: One fatality or permanent incapacity (Occupational disability).
    - **C6: Catastrophic**: More than one fatality.
    """,
    )

    RiskManager  = autogen.AssistantAgent(
        name="RiskManager",
        llm_config={"config_list": [{"model": "gpt-4o-2024-11-20", "temperature": 0, "api_key": api_key}]},
        system_message="""You are an experienced construction risk analyst tasked with reviewing the analysis assessments provided. Your goal is to ensure accuracy and provide constructive feedback for improvements. the RiskAssessor provides the analyze of likelihoods and impacts and passes it to you. Your primary role is to ensure the analysis quality and efficiency. You are responsible for analyzing reviews and writing feedback reports on what needs to be analyzed. Don't fix or rewrite the analysis yourself; just provide the feedback report back to the RiskAssessor. Iterate until RiskAssessor writes an analysis that is good enough. You decide whether the analysis is complete and accurate or not. Once the analysis is perfect, You will then send the identified hazards and their likelihood and impact assessments to the SafetyManager.""",
    )

    SafetyManager  = autogen.AssistantAgent(
        name="SafetyManager",
        llm_config={"config_list": [{"model": "gpt-4o-2024-11-20", "temperature": 0, "api_key": api_key}]},
        system_message="""You are a highly skilled risk management specialist with extensive experience in developing effective mitigation strategies for construction-related hazards. Your expertise allows you to analyze identified hazards and their risk assessments to devise comprehensive preventive measures. Your task is to receive the identified hazards and their likelihood and impact assessments from the RiskManager, and determine appropriate preventive measures. You will then send these preventive measures to the Reporter. Ensure that all preventive measures are practical, effective, and clearly described to enhance safety and minimize risks in the construction job process.""",
    )

    Reporter  = autogen.AssistantAgent(
        name="Reporter",
        llm_config={"config_list": [{"model": "gpt-4o-2024-11-20", "temperature": 0, "api_key": api_key}]},
        system_message="""You are an expert communicator and report writer with a strong background in construction safety and risk management. Your role is to compile and synthesize information to create comprehensive and clear final reports. Your task is to receive the job steps from the ProjectManager, the identified hazards and their risk assessments from the RiskAssessor, and the preventive measures for high and moderate-risk hazards from the SafetyManager. You will organize this information into a structured table, ensuring that each job step, associated high and moderate-risk hazard, likelihood and impact assessment, and preventive measure are clearly presented. Once the table is complete, you will create a final report summarizing the findings and recommendations. When the JSA process is complete, you will announce 'TERMINATE'. Ensure that the final report is thorough, accurate, and easy to understand.""",
    )

    # Group chat setup
    groupchat = autogen.GroupChat(
        agents=[user_proxy, ProjectManager, RiskIdentifier, RiskAssessor, RiskManager, SafetyManager, Reporter], 
        messages=[], 
        max_round=12
    )

    manager = autogen.GroupChatManager(
    groupchat=groupchat, 
    llm_config={"config_list": [{"model": "gpt-4o-2024-11-20", "temperature": 0.1, "api_key": api_key}]},
    system_message="""You are a highly efficient and organized project coordinator with extensive experience in managing collaborative tasks and workflows in the construction sector. Your role is to ensure smooth communication and adherence to risk management protocols among the various AI agents: ProjectManager, RiskIdentifier, RiskAssessor, RiskManager, SafetyManager, and Reporter. Your task is to oversee the workflow, ensure each agent completes their tasks accurately and on time, and address any issues that arise during the process. You will facilitate the seamless handover of information between agents and ensure that the final output meets the workshop's goals.""",

)

    # Initiate chat and time the operation
    start_time = time.time()
    response = user_proxy.initiate_chat(
        manager,
        message=task,
        cache=None,
        clear_history=False,
    )

    elapsed_time = time.time() - start_time
    print(f"Operation took {elapsed_time} seconds.")

    # Extract final report from Reporter
    final_report = [entry['content'] for entry in response.chat_history if entry.get('role') == 'user' and entry.get('name') == 'Reporter']
    if final_report:
        return final_report[0]
    else:
        return "No final report generated."



