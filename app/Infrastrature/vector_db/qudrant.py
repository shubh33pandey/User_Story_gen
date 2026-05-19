from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
 
    def rerank(self, query, chunks, top_k=3):
        if not chunks:
            return []
 
        pairs = [[query, c] for c in chunks]
        scores = self.model.predict(pairs, batch_size=16)
 
        query_words = set(query.lower().split())
 
        combined = []
        for chunk, score in zip(chunks, scores):
            overlap = sum(1 for w in query_words if w in chunk.lower())
            overlap_score = overlap / (len(query_words) + 1)
 
            final_score = score + overlap_score
            combined.append((chunk, final_score))
 
        combined = sorted(combined, key=lambda x: x[1], reverse=True)
        return [c for c, _ in combined[:top_k]]
 