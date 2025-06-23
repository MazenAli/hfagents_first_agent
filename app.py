from smolagents import CodeAgent, DuckDuckGoSearchTool, load_tool, tool, LiteLLMModel
import os
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def search_web(query: str, num_results: int) -> str:
    """Searches the web for a query and returns the top results.
    Args:
        query: The search query.
        num_results: Number of results to return.
    """
    search_tool = DuckDuckGoSearchTool(max_results=num_results)
    results = search_tool(query)
    return f"Top {num_results} results for '{query}':\n" + "\n".join(results)

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

model = LiteLLMModel(
    model_id="ollama_chat/qwen2:7b",
    api_base="http://host.docker.internal:11434",
    num_ctx=8192,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", token=os.getenv("HF_TOKEN"), trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer, search_web, image_generation_tool], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates,
    additional_authorized_imports=["matplotlib.pyplot", "IPython.display", "PIL", "PIL.Image"]
)


GradioUI(agent).launch(server_name="0.0.0.0", server_port=7860)
