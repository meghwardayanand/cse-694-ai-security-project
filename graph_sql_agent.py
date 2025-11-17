from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

from safe_sql_module import SafeSQLDatabase, sanitize_sql
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import Ollama


class SQLState(TypedDict):
    question: str
    sql_query: Optional[str]
    result: Optional[str]


def generate_sql(state: SQLState, llm: Ollama, db: SQLDatabase):
    question = state["question"]

    prompt = f"""
        You are an expert SQL generator. Convert the user question into a SAFE SQL query.

        User question: {question}

        Only produce SQL. Database schema:
        {db.get_table_info()}

        SQL:
    """
    sql = llm.invoke(prompt).strip()
    sql = sql.replace('```', '')
    sql = sql.replace('\n', ' ')
    
    return {"sql_query": sql}


def execute_sql(state: SQLState, db: SafeSQLDatabase):
    print(f'BEFORE Sanitization SQL Query: {state["sql_query"]}')
    sql = sanitize_sql(state["sql_query"])
    print(f"SQL Query: {sql}")
    result = db.run(sql)
    return {"result": str(result)}


def create_sql_graph(llm: Ollama, db: SafeSQLDatabase):
    graph = StateGraph(SQLState)

    graph.add_node("generate_sql", lambda s: generate_sql(s, llm, db))
    graph.add_node("execute_sql", lambda s: execute_sql(s, db))

    graph.set_entry_point("generate_sql")
    graph.add_edge("generate_sql", "execute_sql")
    graph.add_edge("execute_sql", END)

    return graph.compile()
