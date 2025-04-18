from pathway.xpacks.llm.llms import OpenAIChat
from pathway.xpacks.llm.question_answering import AdaptiveRAGQuestionAnswerer
from pathway.xpacks.llm.prompts import prompt_qa
from pathway.xpacks.llm.servers import QASummaryRestServer
from pathway_connector.commentary_handler import CommentaryHandler
from pathway_connector.commentary_documentStore import CommentaryDocumentStore


class Commentary_RAG:
    def __init__(self):
        self.llm = OpenAIChat()

    def start_pipeline(self):
        commentary = CommentaryHandler().read_input("115167")
        store = CommentaryDocumentStore().initStore(commentary)

        rag_pipeline = AdaptiveRAGQuestionAnswerer(
            llm=self.llm,
            indexer=store,
            prompt_template=prompt_qa,
            no_answer_string="No information found.",
            n_starting_documents=2,
            factor=2,
            max_iterations=4,
        )

        QASummaryRestServer(rag_pipeline).serve()
