from dataclasses import dataclass, field


@dataclass
class InMemoryDocumentStore:
    records: list[dict] = field(default_factory=list)

    def save(self, record: dict) -> None:
        self.records.append(record)


@dataclass
class InMemoryVectorStore:
    vectors: list[dict] = field(default_factory=list)

    def upsert(self, payload: dict) -> None:
        self.vectors.append(payload)


document_store = InMemoryDocumentStore()
vector_store = InMemoryVectorStore()
