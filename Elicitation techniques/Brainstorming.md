[Brainstorming _SE_Project.md](https://github.com/user-attachments/files/22450903/Brainstorming._SE_Project.md)
# **Brainstorming for Requirement Elicitation**

## 

## **Author(s) :** Maharshi Patel(202301486) <br> &nbsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp; Jainesh Patel(202301446)
          
	           

## 

## **1\. Brainstorming**

* **Definition:** Brainstorming is a group creativity technique where users/stakeholders come together to generate a wide range of ideas/requirements in a period of time, without immediately judging or evaluating them. It encourages open thinking and free flow of ideas. It helps in exploring new perspectives, and coming up with wild extreme ideas that may not come up in other similar elicitation techniques.

## **2\. Why use Brainstorming in our Project?**

* Our system covers various domains such as law, technology, business, and user experience.  
* Each stakeholder/user can have **different perspectives** which contribute to ideas generation.(e.g: a lawyer cares about accuracy and correctness, while a user cares about simplicity).  
* This method allows combining legal expertise with user needs along with checking for technical feasibility.  
* The method can help in generating  **creative and futuristic features.** (We came up with ideas like this : AI-powered fraud detection, smart contract suggestions, voice-based document explanations, multilingual support and inter-language document conversion).

## **3\. Steps for Brainstorming Elicitation**

**People in the Brainstorming: (10 people) (virtual meeting)**

**Scribe:** Write's down all the ideas  
**Moderator:** Moderates the session  
**Participants:** People with legal knowledge, general users(from our group and other general people), developers(from our group)

* We started with some basic questions (like Have you ever faced difficulty in understanding legal documents, what is the worst thing you have experienced with it, has legal language ever feared you, has misinterpreting legal documents landed you in a troublesome situation) so as to make the participants comfortable and to initiate the conversation.  
* Everyone spoke about the difficulties they have faced while working with legal documents. We gave time to each individual for saying their own past experiences that they have with legal complexity.  
* Then we asked a few questions like what they expect from this type of platform that resolves the problems they have faced and caters their needs.  
* Everyone started coming up with their own ideas, based on their creativity and past experiences.  
* The scribe noted down all the ideas that came up by all.  
* All the ideas that came up were thoroughly discussed taking advice from the legal experts and the developers. Each participant's viewpoints regarding each idea were taken into consideration. They were combined into various groups.  
* The ideas were then prioritized based on their necessity, how critical they can be for user experience and adoption, feasibility, legal validity, etc. We also kept in mind the DVF (Desirability, Viability, and Feasibility).  
* In some cases voting was used to help achieve consensus.  
* Used **MoSCoW** prioritisation method **(Must have, Should have, Could have, Won't Have)** for assessment of ideas.  
* Final recorded all raw ideas and final prioritized requirements.

**All Ideas recorded :**

(All ideas were captured without judgment — both practical and wild ones)

### A) Document Simplification/Summary

* Complex legal documents, hard to comprehend for common people, can be converted into simple, easy to understand language using AI.  
* Highlight the critical clauses in the document that may have high risk legally for the party.  
* The voice assistant reads out contract terms in simple words.  
* Clause-by-clause video explanations for users.  
* Visual summaries (infographics of key obligations, rights, penalties).

### B) Document Generation & Editing

* Standard templates for NDAs, rent agreements, contracts, etc. are modified using AI on the basis of the case provided  
* Provides the feature of auto-filling common details (names, dates, addresses) from user profile.  
* Allows Multiple users/parties to real-time edit generated legal documents (just like Google Docs).  
* Various parties can make suggestions/comments in the documents.  
* Suggestions which are accepted by all other parties are added to the documents.  
* AI auto-suggests missing legal clauses (e.g., termination clause, dispute resolution).  
* Integration with Microsoft Word/Google Docs for import/export.

### C) Version Tracking & E-signature

* Full version history providing comparison with the previous versions (highlight added/removed clauses).  
* Allows to move back to previous versions.  
* Provides integration of e-signature that is legally compliable.  
* Multi-party signing workflow (signatures in sequence or parallel).  
* To ensure high-stakes contracts cannot be altered or faked, use secured storage mechanism technology like Blockchain.

### D) Lawyer/Expert Support

* Help to connect to a lawyer based on the case type/case briefing provided  
* Can filter the lawyers on their field of expertise, experience, rating, fees, etc.  
* Live chat/video call with a lawyer from within the platform.  
* Lawyers can annotate directly on the document.  
* Lawyer verification badges/e \- signature for trustworthiness.  
* Lawyer connect feature for the cases in which escalation is required.  
* Separate lawyer portal where they have their own profile, which is verified by the platform and they are connected to the clients by this.  
* Users can schedule appointments with a lawyer.

### E) Compliance & Security

* Automatic check for legal compliance.  
* Secure cloud storage with encryption.  
* Role-based access (who can view/edit/sign).

### F) User Support & Accessibility

* Mobile app version for quick access.  
* Chatbot Q\&A for “What does this clause mean?”  
* Multi-language support (e.g., Hindi, Gujarati, English).  
* Voice-to-text for dictating contracts.  
* Accessibility features (screen reader compatibility).  
* Voice based querying support.

**Prioritized ideas based on MoSCoW:** 

Then, we clustered and prioritized using **MoSCoW (Must, Should, Could, Won’t Have for now)**.

**Must-Have (Core MVP features)**

* Complex legal documents, hard to comprehend for common people, can be converted into simple, easy to understand language using AI  
* Standard templates for NDAs, rent agreements, contracts modified using AI on the basis of the case provided.  
* Various parties can make suggestions/comments in the documents  
* Version tracking with rollback.  
* E-signature integration.  
* Lawyer connection feature (at least request/appointment booking).  
* Compliance check for mandatory clauses.  
* Secure storage & role-based access.

### **Should-Have (Next release features)**

* Highlighting for risky clauses.  
* Lawyer annotations inside documents.  
* AI suggestion engine for missing clauses.  
* Privacy and Security of users data.

### **Could-Have (Innovative add-ons)**

* Voice assistant for clause explanations.  
* Infographic-based document summaries.  
* Voice-to-text contract dictation.  
* Live video consultations with lawyers.  
* Voice based querying support.  
* Multi-language support (e.g., Hindi, Gujarati, English).

### **Won’t-Have (For now — future roadmap)**

* Blockchain-based document validation.  
* Fully automated smart contracts.  
* Clause-by-clause video explanations.  
* Deep integration with Word/Google Docs (complex and secondary).

**Functional Requirements that we derived from this method :**

1. Document Summarizer.  
2. Legal Document Generation.  
3. E-signature integration on documents.  
4. Lawyer connect feature.  
5. Version tracking with rollback.  
6. Multi-party comments and suggestions.
7. Collaborative features.
   

**Non-Functional Requirements that we derived from this method :**  

1. Privacy and security of data of users.  
   

**User-Stories :** 

| ID | User Story (Front Card) | Acceptance Criteria (Back Card) |
| :---- | :---- | :---- |
| **1** | As a user, I want complex legal documents to be converted into simple, plain language so that I can easily understand the content without legal expertise. | Summarizes complex legal documents into easy to understand language The document clauses are correctly interpreted, analyzed and simplified. User can further ask for clarifications or clause based explanation using chatbot |
| **2** | As a user, I want to generate legal documents using standard templates personalized based on my case details so that I don’t have to draft from scratch. | The system provides pre-built templates. The AI personalizes templates using the case details provided(e.g., duration, parties, rent., and other details). Generates customized drafts. The drafts must contain all the necessary legal clauses as per the case and client requirements The draft complies with the legal provisions |
| **3** | As a stakeholder, I want to add suggestions and comments on documents so that multiple parties can collaboratively review before finalization.  | Users can comment inline. Changes are tracked using author identity. Other parties can see the comments and can accept, reject or can further suggest changes to the comments made. Notifications sent to the concerned parties when comments are added. When all the parties accept the suggested changes the changes are updated in the generated document |
| **4** | As a user, I want version tracking for legal documents so that I can review change history and roll back to a previous version if needed. | Each edit version of the document is stored as a new version. Rollback possible to any previous version. Metadata (who edited, when) is captured and stored |
| **5** | As a user, I want e-signature support so that contracts can be signed digitally without printing or scanning. | Legally valid signatures (e.g., Aadhaar eSign, DocuSign, Stamp) are added to document as watermark Data of who e-signed the document, when is stored Signed copy stored securely. E-sign complies with the legal provisions |
| **6** | As a user, I want to request or book an appointment with a lawyer so that I can get expert advice when needed. | Users can filter lawyers on the basis of their area of expertise, experience, rating, fees, etc. AI suggests them lawyers on the basis of the case and details provided. Users can request consultation from lawyers. Lawyers notified with request details including the user and the case details considering the security and privacy The lawyers can accept/reject for consultation. Appointment scheduling supported. |
| **7** | As a user, I want the system to check if my legal document contains all mandatory clauses so that I don’t miss important legal requirements.  | AI scans for the documents for required clauses as per legal provisions (e.g., in NDA \-- confidentiality, jurisdiction). Warns if clauses are missing. Suggest the clauses to be added to the document. |
| **8** | As an admin, I want secure storage and role-based access control so that sensitive legal documents are protected and only authorized users can view/edit them. | Encrypted storage of documents. Role-based access (viewer, editor, admin, lawyer). Activity logs for every access/change. |

