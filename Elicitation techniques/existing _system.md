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

# User Stories


## Story 1

**Front of the card:**  
As a small business owner, I’d like to upload my contract and receive a plain English summary so that I can read it myself without requiring a lawyer for every little thing.

**Back of the card:**  
- The system should allow uploading documents in PDF/Word formats.  
- The system should generate a clear, simplified summary.  
- Summary must retain critical details such as dates, obligations, and penalties.


## Story 2

**Front of the card:**  
As a startup founder, I’d like uncertain or risky terms highlighted so I don’t inadvertently sign on to damaging conditions.

**Back of the card:**  
- The system should flag ambiguous or high-risk clauses.  
- Highlighted clauses must be clearly visible.  
- Users should receive a short explanation of why the clause was flagged.


## Story 3

**Front of the card:**  
As a compliance officer, I’d like version tracking and comments so my team can stay in sync on legal reviews.

**Back of the card:**  
- The system should store and display different versions of documents.  
- Users should be able to compare changes between versions.  
- Threaded comments must be linked to specific sections of the document.


## Story 4

**Front of the card:**  
As a user, I want to ask a chatbot direct questions like “What’s the renewal date?” so I don’t have to read the whole contract.

**Back of the card:**  
- Chatbot should provide contextually accurate answers from the document.  
- If the chatbot can’t answer, it should suggest alternative actions (manual search or lawyer consultation).  
- Answers should reference the original clause for transparency.


## Story 5

**Front of the card:**  
As a client, I want the option to connect with a lawyer directly when the AI’s explanation isn’t enough, so I feel more secure before signing.

**Back of the card:**  
- System must provide a “Connect with Lawyer” feature.  
- Lawyers should receive the client’s query along with relevant document context.  
- Communication must be secure, supporting chat or call options.  
- Lawyer responses should be logged for traceability and follow-up.
  

## Story 6

**Front of the card:**  
As a member of the legal team, I’d like comment threads that are collaborative so I and my team members can comment easily on certain sections of a contract.

**Back of the card:**  
- Users should be able to tag specific sections of the document for discussion.  
- Comment threads must support replies, mentions, and notifications.  
- All comments should be version-controlled and stored securely.


## Story 7

**Front of the card:**  
As a user, I’d like e-signature capabilities so that I can sign agreements within the same system.

**Back of the card:**  
- System must integrate with legally compliant e-signature services.  
- Signed documents must be securely stored and linked to the original document version.  
- Users should receive confirmation after signing.

## Story 8

**Front of the card:**  
As an attorney, I’d like clients’ questions sent to me through the system so I can respond quickly and effectively.

**Back of the card:**  
- Lawyers should receive notifications when clients submit queries.  
- System should display the relevant document context to the lawyer.  
- Lawyers’ responses must be secure and logged for accountability.
  
