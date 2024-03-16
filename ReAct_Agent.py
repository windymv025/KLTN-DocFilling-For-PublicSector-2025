from typing import Optional, Sequence

from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.tools import BaseTool

from langchain.agents import AgentOutputParser
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.tools.render import ToolsRenderer, render_text_description

# Output parser
import re
from typing import Union
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.exceptions import OutputParserException
from langchain.agents.agent import AgentOutputParser
from langchain.agents.output_parsers import ReActSingleInputOutputParser
# Chat history
from langchain_core.messages import AIMessage, HumanMessage


FINAL_ANSWER_ACTION = "Final Answer:"
MISSING_ACTION_AFTER_THOUGHT_ERROR_MESSAGE = (
    "Invalid Format: Missing 'Action:' after 'Thought:"
)
MISSING_ACTION_INPUT_AFTER_ACTION_ERROR_MESSAGE = (
    "Invalid Format: Missing 'Action Input:' after 'Action:'"
)
FINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE = (
    "Parsing LLM output produced both a final answer and a parse-able action:"
)

def format_filter(text):
  # Regex pattern
  regex1 = r'Thought:\s*(.*?)\n|Action:\s*(.*?)\n|Action Input:\s*(.*?)\n'
  regex2 = r'Thought: (.+)\s+Final Answer: (.+)'
  # Tìm tất cả các khớp phù hợp
  matches = re.findall(regex1, text)
  match2 = re.findall(regex2, text)
  # Lọc ra bộ 3 phù hợp
  format = []
  temp1, temp2, temp3 = '', '', ''
  for i in range(len(matches)):
      thought, action, action_input = matches[i]
      if thought:
        temp1 = "Thought: " + thought
      elif action:
        temp2 = "Action: " + action
      elif action_input:
        temp3 = "Action Input: " + action_input
      if i%3==2:
        format.append((temp1,temp2,temp3))
      if i == len(matches) - 1:
        format.append(match2[-1])
  return format 

count = -1
format = []
class CustomizeReActOutputParser(AgentOutputParser):
    """Parses ReAct-style LLM calls that have a single tool input.

    Expects output to be in one of two formats.

    If the output signals that an action should be taken,
    should be in the below format. This will result in an AgentAction
    being returned.

    ```
    Thought: agent thought here
    Action: search
    Action Input: what is the temperature in SF?
    ```

    If the output signals that a final answer should be given,
    should be in the below format. This will result in an AgentFinish
    being returned.

    ```
    Thought: agent thought here
    Final Answer: The temperature is 100 degrees
    ```

    """

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        include_answer = FINAL_ANSWER_ACTION in text
        if include_answer:
            global count
            global format
            count += 1
            if count == 0:
                text = text.replace('*','')
                format = format_filter(text)
            if count != len(format) - 1:
                action = format[count][1]
                action_input = format[count][2]
                text = format[count][0] + '\n' + format[count][1] + '\n' + format[count][2] + '\n' 
                return AgentAction(action, action_input, text)
            else:
                temp = count
                count = -1
                text = format[temp][0] + '\n' + format[temp][1] + '\n'
                return AgentFinish({"output": format[temp][-1]}, text)
        

        if not re.search(r"Action\s*\d*\s*:[\s]*(.*?)", text, re.DOTALL):
            raise OutputParserException(
                f"Could not parse LLM output: `{text}`",
                observation=MISSING_ACTION_AFTER_THOUGHT_ERROR_MESSAGE,
                llm_output=text,
                send_to_llm=True,
            )
        elif not re.search(
            r"[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)", text, re.DOTALL
        ):
            raise OutputParserException(
                f"Could not parse LLM output: `{text}`",
                observation=MISSING_ACTION_INPUT_AFTER_ACTION_ERROR_MESSAGE,
                llm_output=text,
                send_to_llm=True,
            )
        else:
            raise OutputParserException(f"Could not parse LLM output: `{text}`")

def create_react_agent(
    llm: BaseLanguageModel,
    tools: Sequence[BaseTool],
    prompt: BasePromptTemplate,
    output_parser: Optional[AgentOutputParser] = None,
    tools_renderer: ToolsRenderer = render_text_description,
) -> Runnable:

    missing_vars = {"tools", "tool_names", "agent_scratchpad"}.difference(
        prompt.input_variables
    )
    if missing_vars:
        raise ValueError(f"Prompt missing required variables: {missing_vars}")

    prompt = prompt.partial(
        tools = tools_renderer(list(tools)),
        tool_names = ", ".join([t.name for t in tools]),
    )
    llm_with_stop = llm.bind(stop=["\nObservation"])
    output_parser = output_parser or CustomizeReActOutputParser()
    agent = (
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
        )
        | prompt
        | llm_with_stop
        | output_parser
    )
    return agent