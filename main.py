from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse 
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, PromptTemplate 
from llama_index.core.embeddings import resolve_embed_model 
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.query_pipeline import QueryPipeline
from pydantic import BaseModel
import os 


from prompts import context, code_parser_template
from dotenv import load_dotenv
import ast
from code_reader import code_reader
#import logging 
#logging.basicConfig(level=logging.DEBUG) 

load_dotenv()

llm = Ollama(
    model = "mistral",
    request_timeout = 60.0
)

parser = LlamaParse(result_type = "markdown") 

file_extractor = {".pdf": parser}
# create an instance to read document from directory

documents = SimpleDirectoryReader("./data",file_extractor = file_extractor).load_data()

# now documents are loaded
# pass this documents to local model 


embed_model = resolve_embed_model("local:BAAI/bge-m3")
# pass the documents into vector_index 

vector_index = VectorStoreIndex.from_documents(documents, embed_model = embed_model) 

# vector_index documents will go to query engine 

query_engine = vector_index.as_query_engine(llm = llm)

# now we can query different question to query_engine() 
#result = query_engine.query("What is the purpose of the document?")


tools = [
    QueryEngineTool(query_engine = query_engine, 
                    metadata = ToolMetadata(
                        name="api_documentation",
                        description="this gives documentation about code for an API. Use this for reading docs for the API",
                    ),
                    ),code_reader # this is 2nd agent
    ]


# make a agent 
code_llm = Ollama(
    model = "codellama",
    request_timeout = 60.0) 
agent = ReActAgent.from_tools(tools, llm= code_llm, verbose=True, context=context)


class CodeOutput(BaseModel):
    code: str
    description: str
    filename: str

parser = PydanticOutputParser(CodeOutput)
# json_prompt_str will extract prompt from prompts.py and 
# convert it like class Codeoutput indexed
json_prompt_str = parser.format(code_parser_template)
json_prompt_tmpl = PromptTemplate(json_prompt_str) 
# now to general purpose, we will use mistral llm
output_pipeline = QueryPipeline (chain=[json_prompt_tmpl, llm])

# only typing "q" is conditioned
while (prompt := input("Enter a prompt (q to quit):" )) != "q":

    # sometime it needs more than one time to prompt 
    retires = 0 
    while retires < 3:
        try:
            result = agent.query(prompt)
            # so result will be passed to next LLM 
            next_result = output_pipeline.run(response = result)
            cleaned_json = ast.literal_eval(str(next_result).replace("assistant:", ""))
            break
        except Exception as e:
            retires += 1
            print(f"Error occured, retry #{retires}: {e}")
        
        if retries >= 3:
            print("Unable to process request, try again..")
            continue
        
        print("code generated")
        print (cleaned_json["code"])
        
        print("\n\n Description:", cleaned_json["description"])
        filename = cleaned_json["filename"]
        

        try:
            with open(os.path.join("output", filename), "w") as f:
                f.write(cleaned_json["code"])
            print("saved file", filename)
        except:
            print("Error saving file...") 
            
            
            
