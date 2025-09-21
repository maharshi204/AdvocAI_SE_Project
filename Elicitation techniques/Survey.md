## Authors:-

1. Sharnam Shah      - 202301247
2. Parth Karena      - 202301472
3. Dhanush B. Pillai - 202301483



# Definition

## Survey Elicitation Technique  
The **Survey Elicitation Technique** is a method of collecting structured input from stakeholders through carefully designed surveys.  
It is used to gather both:  

- **Functional requirements** (specific features or services users need)  
- **Non-functional requirements** (qualities such as trust, usability, and personalization)  

This technique helps in understanding user needs, expectations, and preferences, allowing for the mapping of these insights to system features.  

---

# Why We Used This Method

### Relevance to Target Users  
Since our platform (**AdvocAI**) is user-centric, we needed direct feedback from potential users.  

### Scalability  
A single Google Form could reach a large and diverse audience quickly.  

### Balanced Data Collection  
The form had closed-ended questions for quantitative analysis and open-ended questions for qualitative insights.  

### Ease of Participation  
Stakeholders could respond anytime and anonymously, encouraging more honest answers.  

### Efficient Requirement Gathering  
This allowed us to collect both functional requirements and non-functional requirements simultaneously.  

---

# Detailed Description of How We Did That

## Step 1: Preparation  
We defined the objectives of the survey:  
- To understand how users interact with legal documents  
- To identify their pain points  
- To capture the features they would like in **AdvocAI**  

## Step 2: Form Design  

### Legal Document Features  
- Difficulty in understanding legal documents  
- Usefulness of summarization  
- Types of documents: contracts, property, business, employment  

### Lawyer Connection Features  
- Preference for risk/highlight extraction  
- Interest in connecting to lawyers  
- Preferred modes of communication  
- Factors influencing lawyer choice  

### AI Summariser  
- Comfort level in using AI for legal queries  
- Types of lawyer assistance preferred  

### Feedback  
- Open-ended questions about challenges  
- Trust factors  
- Additional suggestions  

---

# Requirements for Sprint 1

## Functional Requirements (FRs) – Basic Scope  

### Document Upload & Summarization  
- Upload simple documents (contracts, property, HR docs)  
- Generate short summaries with only key points.

### Lawyer Connection & Consultation  
- Provide a basic option to connect with lawyers after AI summary  

### AI Summariser
- Answer basic legal definitions and FAQs  
- Provide step-by-step guidance for **very simple tasks** 

---

## Non-Functional Requirements (NFRs) – Basic Scope  

- **Accuracy & Reliability** – Deliver simple, reasonably correct outputs 
- **Security** – Basic file privacy
- **Usability** – Simple, user-friendly interface for first-time users  
- **Performance** – Quick summarization and chatbot responses for small documents  
- **Scalability** – Limited user support for testing (not full real-time availability yet)  
- **Trust** – Show clear, simple explanations and basic lawyer details (name, expertise)  

## User Stories 

# User Stories

