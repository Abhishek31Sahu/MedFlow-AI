from langgraph.checkpoint.postgres import PostgresSaver

DATABASE_URL = (
    "postgresql://hospital:hospital123@localhost:5432/hospital_db"
)

checkpointer_cm = PostgresSaver.from_conn_string(DATABASE_URL)