# Author: Shubham Varmora (202301450)

## Elicitation Technique: Analysis of Existing Systems

### 1. Technique Description
In our project, we applied the **analysis of existing systems** technique. This involves examining other tools currently available in the legal-tech arena, evaluating their capabilities, and identifying both positives and negatives.  

Since our project focuses on **simplifying legal documents for non-lawyers**, it was logical to see how others are tackling the same problem.


### 2. Why We Used This Approach
We used this approach because legal-tech is not a new field. Platforms such as **LegalReview.AI**, **LegalFly**, and **Flair** already exist to make contracts and compliance documents easier to understand. From examining them, we could:

- Avoid reinventing the wheel on features that already exist.  
- Observe what is effective and should be retained in our system.  
- Identify gaps in their offerings that we might fill.  
- Understand how we can stand out in a crowded space.  

A key reason for this technique was to **test and validate our feature concept** of allowing users to connect with a lawyer for uncertainties. Most existing tools work entirely on AI, but actual users often want **human assurance**.


### 3. How We Did the Analysis
We analyzed competitor tools such as **LegalReview.AI**, **Flair**, and **LegalFly** by:

1. Checking their websites, product demos, and available reviews.  
2. Categorizing their features into three buckets:
   - **Core features:** Available in all tools (clause extraction, document summaries).  
   - **Value-add features:** Available in some but not all (collaboration, e-signature support).  
   - **Missing or weak features:** Areas where they struggled (ambiguity detection, human lawyer connectivity).  
3. Documenting trends and mapping them against the objectives of our own system.  
4. Identifying loopholes and planning features we could develop to address them.


### 4. What We Found (Summary Report)
After studying these systems, we observed:

- **Strengths:** Effective at automation — extracting clauses such as dates, obligations, penalties, and providing summaries.  
- **Partial capabilities:** E-signatures and simple collaboration exist but are limited.  
- **Weaknesses:**  
  - Poor clarity and trust features.  
  - No human-in-the-loop capability.  
  - Minimal collaboration features; often only “share document” without threaded discussions.  

**Conclusion:** There is a significant opportunity for a **hybrid setup** where AI handles routine tasks, users can consult a lawyer when needed, and groups can collaborate effectively.


### 5. Requirements We Derived

#### Functional Requirements (FR)
1. Upload legal documents in various formats.  
2. Extract prominent clauses (dates, obligations, penalties, etc.).  
3. Highlight risky or unclear terms.  
4. Generate plain-English summaries.  
5. Document version tracking.  
6. E-signature integration permitted.  
7. Threaded comment discussions enabled for collaboration.  
8. Users connected with a lawyer for expert explanation.  
9. Secure export and sharing of documents.

#### Non-Functional Requirements (NFR)
1. High accuracy clause extraction and summarization.    
2. Stable and reliable performance, even with large contracts.  
3. Secure platform.  
4. Scalable to support multiple users and documents.  
