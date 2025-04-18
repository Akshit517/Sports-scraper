
from pathway.xpacks.llm.document_store import DocumentStore

from pathway.stdlib.indexing.text_search import TantivyBM25Factory


class CommentaryDocumentStore:

    def initStore(self, formatted_commentary):
        retriever_factory = TantivyBM25Factory()
        store = DocumentStore(docs=formatted_commentary,
                              retriever_factory=retriever_factory)
        return store
