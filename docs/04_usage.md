# Usage Guide: GenAI Email & Report Drafting System

**Project:** GenAI Email & Report Drafting System  
**Purpose:** How to use the application for generating emails and reports  
**For Setup Instructions:** See [Setup Guide](03_setup.md)

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Registration](#user-registration)
3. [Generating an Email](#generating-an-email)
4. [Generating a Report](#generating-a-report)
5. [Viewing Document History](#viewing-document-history)
6. [Understanding Generated Content](#understanding-generated-content)
7. [Examples](#examples)
8. [Admin Features](#admin-features)
9. [API Usage](#api-usage)
10. [Best Practices](#best-practices)

---

## Getting Started

Before using the application, ensure you have completed the setup process described in the [Setup Guide](04_setup.md).

**Quick Access:**

1. Ensure backend is running on `http://localhost:5000`
2. Ensure frontend is running (typically `http://localhost:5173`)
3. Open your browser and navigate to the frontend URL
4. You'll see the login page

---

## User Registration

### Creating a New Account

1. Click on "Register" from the login page
2. Enter your name, email, and password
3. Select role (default: USER)
4. Click "Register"
5. You'll be automatically logged in after successful registration

**Role Types:**

- **USER:** Can generate emails and reports, view own history
- **ADMIN:** All User permissions plus view all documents and system stats

**Password Requirements:**

- Minimum 8 characters (recommended)
- Use a strong, unique password

### Logging In

1. Enter your email address
2. Enter your password
3. Click "Login"
4. You'll be redirected to the dashboard

**Note:** Your session will be maintained via JWT tokens stored in browser localStorage.

---

## Generating an Email

### Step-by-Step Process

1. **Navigate to "Generate Email"** from the dashboard
2. **Enter the Purpose** of the email
   - Example: "Follow-up on yesterday's meeting"
   - Be specific and clear

3. **Select the Tone:**
   - **Professional:** Business-appropriate, clear, respectful
   - **Casual:** Informal, friendly, conversational
   - **Formal:** Very formal, official, traditional
   - **Friendly:** Warm, approachable, personable

4. **Provide Context** with relevant details
   - Include key points you want to mention
   - Add any specific requirements
   - Mention recipient context if relevant

5. **Optionally enter recipient email** (for your reference)

6. **Click "Generate"**
   - Wait for the AI to generate content
   - Loading indicator will show progress

7. **Review the generated email**
   - Read through the content
   - Check if it meets your requirements

8. **Take Action:**
   - **Copy:** Copy to clipboard for pasting elsewhere
   - **Save:** Store in your document history
   - **Regenerate:** Generate a new version with adjusted context

### Tips for Better Email Generation

- **Be specific:** Provide clear, detailed context
- **Include key points:** Mention all important details
- **Set appropriate tone:** Match the tone to your audience
- **Review and edit:** Always review AI-generated content before using

---

## Generating a Report

### Step-by-Step Process (Reports)

1. **Navigate to "Generate Report"** from the dashboard

2. **Enter the Purpose** of the report
   - Example: "Quarterly project status"
   - Be clear about the report's goal

3. **Select the Tone:**
   - Same options as email generation
   - Choose based on your audience

4. **Provide Context** with detailed information
   - Include all relevant data points
   - Mention key metrics or milestones
   - Add any specific sections needed

5. **Select Structure:**
   - **Executive Summary:** High-level overview with summary
   - **Detailed:** Comprehensive, in-depth report
   - **Bullet Points:** Concise, point-by-point format

6. **Click "Generate"**
   - Wait for generation (may take longer than emails)
   - Loading indicator will show progress

7. **Review the generated report**
   - Check formatting (rendered as markdown)
   - Verify all key points are covered

8. **Take Action:**
   - **Copy:** Copy to clipboard
   - **Export as PDF:** (if available) Download as PDF
   - **Save:** Store in your document history
   - **Regenerate:** Create a new version with adjusted parameters

### Tips for Better Report Generation

- **Provide structured context:** Organize your input clearly
- **Include data points:** Mention specific metrics or achievements
- **Choose appropriate structure:** Match structure to your needs
- **Use formal tone for official reports:** Professional or formal tone recommended

---

## Viewing Document History

### Accessing Your History

1. **Navigate to "History"** from the dashboard
2. View all your previously generated documents
3. Each entry shows:
   - Document type (Email/Report)
   - Purpose/Context (truncated)
   - Tone used
   - Created date
   - Actions (View, Delete)

### Filtering and Searching

- **Filter by type:** Select Email or Report from dropdown
- **Search:** Use search box to find specific documents by purpose or context
- **Sort:** Click column headers to sort by different criteria

### Viewing Full Documents

1. Click on any document row or "View" button
2. See complete generated content
3. Copy content if needed
4. Return to history list

### Deleting Documents

1. Click "Delete" button on any document
2. Confirm deletion
3. Document will be permanently removed

**Note:** You can only delete your own documents. Admins can view but not delete user documents from the history view.

---

## Understanding Generated Content

### Email Structure

Generated emails typically include:

- **Greeting:** Appropriate for selected tone
- **Purpose Statement:** Clear statement of email's goal
- **Context Details:** Information from your input
- **Conclusion:** Professional wrap-up
- **Sign-off:** Tone-appropriate closing

**Example Structure:**

```text
[Greeting based on tone]

[Purpose statement]

[Contextual details from input]
[Key points addressed]

[Professional closing]
[Sign-off based on tone]
```

### Report Structure

Generated reports include:

- **Title/Header:** Based on purpose
- **Executive Summary:** (if structure selected)
- **Sections:** Organized based on context
- **Content:** Structured according to selected format
- **Formatting:** Professional markdown formatting

**Example Structure (Executive Summary):**

```markdown
# [Report Title]

## Executive Summary
[High-level overview]

## [Section 1]
[Detailed content]

## [Section 2]
[Additional details]

## Conclusion
[Final thoughts]
```

### Tone Variations

| Tone | Characteristics | Best For |
|------|----------------|----------|
| **Professional** | Business-appropriate, clear, respectful | Most business communications |
| **Casual** | Informal, friendly, conversational | Team communications, peers |
| **Formal** | Very formal, official, traditional | Official documents, executives |
| **Friendly** | Warm, approachable, personable | Client relationships, networking |

---

## Examples

### Example 1: Professional Email

**Input:**

- **Purpose:** Follow-up on project proposal
- **Tone:** Professional
- **Context:** "Met with client yesterday, discussed Q1 timeline, need to send follow-up"

**Generated Output:**

```text
Subject: Follow-up on Project Proposal Discussion

Dear [Client Name],

Thank you for taking the time to meet with us yesterday to discuss the project proposal. I wanted to follow up on our conversation regarding the Q1 timeline.

As we discussed, the proposed timeline aligns well with your requirements, and our team is prepared to begin work as soon as we receive your approval. I've attached the detailed project plan for your review.

Please let me know if you have any questions or require any clarifications. I'm happy to schedule another meeting to address any concerns.

Looking forward to your response.

Best regards,
[Your Name]
```

### Example 2: Formal Report

**Input:**

- **Purpose:** Quarterly project status
- **Tone:** Formal
- **Context:** "Q1 2026 progress, milestones: Phase 1 complete, Phase 2 in progress, challenges: resource allocation"
- **Structure:** Executive Summary

**Generated Output:**

```markdown
# Quarterly Project Status Report - Q1 2026

## Executive Summary

This report provides a comprehensive overview of the project status for the first quarter of 2026. The project has made significant progress, with Phase 1 successfully completed and Phase 2 currently underway.

## Milestones Achieved

### Phase 1: Complete
Phase 1 has been completed successfully, meeting all defined objectives and deliverables. The team has transitioned smoothly to Phase 2.

### Phase 2: In Progress
Phase 2 is currently in progress and proceeding according to schedule. The team is actively working on the designated tasks and maintaining momentum.

## Challenges

### Resource Allocation
The primary challenge identified during this quarter relates to resource allocation. The team has identified this area as requiring additional attention to ensure continued project success.

## Recommendations

To address the resource allocation challenge, we recommend conducting a comprehensive review of current resource distribution and implementing adjustments as necessary to optimize project efficiency.

## Conclusion

Overall, the project maintains a positive trajectory with Phase 1 completed and Phase 2 progressing well. Addressing the resource allocation challenge will be key to maintaining this momentum through Q2 2026.
```

### Example 3: Casual Email

**Input:**

- **Purpose:** Team meeting reminder
- **Tone:** Casual
- **Context:** "Reminder for tomorrow's team sync at 10 AM, discuss sprint planning"

**Generated Output:**

```text
Subject: Quick Reminder - Team Sync Tomorrow!

Hey team,

Just a quick reminder that we have our team sync tomorrow at 10 AM. We'll be diving into sprint planning, so come prepared with your thoughts and ideas!

Looking forward to seeing everyone there.

Cheers,
[Your Name]
```

---

## Admin Features

If you have the ADMIN role, you have access to additional features:

### Admin Dashboard

1. **Navigate to "Admin Dashboard"** from the menu
2. View system-wide statistics:
   - Total registered users
   - Total documents generated
   - Breakdown by document type (Emails vs Reports)
   - Most used tones

### View All Documents

1. In the Admin Dashboard, access the "All Documents" section
2. View documents from all users (not just your own)
3. Filter and search across all documents
4. View full content of any document

**Note:** Admins have read-only access to user documents. You cannot delete or modify documents created by other users.

### System Monitoring

- Monitor system usage patterns
- Identify popular features
- Track user engagement
- View overall system health

---

## API Usage

You can also interact with the system programmatically using the REST API.

OpenAPI specification is available at `http://localhost:5000/api/openapi.yaml`.

**Endpoint list:** See [API Endpoints](13_api-endpoints.md) for the canonical endpoint listing.

### Authentication

```bash
# Login to get JWT token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your-password"
  }'
```

### Generate Email via API

```bash
# Generate email
curl -X POST http://localhost:5000/api/documents/email:generate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Meeting with client about project timeline",
    "tone": "professional",
    "subject": "Follow-up on meeting"
  }'
```

### Generate Report via API

```bash
# Generate report
curl -X POST http://localhost:5000/api/documents/report:generate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Quarterly status",
    "tone": "formal",
    "key_points": "Q1 progress and milestones",
    "structure": "executive_summary"
  }'
```

### Get Document History

```bash
# Get your documents
curl -X GET http://localhost:5000/api/history \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**For complete API documentation, see [Requirements Specification](02_requirements.md#core-api-design).**

---

## Best Practices

### 1. Provide Clear Context

**Good Context:**

```text
"Need to follow up with client John Smith regarding the Q1 proposal we discussed on January 10th. Key points: timeline approval needed by January 20th, budget confirmed at $50K, three-phase implementation plan."
```

**Poor Context:**

```text
"Follow up on proposal"
```

### 2. Choose Appropriate Tone

- **Professional:** Default for most business communications
- **Formal:** Official documents, senior executives, legal matters
- **Casual:** Internal team communications, friendly colleagues
- **Friendly:** Building relationships, networking, warm outreach

### 3. Review Generated Content

- **Always review** AI-generated content before using
- **Edit as needed** to match your specific requirements
- **Verify accuracy** of any facts or details
- **Personalize** when appropriate

### 4. Use History Effectively

- **Save important documents** for future reference
- **Search history** to find similar past documents
- **Maintain consistency** by referencing previous communications
- **Clean up regularly** by deleting outdated documents

### 5. Iterative Refinement

If the first generation doesn't meet your needs:

1. **Analyze what's missing** or incorrect
2. **Adjust your context** to be more specific
3. **Try a different tone** if appropriate
4. **Regenerate** with improved inputs
5. **Compare versions** to find the best output

### 6. Security Practices

- **Use strong passwords** for your account
- **Don't share** your login credentials
- **Logout** when using shared computers
- **Protect sensitive information** in generated documents
- **Review permissions** before sharing generated content

### 7. Quality Assurance

- **Proofread** all generated content
- **Verify facts** and figures
- **Check formatting** (especially for reports)
- **Test tone** with your audience in mind
- **Get feedback** on important communications

---

**Document Version:** 1.0  
**Last Updated:** January 13, 2026  
**Status:** Complete