| Front | Back (Acceptance Criteria) |
|-------|-----------------------------|
| **As a** non professional user, **I want** the facility to summarise general contracts and agreements, real estate and property related documents, business contracts, application forms and employment/HR documents **so that** I can easily understand them without wasting time going through them. | 1. User can upload contracts, real estate/property docs, business contracts, application forms and HR/employment docs.<br>2. System generates a concise summary in plain, jargon-free language.<br>3. File format should be Word or PDF.<br>4. Summary is generated within a reasonable time, say 5 minutes.<br>5. A disclaimer to further consult a lawyer before proceeding with AI’s understanding of the document. |
| **As a** non professional user, **I want** to be able to connect and communicate to a lawyer via chat service, audio or video call or email after generating the AI summary, **so that** I can feel secure about proceeding with the document. | 1. Users should be able to see an option to connect with a lawyer.<br>2. User can choose between multiple communication modes:<br>&nbsp;&nbsp;&nbsp;• Chat service<br>&nbsp;&nbsp;&nbsp;• Audio call<br>&nbsp;&nbsp;&nbsp;• Video call<br>&nbsp;&nbsp;&nbsp;• Email<br>3. System shows available lawyers before the user initiates contact.<br>4. Lawyer must request user’s permission to view the document if it is set to be viewed with access. If set as “anyone can view”, then the Lawyer can click on a user’s document to see it.<br>5. User receives confirmation that the lawyer has accepted or scheduled the session. |
| **As a** non professional user, **I want** to be able to see the lawyer’s area of expertise, years of experience, fees charged for his/her work, ratings and reviews in his profile section, **so that** I have a better understanding of who to talk to. | 1. Each lawyer has a profile section visible to non-professional users. The Lawyer can edit his/her profile by clicking on the “Edit” button.<br>2. The Lawyer must be required to show proof of his expertise to avoid fake info in his profile.<br>3. Profiles can be searched and filtered by the user. |
| **As a** non professional user, **I want** a chatbot that does not reveal my information to any 3rd parties and one-to-one private communication mode with legal professionals **so that** my data is secure and I can feel safe. | 1. Chatbot does not share any user information with third parties.<br>2. User has access to a one-on-one end-to-end encrypted communication channel with legal professionals (chat, audio, or video).<br>3. No other users or professionals can access the conversation unless explicitly invited by the user.<br>4. System displays a clear privacy statement explaining how data is handled and a checkbox for accepting terms and conditions. The Terms and Conditions should be accessible via a link.<br>5. User can request deletion of their chat history and associated data at any time.<br>6. Logs and transcripts are not accessible to anyone outside the platform’s secure environment or to the user unless logged in to the account. |
| **As a legal professional, I want** a feature to create a profile for normal public to view and the feature to view a document before accepting queries of the person in need **so that** my work goes smoothly and efficiently. | 1. Legal professional can create and edit a public profile.<br>2. Profile must display at minimum:<br>&nbsp;&nbsp;&nbsp;• Area of expertise<br>&nbsp;&nbsp;&nbsp;• Years of professional experience<br>&nbsp;&nbsp;&nbsp;• Fees charged<br>&nbsp;&nbsp;&nbsp;• Ratings (average score)<br>&nbsp;&nbsp;&nbsp;• Reviews<br>3. Public users can view the lawyer’s profile before initiating contact.<br>4. Legal professional can accept or decline a query after viewing the document.<br>5. If declined, the user is notified and can choose another lawyer.<br>6. All document previews are secure and accessible only to the intended lawyer. |





# Survey Responses

We took a comprehensive survey via a Google Form, which was filled by **100+ participants**.  
The summary of the survey is presented below, with charts/graphs attached.

---

## Age Distribution
The survey was filled by people ranging from ages **17 to 58**, with maximum participants in the **19–20** and **53–56** age groups.

![Age Distribution](images/age_distribution.png)

---

## Profession Split
There was a roughly even split between **working professionals** and **students**.  
(*Note: Both red and yellow in the chart represent working professionals – a spelling error caused duplication.*)

![Profession Split](images/profession_split.png)

---

## Understanding Legal Documents
A **majority of participants** find it *somewhat difficult* to understand legal documents.

![Difficulty Understanding](images/difficulty_understanding.png)

---

## Use of Online Legal Assistance Tools
Most people had **never used an online legal assistance tool**.

![Online Tools Usage](images/online_tools_usage.png)

---

## Summarisation Feature
Most respondents felt that a **document summarisation feature** would be useful.

![Summarisation Feature](images/summarisation_feature.png)

---

## Common Document Types
The majority of people deal with **Contracts & Agreements**.

![Document Types](images/document_types.png)

---

## AI Highlighting Feature
Most people were in favour of **AI that highlights risks, obligations, and key clauses**.  
No one was against it.

![AI Highlights](images/ai_highlights.png)

---

## Lawyer Connection Preferences
There was a **split opinion** on whether to connect directly with a lawyer after reviewing the AI summary.  
Many preferred an **audio call** to connect with the lawyer.

![Lawyer Connection](images/lawyer_connection.png)

**Influencing factors** in choosing a lawyer:  
- Area of expertise  
- Years of experience  
- Fees  

---

## Personalised Dashboard
More than a quarter of people felt the need for a **dashboard** to track uploaded documents, summaries, and consultations.

![Dashboard Need](images/dashboard.png)

---

## Chatbot Usage
There was a **split opinion** on willingness to ask a **chatbot** for basic legal questions.

![Chatbot Usage](images/chatbot_usage.png)

---

## Step-by-Step Assistance
Many felt that **step-by-step assistance for simple legal tasks** would be the most useful feature.

![Step by Step Assistance](images/step_assistance.png)

---

# Conclusion
The survey highlights the **demand for AI-driven tools** that simplify legal documents, provide actionable insights, and offer direct lawyer connectivity where needed.  
A combination of **AI-powered summarisation, clause highlighting, personalised dashboards, and step-by-step guidance** is likely to be the most impactful solution.

# Analysis of User Responses on Advoc AI

## Q1: What challenges do you currently face in accessing legal help?

