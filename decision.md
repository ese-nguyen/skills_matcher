## Requirements to Solution Decision Flow

1. **Requirements Gathering**
    - The core requirement is mapping raw skill text to standardized entries in the database.

2. **Analysis**
    - Database skills change infrequently.
    - Incoming skill lists are typically smaller than the database.
    - Inputs may include abbreviations and multiple languages.
    - No labeled training data is available.
    - Key components needed: API, extraction, matching, storage.

3. **Design Approach**
    - Architect skill extraction and matching logic to meet requirements.
    - Plan for future cloud deployment (GCP integration).

4. **Solution Options**
    - The skill database is large (4k+ skills, more in production).
    - Considered approaches:
        - **LLMs (e.g., Pydantic schema output):**
            - Flexible, handles complex language, enforces structured output.
                - E.g.
                    ```
                    class SkillSchema(BaseModel):
                    skills: Literal["Python", "SQL"]```
            - High computational cost, latency, requires prompt engineering, may need input filtering.
        - **Regex / Fuzzy Matching:**
            - Fast, lightweight, simple for exact/near matches.
            - Limited semantic understanding, poor scalability for ambiguous data.
        - **SetFit Model:**
            - Efficient with few labels, fast inference, adapts to domain, leverages sentence-transformers.
            - Needs labeled data, may not generalize, performance depends on label quality and embedding model.
        - **Semantic Language Model (chosen):**
            - Captures meaning/context, handles synonyms/variations, scalable, fast with small models.
            - May require training/tuning, computationally intensive for large models, accuracy depends on model size, external dependencies needed.

5. **Trade-offs: Speed, Accuracy, Scalability**

| Model Type                      | Speed                          | Accuracy                        | Scalability                     | Notes                                                      |
|----------------------------------|-------------------------------|---------------------------------|----------------------------------|------------------------------------------------------------|
| **LLMs (e.g., GPT, Pydantic output)** | Slowest (API calls, large models) | High for complex language/context | Poor for large batches           | Best for nuanced understanding, but costly and slow         |
| **Regex / Fuzzy Matching**       | Fastest (simple string ops)    | Low for semantic similarity      | Excellent                        | Good for exact/near matches, not for meaning/context        |
| **SetFit Model**                 | Fast (small models, local inference) | Moderate to high (with good labels) | Good                             | Needs labeled data, adapts to domain, fast for batch jobs   |
| **Semantic Language Model (sentence-transformers/model2vec)** | Fast to moderate (model size dependent) | High for semantic similarity     | Good with optimized embeddings                             | Handles synonyms/context, works for short phrases           |

**Summary:**  
- Regex/fuzzy matching is fastest but least accurate for semantic tasks.
- LLMs are most accurate for complex language but slow and expensive.
- SetFit and semantic embedding models (sentence-transformers/model2vec) offer a strong balance: fast, scalable, and accurate for skill matching, especially with multilingual support.
- For production, distilled models like `minishlab/potion-multilingual-128M` deliver efficient, multilingual accuracy.

**Chosen Trade-off:**
We have selected semantic embedding models (specifically sentence-transformers/model2vec) as our solution. This choice balances speed, accuracy, and scalability for the skill matching task. While LLMs provide the highest accuracy for complex language, their latency and cost are prohibitive for production-scale matching. Regex/fuzzy matching is extremely fast but fails to capture semantic meaning, making it unsuitable for our use case. SetFit models require labeled data, which we do not have. Semantic embedding models, especially distilled multilingual variants, offer high semantic accuracy, reasonable speed, and scalability for large skill databases and multilingual inputs. This trade-off ensures robust matching performance without excessive computational or operational overhead.

6. **Solution Journey**

Semantic embedding models excel with sentences, but inputs are often single words or short phrases. To improve results:
- Convert keywords to sentences before embedding (e.g., "SQL" → "I have experience in SQL skills"), the same action need to be done with the database.

Three main model types for embeddings:
- Original sentence-transformers
- Instruction-embedding models
- Distilled sentence-transformers (model2vec)

After evaluation, `minishlab/potion-multilingual-128M` stands out for:
- Multilingual support
- Strong word similarity benchmarks
- Small size and fast inference
- Proven performance in the Potion model family

7. **Deployement**

- Using GCP Cloud run
- Steps:
    - Build docker image:
        ```
        docker build <name>/<repo name>:<tag>
        ```
    - Push into docker hub
    - Cloud run point to `docker.io/<name>/<repo name>:<tag>`