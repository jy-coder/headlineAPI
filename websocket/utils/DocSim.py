import numpy as np


class DocSim:
    def __init__(self, w2v_model, stopwords=None):
        self.w2v_model = w2v_model
        self.stopwords = stopwords if stopwords is not None else []

    def vectorize(self, doc: str) -> np.ndarray:
        """
        Identify the vector values for each word in the given document
        :param doc:
        :return:
        """
        doc = doc.lower()
        words = [w for w in doc.split(" ") if w not in self.stopwords]
        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        # PS: There are other & better ways to do it.
        vector = np.mean(word_vecs, axis=0)
        return vector

    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    def calculate_similarity(self, source_doc, target_docs=None,article_id_list=[], headline=[],threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        if not target_docs:
            return []

        if isinstance(target_docs, str):
            target_docs = [target_docs]

        source_vec = self.vectorize(source_doc)
        results = []
        for ind,doc in enumerate(target_docs):
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            if sim_score > threshold and sim_score >= 0.80 and sim_score != 1:
                results.append({"id" :article_id_list[ind], "title": headline[ind], "similarity": round(sim_score * 100)})
                # results.append({"score": sim_score, "doc": doc, "article_id": article_id_list[ind]})
            # Sort results by score in desc order
            # results.sort(key=lambda k: k["score"], reverse=True)
            # results.sort(key=lambda k: k, reverse=True)
        return results
        # return list(filter(lambda x: x["score"] >= 85, results))

    def calculate_similarity_r(self, source_doc, target_docs=None,threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        if not target_docs:
            return []

        if isinstance(target_docs, str):
            target_docs = [target_docs]

        source_vec = self.vectorize(source_doc)
        results = []
        for ind,doc in enumerate(target_docs):
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            # print(sim_score)
            if sim_score > threshold and sim_score >= 0.60 or sim_score == 1:
                # pass
                return True
        return False