# B. VIVA Q&A (40 QUESTIONS – EXAM-READY)

---

## **1. What is Generative AI?**

Generative AI refers to AI models that can generate new content such as text, images, or code based on learned patterns.

## **2. Why did you choose Google Gemini?**

Gemini provides strong instruction-following, reliable text generation, and is backed by Google, making it suitable for academic and enterprise use.

## **3. What problem does your system solve?**

It automates professional email and report drafting, reducing manual effort and improving consistency.

## **4. What architecture did you use?**

An N-Tier architecture with React, Flask, PostgreSQL, and an AI service layer.

## **5. Why N-Tier architecture?**

It improves scalability, maintainability, and separation of concerns.

## **6. What is JWT?**

JWT is a stateless authentication mechanism using signed tokens to secure APIs.

## **7. Why not Auth0?**

Auth0 adds unnecessary complexity for an academic project; JWT provides sufficient security.

## **8. What is RBAC?**

Role-Based Access Control restricts system access based on user roles.

## **9. What roles exist in your system?**

Admin and User.

## **10. What can an Admin do?**

View all generated documents and system usage data.

## **11. What can a User do?**

Generate emails/reports and view personal history.

## **12. How is data stored?**

In a PostgreSQL relational database.

## **13. Why PostgreSQL?**

It provides ACID compliance, reliability, and strong relational support.

## **14. What is prompt engineering?**

Designing structured prompts to control AI output.

## **15. How do you control tone?**

Tone is passed as a prompt parameter.

## **16. Is your system vendor-locked?**

No, the AI layer is abstracted.

## **17. How do you ensure security?**

JWT authentication, password hashing, and role checks.

## **18. What happens if Gemini API fails?**

The system returns an error message to the user.

## **19. Is training involved?**

No, the system uses inference-only API calls.

## **20. What are the limitations of your project?**

No fact verification and dependency on AI API availability.

## **21. Can this system scale?**

Yes, due to stateless APIs and modular architecture.

## **22. How is history maintained?**

Generated documents are stored with user IDs and timestamps.

## **23. What type of prompts are used?**

Instruction-based prompts.

## **24. How is the frontend secured?**

By protecting routes using JWT tokens.

## **25. What is the role of Flask?**

It acts as the backend API and business logic layer.

## **26. Why React for frontend?**

It provides a responsive and modular UI.

## **27. What is the AI service layer?**

The layer responsible for interacting with Google Gemini.

## **28. How do you prevent misuse?**

Authentication, authorization, and input validation.

## **29. Is this suitable for enterprises?**

Yes, with additional IAM and analytics integrations.

## **30. Can this support multiple languages?**

Yes, as a future enhancement.

## **31. What are evaluation metrics?**

Content quality, tone accuracy, time efficiency, and user satisfaction.

## **32. What is stateless authentication?**

Authentication without server-side session storage.

## **33. How are passwords stored?**

As hashed values, not plain text.

## **34. What is RAG?**

Retrieval-Augmented Generation, combining search with LLMs.

## **35. Is RAG used here?**

No, but it is planned as a future enhancement.

## **36. What is the biggest challenge in GenAI systems?**

Controlling output accuracy and hallucinations.

## **37. How does your system handle hallucinations?**

By restricting prompts to user-provided context.

## **38. Can this be deployed to cloud?**

Yes, it is cloud-ready.

## **39. What did you learn from this project?**

GenAI integration, secure architecture, and prompt engineering.

## **40. How can this project be extended?**

By adding RAG, analytics, SSO, and multilingual support.

---