### Findings
Users face multiple pain points when dealing with legal services. The key challenges can be categorized as follows:

#### Accessibility Issues
- Difficulty in finding the right lawyer with relevant expertise.
- Problems with availability and scheduling of appointments.
- Long waiting times and time-consuming legal procedures.

#### Knowledge & Comprehension Gaps
- Struggle to understand complex legal terminology and jargon.
- Lack of awareness about required documents and updated government rules.
- Confusion due to inconsistent or conflicting advice from different lawyers.

#### Trust & Security Concerns
- Fear of encountering fake or untrustworthy lawyers.
- Concerns about data security when uploading documents online.
- Skepticism about whether legal advice will be accurate and reliable.

#### Cost & Resource Constraints
- High consultation fees, even for minor advice.
- Perception of wasted money, time, and effort due to inefficiencies.

#### Process Inefficiencies
- Difficulty in document preparation, digital signatures, and filing.
- Losing track of deadlines, updates, or required procedures.
- Stressful, tedious, and often frustrating user experience.

### Software Engineering Viewpoint
- These insights highlight user pain points (problem domain analysis).
- The challenges indicate a strong need for requirement-driven solutions focusing on usability, accessibility, security, and cost-effectiveness.
- The diversity of responses shows the importance of requirements elicitation from real users before system design.

---

## Q2: What features would make you trust an AI-powered legal assistant more?

### Findings
Users expressed both expectations and skepticism. The key trust-building features are:

#### Transparency & Verification
- Clear references to legal sources (e.g., government portals, constitution articles).
- Verification or certification by experienced human lawyers.
- Proof, citations, or statistics supporting the advice.

#### Privacy & Security
- Strong protection of sensitive personal data (no misuse, no third-party access).
- Options to delete files and chat history after usage.
- Explicit user consent before data is reviewed by others.

#### Simplicity & Comprehension
- Explanations in plain, layman-friendly language.
- Step-by-step guidance on processes, required documents, and next steps.
- Avoidance of heavy legal jargon.

#### Reliability & Context Awareness
- Updated legal knowledge according to region, state, or country.
- Ability to highlight when human lawyer involvement is required.
- Summaries of pros/cons, risks, and possible outcomes.

#### User Experience
- Ease of use, fast responses, and accessible interface.
- Interactive, personalized guidance for specific legal issues.

### Software Engineering Viewpoint
- These responses reflect non-functional requirements like security, reliability, transparency, and usability.
- Skepticism shows a need for validation mechanisms, such as human-in-the-loop design where AI advice can be reviewed by a professional.
- Trust is not only a technical quality attribute but also an ethical requirement for AI-based systems.

---

## Q3: Any additional suggestions or expectations you have from Advoc AI?

### Findings
The suggestions provide insights into future enhancements and feature expectations:

#### Data Privacy as the Foundation
- Strong emphasis on safeguarding sensitive personal, business, and financial data.
- Avoiding misuse of identification details (e.g., Aadhaar, PAN).
- Ethical handling of confidential cases (e.g., family disputes, domestic violence).

#### Feature Enhancements
- Voice-based interaction for easier queries.
- Automated drafting of legal documents (in multiple formats and languages).
- Notifications for document expirations and deadlines.
- Guidance on licenses and compliance for new businesses.

#### Contextual & Human-Aware Assistance
- AI should explain the legal reasoning behind its advice (laws, sections, references).
- Support multi-language features for inclusivity.
- Sensitivity to emotional and situational aspects (e.g., victim safety in disputes).

#### Continuous Improvement & Reliability
- Regular updates to legal knowledge as laws evolve.
- Testing for bias and errors to ensure fairness.
- Providing case-based examples and step-by-step assistance.

### Software Engineering Viewpoint
- These inputs represent evolutionary requirements (future scope for system growth).
- Strong user demand for non-functional qualities like privacy, transparency, usability, adaptability, and ethical AI design.
- Expectations highlight the importance of requirements validation and iterative development to align the product with real-world user needs.

---

## Overall Analysis
- **Problem Space:** Legal services are currently expensive, time-consuming, complex, and untrustworthy for many users.
- **Requirement Space:** Users want Advoc AI to be secure, simple, transparent, and context-aware.
- **Quality Attributes:** The system must focus on privacy, accuracy, usability, reliability, and ethics to gain user trust.
- **Risks:** Skepticism remains high — many users believe AI cannot fully replace lawyers, especially in sensitive or high-stakes cases.

**Summary:**  
The responses provide valuable insights for requirements engineering, guiding the design of Advoc AI towards a secure, trustworthy, and user-centered legal assistant.

